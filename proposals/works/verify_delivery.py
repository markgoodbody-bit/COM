"""Read only exact local preview routes; bound delivery claims to the built inventory."""
import hashlib
import json
from urllib.request import urlopen
from urllib.parse import urlparse
from pathlib import Path

ROOT=Path(__file__).resolve().parent
OUT=ROOT.parents[1]/'outputs/works-exact-lineage'
inventory=json.loads((OUT/'inventory.json').read_text())
for route,pin in inventory.items():
    with urlopen('http://127.0.0.1:8834/'+route,timeout=5) as response:
        assert response.status==200
        body=response.read()
        assert len(body)==pin['bytes'] and hashlib.sha256(body).hexdigest()==pin['sha256'],route
measures=json.loads(Path('C:/Users/markg/Downloads/PSFH-five-repaired-render-20260909/measurements.json').read_text())
rows=[]
for r in measures['results']:
    images=[urlparse(im['src']).path.lstrip('/') for im in r['images']]
    rows.append(dict(view=r['view'],slug=r['slug'],image_bytes=sum(inventory[p]['bytes'] for p in set(images)),selected_images=images))
(OUT.parent/'works-delivery-observation.json').write_text(json.dumps(dict(scope=f'{len(inventory)} exact local HTTP responses; selected-image bytes from DPR1 full-document rendering, not initial-load timing/transfer or physical-device testing',images=rows),indent=2)+'\n')
print(f'PASS:{len(inventory)} exact HTTP deliveries. Selected-image bytes:')
for r in rows:
    if r['view'] in ['desktop','mobile']:print(r['view'],r['slug'] or 'shelf',r['image_bytes'])
