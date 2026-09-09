"""Isolated first-five shelf: custody checks, per-work pages, no normal build wiring."""
import hashlib
import importlib.util
import json
import shutil
from html import escape as e
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlparse
from PIL import Image

ROOT = Path(__file__).resolve().parent
PROPOSALS = ROOT.parent
OUT = PROPOSALS.parent / 'outputs/works-first-five'
NEW = [('atkins','anna-atkins','cyanotype'),('shen','shen-zhou','scroll'),('lewis','edmonia-lewis','sculpture')]
IDENTITIES={'atkins':('Anna Atkins','Ulva lactuca','291638'),'shen':('Shen Zhou','Anchorage on a rainy night','49549'),'lewis':('Edmonia Lewis','The Death of Cleopatra','saam_1994.17')}
PINS = {'atkins':['ae5864af965af2d8a063016b1df67a9e765270281b9bc313513cde12d9f974a6'],
 'shen':['e9bc05358ce37ef9eae53dd5454fca797b1e1f43ba4dbdb9164e702493282004'],
 'lewis':['d6494d0620ad68d9e35aaafda8d298891c783bfbc6cef21c729865fdb1230b28','e9b53e97cf3e7c9cf7bb0de851f6e6c4c14e6fb2b0c73f0591687cef521bca24']}


def sha(data): return hashlib.sha256(data).hexdigest()


def require(ok, message):
    if not ok: raise ValueError(message)


def check_new(work):
    folder = PROPOSALS / work
    r = json.loads((folder/'artwork.json').read_text(encoding='utf-8'))
    views = json.loads((folder/'images.json').read_text(encoding='utf-8'))
    require((r['creator'],r['title'],r['object_id'])==IDENTITIES[work],'Work identity drift')
    require(r['master_status']=='UNKNOWN' and r['project_response'] is None, 'Unreviewed claim')
    require([v['source']['sha256'] for v in views] == PINS[work], 'Wrong source/view/order')
    for view in views:
        source = view['source']
        parent = folder/'assets'/view['parent_file']
        require(sha(parent.read_bytes())==source['sha256'] and parent.stat().st_size==source['bytes'], 'Source bytes')
        with Image.open(parent) as im:
            require(im.size==(source['width'],source['height']), 'Source dimensions')
            icc=im.info.get('icc_profile')
        for v in view['variants']:
            path=folder/'assets'/v['file']
            require(v['parent_sha256']==source['sha256'], 'Detached derivative')
            require(sha(path.read_bytes())==v['sha256'] and path.stat().st_size==v['bytes'], 'Viewing bytes')
            require(v['width']<=source['width'] and abs(v['height']-source['height']*v['width']/source['width'])<=.5, 'Crop/upscale')
            with Image.open(path) as im:
                require(im.size==(v['width'],v['height']) and im.info.get('icc_profile')==icc, 'Viewing dimensions/ICC')
    return r,views


def image_html(view, alt, width):
    last=view['variants'][-1]
    srcset=', '.join('../../art/'+v['file']+' '+str(v['width'])+'w' for v in view['variants'])
    return f'<a href="../../art/{e(view["parent_file"])}"><img src="../../art/{e(last["file"])}" srcset="{e(srcset)}" sizes="(max-width: {width+32}px) calc(100vw - 32px), {width}px" width="{last["width"]}" height="{last["height"]}" alt="{e(alt)}"></a>'


def render_work(work, slug, kind, r, views):
    credit=f'<p>{e(r["institution"])}. {e(r["credit"])}. {e(r["accession"])}.</p><p><a href="{e(r["object_url"])}">Museum record</a> · {e(r["rights"])}</p>'
    if kind=='sculpture':
        art='<div class="views">'+''.join(f'<figure>{image_html(v,r["alts"][i],578)}<figcaption class="view-label">Museum view {i+1} · {e(v["source"]["view_id"])}</figcaption></figure>' for i,v in enumerate(views))+'</div><div class="credit">'+credit+'<p>Two photographs of one sculpture. Open either image for its unchanged museum file. These are not all possible views.</p></div>'
    else:
        art='<figure>'+image_html(views[0],r['alt'],720 if work=='atkins' else 600)+'</figure>'
        art=art.replace('</figure>','<figcaption>'+credit+'</figcaption></figure>')
    context=''
    if work=='atkins': context=f'<section class="context"><p>From <cite>{e(r["book"])}</cite>.</p><p>The supplied photograph includes the page and book edges. They are retained here.</p></section>'
    if work=='shen': context=f'<section class="context"><h2>Painting and inscription</h2><p>{e(r["museum_account"])}</p><p><a href="{e(r["object_url"])}">Read the poem and museum account</a></p><p>The complete supplied photograph is retained, including the pictured inscriptions. It is not a claim to show every part of the physical mounting.</p></section>'
    info=f'<details><summary>Source and viewing copies</summary><p>Smaller full-frame viewing copies are shown; the unchanged museum files remain linked from the images. No crop, retouch or generated view. Museum-master status is unknown.</p><p><a href="../../art/{work}-images.json">Image identities and preparation</a> · <a href="../../art/{work}.json">Work record</a></p></details>'
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>{e(r["title"])} · {e(r["creator"])}</title><link rel="stylesheet" href="../shelf.css"></head><body><a class="skip" href="#work">Skip to the work</a><nav class="shelf-return"><a href="../index.html">All works</a> · Unpublished preview</nav><main id="work" class="work-page {kind}"><header><p>{e(r["creator"])}</p><h1>{e(r["title"])}</h1><p>{e(r["date"])} · {e(r["medium"])}</p></header>{art}{context}{info}</main></body></html>'


