import {Problem,newKey,sha} from './store.js';
import {CorrectionStore} from './correction-store.js';
import {edgeAdmission} from './edge-admission.js';

const esc=s=>String(s??'').replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;')
  .replaceAll('"','&quot;').replaceAll("'",'&#39;');
const headers={
  'Cache-Control':'no-store','Referrer-Policy':'no-referrer','X-Content-Type-Options':'nosniff',
  'Content-Security-Policy':"default-src 'none'; style-src 'unsafe-inline'; form-action 'self'; base-uri 'none'; frame-ancestors 'none'"
};
const css=`:root{color-scheme:light dark}body{font:1rem/1.6 system-ui,sans-serif;max-width:70ch;margin:2rem auto;padding:0 1rem}input,textarea,select,button{font:inherit;box-sizing:border-box;max-width:100%;padding:.5rem}textarea,input,select{display:block;width:100%;margin:.5rem 0 1rem}pre,code{font-family:ui-monospace,monospace;white-space:pre-wrap;overflow-wrap:anywhere}a:focus-visible,input:focus-visible,textarea:focus-visible,select:focus-visible,button:focus-visible{outline:3px solid currentColor;outline-offset:3px}`;
function page(title,body,status=200){return new Response(`<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${esc(title)}</title><style>${css}</style></head><body><main><p>LOCAL CORRECTION EVALUATION — SYNTHETIC DATA ONLY</p><h1>${esc(title)}</h1>${body}</main></body></html>`,{status,headers:{...headers,'Content-Type':'text/html; charset=utf-8'}});}
function json(obj,status=200){return new Response(JSON.stringify(obj),{status,headers:{...headers,'Content-Type':'application/json; charset=utf-8'}});}
function form(input={},error=''){
  const retry=input.retry_key??newKey(),management=input.management_key??newKey();
  const options=['privacy','safety','misattribution','other'].map(kind=>`<option value="${kind}"${kind===(input.kind??'privacy')?' selected':''}>${kind[0].toUpperCase()+kind.slice(1)}</option>`).join('');
  return `${error?`<p role="alert">${esc(error)}</p>`:''}<p>This separate route asks the project to review material that may concern or affect you. It is not an automatic takedown. Ordinary contribution intake may be paused while correction capacity remains available.</p><form method="post" action="/report"><label>Contribution reference<input name="target_id" value="${esc(input.target_id)}" required></label><label>Reason<select name="kind">${options}</select></label><label>Optional note<textarea name="note" rows="4">${esc(input.note)}</textarea></label><input type="hidden" name="retry_key" value="${esc(retry)}"><input type="hidden" name="management_key" value="${esc(management)}"><p>Save both private keys before sending. A stored request is not a takedown, publication decision or project answer.</p><p>Retry key: <code>${esc(retry)}</code><br>Management key: <code>${esc(management)}</code></p><button>Request review</button></form>`;
}
function manage(){return `<h2>Check or manage a correction request</h2><form method="post" action="/report/manage"><label>Correction reference<input name="id" required></label><label>Private management key<input name="management_key" type="password" required autocomplete="off"></label><button name="action" value="receipt">Check status</button><button name="action" value="withdraw">Withdraw pending request</button><button name="action" value="clear_note">Clear my note after resolution</button></form><p>Clearing a note after resolution preserves the fact of the request and the operator outcome; it removes only the reporter-supplied free-text note from the live request record.</p>`;}
async function readInput(request){
  const type=(request.headers.get('content-type')??'').split(';')[0].trim().toLowerCase();
  if(!['application/json','application/x-www-form-urlencoded'].includes(type))throw new Problem(415,'UNSUPPORTED_CONTENT_TYPE');
  const declared=Number(request.headers.get('content-length')??0);if(declared>65536)throw new Problem(413,'REQUEST_TOO_LARGE');
  let size=0;const parts=[],reader=request.body?.getReader();
  if(reader)for(;;){const {done,value}=await reader.read();if(done)break;size+=value.byteLength;if(size>65536){await reader.cancel();throw new Problem(413,'REQUEST_TOO_LARGE');}parts.push(value);}
  const bytes=new Uint8Array(size);let offset=0;for(const p of parts){bytes.set(p,offset);offset+=p.length;}
  let source;try{source=new TextDecoder('utf-8',{fatal:true}).decode(bytes);}catch{throw new Problem(400,'INVALID_UTF8');}
  try{
    if(type==='application/json'){const v=JSON.parse(source);if(!v||Array.isArray(v)||typeof v!=='object')throw 0;return v;}
    const params=new URLSearchParams(source),v={};for(const [k,x] of params){if(Object.hasOwn(v,k))throw 0;Object.defineProperty(v,k,{value:x,enumerable:true});}return v;
  }catch{throw new Problem(400,'INVALID_REQUEST');}
}
async function moderator(request,env){
  const expected=env.ADMIN_TOKEN;if(typeof expected!=='string'||expected.length<32)throw new Problem(503,'MODERATOR_NOT_CONFIGURED');
  const provided=request.headers.get('authorization')?.replace(/^Bearer /,'')??'';
  const a=await sha(expected),b=await sha(provided);let d=0;for(let i=0;i<a.length;i++)d|=a.charCodeAt(i)^b.charCodeAt(i);
  if(d!==0)throw new Problem(401,'MODERATOR_AUTH_REQUIRED');
}

