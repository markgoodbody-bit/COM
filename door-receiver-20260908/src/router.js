import {handle as handleContribution} from './handler.js';
import {handleCorrection} from './correction-handler.js';
const DIRECT=new Set(['/report','/report/manage','/api/correction','/api/correction-manage','/api/correction-keys']);
const CORRECTION_ADMIN=new Set(['corrections','resolve-correction']);

export async function handle(request,env,clock=()=>Date.now()){
  const url=new URL(request.url);
  if(DIRECT.has(url.pathname))return handleCorrection(request,env,clock);
  if(request.method==='POST'&&url.pathname==='/api/admin'){
    const type=(request.headers.get('content-type')??'').split(';')[0].trim().toLowerCase();
    if(type==='application/json'){
      try{
        const input=await request.clone().json();
        if(input&&CORRECTION_ADMIN.has(input.action))return handleCorrection(request,env,clock);
      }catch{/* base handler owns malformed non-correction admin requests */}
    }
  }
  return handleContribution(request,env,clock);
}