class Routes(HTMLParser):
    def __init__(self):
        super().__init__(); self.urls=[]; self.images=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        require(tag not in {'script','iframe','form'},'Active content')
        require(not any(k.startswith('on') for k in a),'Handler')
        for k in ('href','src'):
            if k in a:self.urls.append(a[k])
        if tag=='img':
            require('alt' in a,'Missing alt')
            self.images.append(a)
            for part in a.get('srcset','').split(','):
                if part.strip():self.urls.append(part.strip().split()[0])


def build():
    outputs={}
    def put(route,data):
        require(route not in outputs,'Route collision '+route)
        outputs[route]=data.encode('utf-8') if isinstance(data,str) else data
    # Powers is held out until PR127 has a repaired, reviewed head.
    for work in ['vermeer']:
        spec=importlib.util.spec_from_file_location('proposal_'+work,PROPOSALS/work/'build.py')
        mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);mod.validate()
        for name,route in mod.ROUTES.items():
            data=(PROPOSALS/work/name).read_bytes()
            if name=='index.html':
                text=data.decode('utf-8').replace('</head>','<link rel="stylesheet" href="../shelf.css"></head>')
                data=text.replace('<main ', '<nav class="shelf-return"><a href="../index.html">All works</a></nav><main ',1).encode('utf-8')
            put(route,data)
    entries=[dict(creator='Johannes Vermeer',title='The Geographer',date='1669',medium='Oil on canvas',slug='johannes-vermeer',image='staedel-1149-thumb-xl.jpg',width=915,height=1024)]
    for work,slug,kind in NEW:
        r,views=check_new(work)
        put(f'works/{slug}/index.html',render_work(work,slug,kind,r,views))
        for name in ['artwork.json','images.json']:
            put(f'art/{work}{"-images" if name=="images.json" else ""}.json',(PROPOSALS/work/name).read_bytes())
        for v in views:
            for name in [v['parent_file']]+[x['file'] for x in v['variants']]:put('art/'+name,(PROPOSALS/work/'assets'/name).read_bytes())
        thumb=views[0]['variants'][0]
        entries.append(dict(creator=r['creator'],title=r['title'],date=r['date'],medium=r['medium'],slug=slug,image=thumb['file'],width=thumb['width'],height=thumb['height']))
    cards=''.join(f'<li><a href="{x["slug"]}/index.html"><div class="image-space"><img src="../art/{x["image"]}" width="{x["width"]}" height="{x["height"]}" alt="" loading="lazy"></div><p class="maker">{e(x["creator"])}</p><h2>{e(x["title"])}</h2><p class="medium">{e(x["date"])} · {e(x["medium"])}</p></a></li>' for x in entries)
    # Linked images repeat the adjacent creator/title; avoid duplicate screen-reader text.
    shelf=f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex"><title>Works · Please Start From Here</title><link rel="stylesheet" href="shelf.css"></head><body><main class="collection"><header><p>Please Start From Here · Unpublished collection preview</p><h1>Works</h1><p>Four works, with room to look. Each opens onto its own page and museum record.</p></header><ul class="shelf">{cards}</ul><footer>This is a local review collection, not a published edition. The works are not endorsements of this project.</footer></main></body></html>'
    put('works/index.html',shelf)
    put('works/shelf.css',(ROOT/'shelf.css').read_bytes())
    for route,data in outputs.items():
        if route.endswith('.html'):
            parser=Routes();parser.feed(data.decode('utf-8'))
            for url in parser.urls:
                if url.startswith(('https://','#')):continue
                resolved=urljoin('/'+route,url).lstrip('/')
                require(resolved in outputs,'Missing local route '+resolved)
    inventory={route:dict(bytes=len(data),sha256=sha(data)) for route,data in outputs.items()}
    for route,data in outputs.items():
        target=OUT/route;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
    (OUT/'inventory.json').write_text(json.dumps(inventory,indent=2)+'\n',encoding='utf-8')
    require({p.relative_to(OUT).as_posix() for p in OUT.rglob('*') if p.is_file()}==set(outputs)|{'inventory.json'},'Unexpected old output')
    print('PASS:',len(outputs),'exact outputs; four distinct work routes; Powers excluded; local links resolve; no normal/public build touched.')
    return inventory


if __name__=='__main__':build()