// Caller authenticates first. This only records a review outcome; it does not
// establish that content changed or perform a target-content action.
export async function correctionAdmin(input,env,clock,actor){
  const corrections=new CorrectionStore(env.DB,clock);
  if(input.action==='corrections')return {corrections:await corrections.queue()};
  if(input.action==='resolve-correction')return corrections.resolve(input.id,input,actor);
  throw new Problem(400,'UNKNOWN_CORRECTION_ADMIN_ACTION');
}

export async function handleCorrection(request,env,clock=()=>Date.now()){
  const url=new URL(request.url),browser=!url.pathname.startsWith('/api/');let input;
  try{
    if(env.SYNTHETIC_ONLY!=='true'||!['localhost','127.0.0.1','[::1]'].includes(url.hostname))throw new Problem(503,'LOCAL_SYNTHETIC_PROTOTYPE_ONLY');
    if(url.origin!==env.APP_ORIGIN||url.search)throw new Problem(400,'INVALID_REQUEST_ORIGIN_OR_QUERY');
    if(!env.DB)throw new Problem(503,'STORAGE_UNAVAILABLE');
    if(request.method==='POST'){
      const origin=request.headers.get('origin');if(origin&&origin!==env.APP_ORIGIN)throw new Problem(403,'CROSS_ORIGIN_POST_REFUSED');
      if(['/report','/api/correction'].includes(url.pathname))await edgeAdmission(env,'correction');
      input=await readInput(request);
    }
    const corrections=new CorrectionStore(env.DB,clock);
    if(request.method==='GET'&&url.pathname==='/api/correction-keys')return json({retry_key:newKey(),management_key:newKey()});
    if(request.method==='GET'&&url.pathname==='/report')return page('Request review or removal',form()+manage());
    if(request.method==='POST'&&['/report','/api/correction'].includes(url.pathname)){
      if(typeof env.RATE_SECRET!=='string'||env.RATE_SECRET.length<32)throw new Problem(503,'RATE_LIMIT_NOT_CONFIGURED');
      const clientHash=await sha(env.RATE_SECRET+':local-loopback:correction:'+Math.floor(clock()/86400000));
      const result=await corrections.submit(input,clientHash);
      return browser?page('Correction request stored — no action implied',`<pre>${esc(JSON.stringify(result,null,2))}</pre>${manage()}<p><a href="/">Return</a></p>`):json(result);
    }
    if(request.method==='POST'&&['/report/manage','/api/correction-manage'].includes(url.pathname)){
      let result;if(input.action==='receipt')result=await corrections.receipt(input.id,input.management_key);
      else if(input.action==='withdraw')result=await corrections.withdraw(input.id,input.management_key);
      else if(input.action==='clear_note')result=await corrections.clearNote(input.id,input.management_key);
      else throw new Problem(400,'UNKNOWN_CORRECTION_ACTION');
      return browser?page('Correction request status',`<pre>${esc(JSON.stringify(result,null,2))}</pre>${manage()}<p><a href="/">Return</a></p>`):json(result);
    }
    if(request.method==='POST'&&url.pathname==='/api/admin'){
      await moderator(request,env);const actor='authorised-local-operator';
      return json(await correctionAdmin(input,env,clock,actor));
    }
    throw new Problem(404,'ROUTE_NOT_FOUND');
  }catch(error){
    const status=error instanceof Problem?error.status:503,code=error instanceof Problem?error.code:'STORAGE_OR_SERVICE_FAILURE';
    const notice=code==='STORAGE_OR_SERVICE_FAILURE'?'No confirmed receipt. A write may have committed before the failure. Retry the SAME request and keys rather than assuming nothing was stored.':code;
    if(browser&&url.pathname==='/report'&&input)return page('Correction request not confirmed',form(input,notice)+manage(),status);
    return browser?page('Request not completed',`<p>${esc(notice)}</p><a href="/report">Return</a>`,status):json({error:code,detail:notice},status);
  }
}
