import {handle as handleContribution} from './handler.js';
import {handleCorrection} from './correction-handler.js';
const DIRECT=new Set(['/report','/report/manage','/api/correction','/api/correction-manage','/api/correction-keys']);

export async function handle(request,env,clock=()=>Date.now()){
  const url=new URL(request.url);
  if(DIRECT.has(url.pathname))return handleCorrection(request,env,clock);
  // Admin dispatch happens only after the contribution handler's bounded read
  // and authentication. Do not sniff an unbounded cloned JSON body here.
  return handleContribution(request,env,clock);
}
