import { pathToFileURL } from 'node:url';
import { resolve } from 'node:path';

const LOOPBACK = new Set(['localhost','127.0.0.1','[::1]']);

export class OperatorError extends Error {
  constructor(message, code=1) { super(message); this.code = code; }
}

function receiverUrl(value) {
  const url = new URL(value || 'http://127.0.0.1:8788/');
  if (url.username || url.password || url.search || url.hash)
    throw new OperatorError('OPERATOR_URL_MUST_NOT_CONTAIN_CREDENTIALS_QUERY_OR_FRAGMENT');
  if (url.protocol !== 'https:' && !(url.protocol === 'http:' && LOOPBACK.has(url.hostname)))
    throw new OperatorError('OPERATOR_URL_MUST_BE_HTTPS_OR_LOOPBACK_HTTP');
  url.pathname = '/api/admin';
  return url;
}

async function stdinJson(readStdin) {
  const raw = (await readStdin()).trim();
  if (!raw) throw new OperatorError('JSON_INPUT_REQUIRED');
  let value;
  try { value = JSON.parse(raw); } catch { throw new OperatorError('INVALID_JSON_INPUT'); }
  if (!value || Array.isArray(value) || typeof value !== 'object')
    throw new OperatorError('JSON_OBJECT_REQUIRED');
  return value;
}

function validatePayload(action, input) {
  if (['ready','pause','queue','corrections'].includes(action)) return {action};
  const id = input.id;
  if (typeof id !== 'string' || !id.trim()) throw new OperatorError('ID_REQUIRED');
  if (action === 'resolve-correction') {
    if (!['no_change','content_changed','content_removed','other'].includes(input.outcome))
      throw new OperatorError('VALID_CORRECTION_OUTCOME_REQUIRED');
    if (typeof input.reason !== 'string' || !input.reason.trim()) throw new OperatorError('REASON_REQUIRED');
    return {action,id,outcome:input.outcome,reason:input.reason};
  }
  const revision = input.revision;
  if (!Number.isSafeInteger(revision) || revision < 1) throw new OperatorError('VALID_REVISION_REQUIRED');
  if (action === 'publish' || action === 'decline') {
    if (typeof input.reason !== 'string' || !input.reason.trim()) throw new OperatorError('REASON_REQUIRED');
    return {action,id,revision,reason:input.reason};
  }
  if (action === 'respond') {
    if (typeof input.body !== 'string' || !input.body.trim()) throw new OperatorError('BODY_REQUIRED');
    return {action,id,revision,body:input.body};
  }
  throw new OperatorError('UNKNOWN_OPERATOR_ACTION');
}

export async function runOperator({argv, env, fetchImpl=fetch, readStdin=async()=>'', write=()=>{}}) {
  const action = argv[0];
  if (!action) throw new OperatorError('ACTION_REQUIRED');
  const token = env.PSFH_ADMIN_TOKEN;
  if (typeof token !== 'string' || token.length < 32) throw new OperatorError('PSFH_ADMIN_TOKEN_NOT_CONFIGURED');
  const url = receiverUrl(env.PSFH_OPERATOR_URL);
  const input = ['ready','pause','queue','corrections'].includes(action) ? {} : await stdinJson(readStdin);
  const payload = validatePayload(action,input);
  const response = await fetchImpl(url, {
    method:'POST',
    headers:{'Authorization':`Bearer ${token}`,'Content-Type':'application/json'},
    body:JSON.stringify(payload),
    redirect:'error',
    cache:'no-store'
  });
  const body = await response.text();
  let result;
  try { result = JSON.parse(body); } catch { throw new OperatorError(`NON_JSON_OPERATOR_RESPONSE_${response.status}`); }
  if (!response.ok) throw new OperatorError(`OPERATOR_REQUEST_FAILED_${response.status}_${result.error || 'UNKNOWN'}`);
  write(JSON.stringify(result,null,2)+'\n');
  return result;
}

async function readProcessStdin() {
  const parts=[];
  for await (const chunk of process.stdin) parts.push(chunk);
  return Buffer.concat(parts).toString('utf8');
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  runOperator({argv:process.argv.slice(2), env:process.env, readStdin:readProcessStdin, write:s=>process.stdout.write(s)})
    .catch(error=>{ process.stderr.write(`${error.message}\n`); process.exitCode = error.code || 1; });
}
