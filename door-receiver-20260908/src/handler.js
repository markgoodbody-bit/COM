import {Store,Problem,newKey,sha,text} from './store.js';
import {correctionAdmin} from './correction-handler.js';
import {edgeAdmission} from './edge-admission.js';
const enc=new TextEncoder();
const esc=s=>String(s??'').replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;')
  .replaceAll('"','&quot;').replaceAll("'",'&#39;');
const headers={
  'Cache-Control':'no-store', 'Referrer-Policy':'no-referrer', 'X-Content-Type-Options':'nosniff',
  'Content-Security-Policy':"default-src 'none'; style-src 'unsafe-inline'; form-action 'self'; base-uri 'none'; frame-ancestors 'none'"
};
const css=`:root{color-scheme:light dark}body{font:1rem/1.6 system-ui,sans-serif;max-width:70ch;margin:2rem auto;padding:0 1rem}h1{font-size:1.953125rem;line-height:1.2}h2{font-size:1.5625rem;line-height:1.2}input,textarea,button{font:inherit;box-sizing:border-box;max-width:100%;padding:.5rem}textarea,input{display:block;width:100%;margin:.5rem 0 1rem}pre,code{font-family:ui-monospace,monospace;white-space:pre-wrap;overflow-wrap:anywhere}a{color:LinkText}a:focus-visible,input:focus-visible,textarea:focus-visible,button:focus-visible{outline:3px solid currentColor;outline-offset:3px}section{margin:2rem 0}label{display:block}button{margin:.5rem .5rem .5rem 0}`;
function page(title,body,status=200){return new Response(`<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${esc(title)}</title><style>${css}</style></head><body><main><p>LOCAL PROTOTYPE 0.1 — SYNTHETIC DATA ONLY</p><h1>${esc(title)}</h1>${body}</main></body></html>`,{status,headers:{...headers,'Content-Type':'text/html; charset=utf-8'}});}
function json(obj,status=200){return new Response(JSON.stringify(obj),{status,headers:{...headers,'Content-Type':'application/json; charset=utf-8'}});}
function form(input={},error=''){
  const retry=input.retry_key??newKey(), management=input.management_key??newKey();
  return `${error?`<p role="alert">${esc(error)}</p>`:''}<p>This is a local demonstration, not the public Door. Use invented examples only. Sending offers this text for possible publication after an authorised moderator reviews it. No GitHub account is needed. A stored receipt is not publication or a project answer.</p><p>Limit: 4,000 Unicode code points; optional self-asserted name: 80. Do not send personal case details, credentials or files.</p><form method="post" action="/submit"><label>Message<textarea name="body" rows="6" required>${esc(input.body)}</textarea></label><label>Optional display name<input name="display_name" value="${esc(input.display_name)}"></label><input type="hidden" name="retry_key" value="${esc(retry)}"><input type="hidden" name="management_key" value="${esc(management)}"><p>Save these private keys before sending to recover an uncertain result. They are not identities. Never post them publicly.</p><p>Retry key: <code>${esc(retry)}</code><br>Management key: <code>${esc(management)}</code></p><button>Send synthetic contribution</button></form>`;
}
function manageForm(){return `<h2>Check or manage a receipt</h2><form method="post" action="/manage"><label>Reference<input name="id" required></label><label>Private management key<input name="management_key" type="password" required autocomplete="off"></label><label>Revision number (for replacement)<input name="revision" inputmode="numeric"></label><label>Replacement text or reconsideration reason<textarea name="body" rows="4"></textarea></label><label>Display name for replacement<input name="display_name"></label><button name="action" value="receipt">Check status</button><button name="action" value="revise">Submit replacement for review</button><button name="action" value="withdraw">Withdraw body</button><button name="action" value="reconsider">Request reconsideration</button></form>`;}
async function readInput(request){
  const type=(request.headers.get('content-type')??'').split(';')[0].trim().toLowerCase();
  if(!['application/json','application/x-www-form-urlencoded'].includes(type)) throw new Problem(415,'UNSUPPORTED_CONTENT_TYPE');
  const declared=Number(request.headers.get('content-length')??0);
  if(declared>65536) throw new Problem(413,'REQUEST_TOO_LARGE');
  let size=0;const parts=[],reader=request.body?.getReader();
  if(reader)for(;;){const {done,value}=await reader.read();if(done)break;size+=value.byteLength;if(size>65536){await reader.cancel();throw new Problem(413,'REQUEST_TOO_LARGE');}parts.push(value);}
  const bytes=new Uint8Array(size);let offset=0;for(const p of parts){bytes.set(p,offset);offset+=p.length;}
  let source;try{source=new TextDecoder('utf-8',{fatal:true}).decode(bytes);}catch{throw new Problem(400,'INVALID_UTF8');}
  let input;
  try {
    if(type==='application/json')input=JSON.parse(source);
    else {const params=new URLSearchParams(source);input={};for(const [k,v] of params){if(Object.hasOwn(input,k))throw new Error('duplicate');Object.defineProperty(input,k,{value:v,enumerable:true});}}
  }catch{throw new Problem(400,'INVALID_REQUEST');}
  if(!input||Array.isArray(input)||typeof input!=='object')throw new Problem(400,'INVALID_REQUEST');
  return input;
}
async function admin(request,input,env){
  const expected=env.ADMIN_TOKEN;
  if(typeof expected!=='string'||expected.length<32)throw new Problem(503,'MODERATOR_NOT_CONFIGURED');
  const provided=request.headers.get('authorization')?.replace(/^Bearer /,'')??input.admin_token??'';
  const a=await sha(expected),b=await sha(String(provided));let d=0;
  for(let i=0;i<a.length;i++)d|=a.charCodeAt(i)^b.charCodeAt(i);
  if(d!==0)throw new Problem(401,'MODERATOR_AUTH_REQUIRED');
}
/** Works with the D1 call shape. Public deployment intentionally refuses all requests. */
export async function handle(request,env,clock=()=>Date.now()){
  const url=new URL(request.url), browser=!url.pathname.startsWith('/api/');
  let input;
  try {
    if(env.SYNTHETIC_ONLY!=='true'||!['localhost','127.0.0.1','[::1]'].includes(url.hostname))
      throw new Problem(503,'LOCAL_SYNTHETIC_PROTOTYPE_ONLY');
    if(url.origin!==env.APP_ORIGIN||url.search)throw new Problem(400,'INVALID_REQUEST_ORIGIN_OR_QUERY');
    if(!env.DB)throw new Problem(503,'STORAGE_UNAVAILABLE');
    if(request.method==='POST'){
      const origin=request.headers.get('origin');
      if(origin&&origin!==env.APP_ORIGIN)throw new Problem(403,'CROSS_ORIGIN_POST_REFUSED');
      if(['/submit','/api/submit'].includes(url.pathname))await edgeAdmission(env,'contribution');
      input=await readInput(request);
    }
    const store=new Store(env.DB,clock);await store.sweep();
    if(request.method==='GET'&&url.pathname==='/api/keys')return json({retry_key:newKey(),management_key:newKey()});
    if(request.method==='GET'&&url.pathname==='/api/posts')return json({posts:await store.publicItems()});
    if(request.method==='GET'&&url.pathname==='/'){
      const posts=await store.publicItems(), readiness=await store.first('SELECT enabled,ready_until FROM service WHERE id=1');
      const open=readiness.enabled&&readiness.ready_until>clock();
      const list=posts.map(p=>`<article><h3>${esc(p.display_name||'Unnamed contributor')} (self-asserted)</h3><p><code>${esc(p.id)}</code> · revision ${p.revision}</p><pre>${esc(p.body)}</pre>${p.responses.map(r=>`<p>Project response — ${esc(r.actor)}</p><pre>${esc(r.body)}</pre>`).join('')}</article>`).join('');
      return page('A contribution can be received and answered',`<p>New intake: <strong>${open?'open for synthetic tests':'paused'}</strong>. Published content is not endorsement.</p><section>${form()}</section><section>${manageForm()}</section><section><h2>Approved synthetic contributions</h2>${list||'<p>None published.</p>'}</section><p><a href="/api/posts">Public JSON</a></p>`);
    }
    if(request.method==='POST'&&['/submit','/api/submit'].includes(url.pathname)){
      if(typeof env.RATE_SECRET!=='string'||env.RATE_SECRET.length<32)throw new Problem(503,'RATE_LIMIT_NOT_CONFIGURED');
      // Local prototype is intentionally one client. Never trust a browser-supplied client ID.
      const clientHash=await sha(env.RATE_SECRET+':local-loopback:'+Math.floor(clock()/86400000));
      const result=await store.submit(input,clientHash);
      return browser?page('Stored receipt — not yet an answer',`<pre>${esc(JSON.stringify(result,null,2))}</pre><p>Keep your existing private management key. No secret appears in the reference URL.</p>${manageForm()}<p><a href="/">Return</a></p>`,200):json(result,200);
    }
    if(request.method==='POST'&&['/manage','/api/manage'].includes(url.pathname)){
      let result;
      const revision=typeof input.revision==='string'&&/^\d+$/.test(input.revision)?Number(input.revision):input.revision;
      if(input.action==='receipt')result=await store.receipt(input.id,input.management_key);
      else if(input.action==='revise')result=await store.revise(input.id,input.management_key,{...input,revision});
      else if(input.action==='withdraw')result=await store.withdraw(input.id,input.management_key);
      else if(input.action==='reconsider')result=await store.reconsider(input.id,input.management_key,input.body);
      else throw new Problem(400,'UNKNOWN_ACTION');
      return browser?page('Contribution status',`<pre>${esc(JSON.stringify(result,null,2))}</pre>${manageForm()}<p><a href="/">Return</a></p>`):json(result);
    }
    if(request.method==='POST'&&url.pathname==='/api/admin'){
      await admin(request,input,env);const actor='authorised-local-operator';let result;
      if(['corrections','resolve-correction'].includes(input.action))return json(await correctionAdmin(input,env,clock,actor));
      if(input.action==='ready'||input.action==='pause')result=await store.readiness(input.action==='ready');
      else if(input.action==='queue')result={queue:await store.queue()};
      else if(input.action==='respond')result=await store.respond(input.id,input,actor);
      else result=await store.moderate(input.id,input,actor);
      return json(result);
    }
    throw new Problem(404,'ROUTE_NOT_FOUND');
  }catch(error){
    const status=error instanceof Problem?error.status:503;
    const code=error instanceof Problem?error.code:'STORAGE_OR_SERVICE_FAILURE';
    const notice=code==='STORAGE_OR_SERVICE_FAILURE'?'No confirmed receipt. A write may have committed before the failure. Retrying the SAME request and keys can recover it; do not infer that nothing was stored.':code;
    if(browser&&url.pathname==='/submit'&&input)return page('Not confirmed',form(input,notice),status);
    return browser?page('Request not completed',`<p>${esc(notice)}</p><a href="/">Return</a>`,status):json({error:code,detail:notice},status);
  }
}
