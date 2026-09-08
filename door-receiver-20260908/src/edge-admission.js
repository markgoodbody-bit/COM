import {Problem} from './store.js';

const CONFIG = {
  contribution: {binding: 'CONTRIBUTION_RATE_LIMITER', key: 'psfh:contribution', code: 'CONTRIBUTION_EDGE_RATE_LIMITED'},
  correction: {binding: 'CORRECTION_RATE_LIMITER', key: 'psfh:correction', code: 'CORRECTION_EDGE_RATE_LIMITED'}
};

/**
 * Soft edge admission gate. The key is deliberately route/class based rather than
 * a visitor identity or IP address. D1 transaction caps remain the hard queue/body
 * boundary; this limiter only sheds bursts before the request body is consumed.
 *
 * Local synthetic tests may omit the binding. Any future non-synthetic mode fails
 * closed if a required binding is absent.
 */
export async function edgeAdmission(env, kind) {
  const cfg=CONFIG[kind];
  if(!cfg)throw new Problem(500,'UNKNOWN_EDGE_ADMISSION_KIND');
  const limiter=env[cfg.binding];
  if(!limiter){
    if(env.SYNTHETIC_ONLY==='true')return {enforced:false};
    throw new Problem(503,'EDGE_RATE_LIMIT_NOT_CONFIGURED');
  }
  let result;
  try{result=await limiter.limit({key:cfg.key});}
  catch{throw new Problem(503,'EDGE_RATE_LIMIT_UNAVAILABLE');}
  if(!result||result.success!==true)throw new Problem(429,cfg.code);
  return {enforced:true};
}
