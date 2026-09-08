import { Store, newKey, sha } from '../door-receiver-20260908/src/store.js';
import { handle } from '../door-receiver-20260908/src/handler.js';

function check(value: unknown, label: string): asserts value {
  if (!value) throw Error(label);
}
function object(value: unknown): Record<string, unknown> {
  check(value !== null && typeof value === 'object' && !Array.isArray(value), 'expected JSON object');
  return Object.fromEntries(Object.entries(value));
}

// Synthetic recipe only. Caller cannot supply content, keys, actions or targets.
export async function receiptResponseEvaluation(env: Env): Promise<Response> {
  const store = new Store(env.DB);
  const settings = { DB: env.DB, SYNTHETIC_ONLY: 'true', APP_ORIGIN: 'http://127.0.0.1:8791',
    ADMIN_TOKEN: newKey(), RATE_SECRET: newKey() };
  const input = { body: 'SYNTHETIC private answer lookup', display_name: '',
    retry_key: newKey(), management_key: newKey() };
  const passed: string[] = [];
  let id: string | undefined;
  let failure: string | undefined;
  let cleanupAllowed = false;
  async function call(path: string, body: Record<string, unknown>, admin = false) {
    const headers: Record<string, string> = { 'Content-Type': 'application/json' };
    if (admin) headers.Authorization = 'Bearer ' + settings.ADMIN_TOKEN;
    const response = await handle(new Request(settings.APP_ORIGIN + path, {
      method: 'POST', headers, body: JSON.stringify(body)
    }), settings);
    return { status: response.status, body: object(await response.json()) };
  }
  async function receipt() {
    const result = await call('/api/manage', { action: 'receipt', id, management_key: input.management_key });
    check(result.status === 200, 'owner receipt status');
    return result.body;
  }
  async function publishAndAnswer(revision: number, body: string) {
    check((await call('/api/admin', { action: 'publish', id, revision, reason: 'SYNTHETIC review' }, true)).status === 200, 'publication');
    check((await call('/api/admin', { action: 'respond', id, revision, body }, true)).status === 200, 'answer');
  }
  function exactAnswer(view: Record<string, unknown>, body: string) {
    check(Array.isArray(view.responses) && view.responses.length === 1, 'one current answer');
    const answer = object(view.responses[0]);
    check(answer.body === body && answer.actor === 'authorised-local-operator' &&
      typeof answer.created_at === 'number' && Number.isSafeInteger(answer.created_at), 'answer body, attribution and timestamp');
    check(Object.keys(answer).sort().join(',') === 'actor,body,created_at', 'bounded answer fields');
  }
  try {
    const initial = await store.first('SELECT enabled,ready_until FROM service WHERE id=1');
    check(initial?.enabled === 0 && initial?.ready_until === 0, 'evaluation must start paused');
    cleanupAllowed = true;
    check((await call('/api/admin', { action: 'ready' }, true)).status === 200, 'synthetic readiness');
    const submitted = await call('/api/submit', input);
    check(submitted.status === 200 && typeof submitted.body.id === 'string', 'synthetic submission');
    id = submitted.body.id;
    check((await call('/api/admin', { action: 'pause' }, true)).status === 200, 'pause after submission');
    await publishAndAnswer(1, 'SYNTHETIC first answer');
    exactAnswer(await receipt(), 'SYNTHETIC first answer');
    passed.push('owner receipt returns one separately attributed current answer');
    const wrong = await call('/api/manage', { action: 'receipt', id, management_key: newKey() });
    check(wrong.status === 404 && wrong.body.error === 'RECEIPT_UNAVAILABLE' && !('responses' in wrong.body), 'wrong owner must not see answer');
    passed.push('wrong management key refused without response disclosure');
    const revised = await call('/api/manage', { action: 'revise', id, management_key: input.management_key,
      revision: 1, body: 'SYNTHETIC replacement', display_name: '' });
    check(revised.status === 200, 'replacement');
    const pending = await receipt();
    check(pending.state === 'pending' && pending.revision === 2 && Array.isArray(pending.responses) && pending.responses.length === 0, 'replacement hides old answer');
    await publishAndAnswer(2, 'SYNTHETIC second answer');
    exactAnswer(await receipt(), 'SYNTHETIC second answer');
    passed.push('replacement hides old answer; fresh publication exposes only new answer');
    check((await call('/api/manage', { action: 'withdraw', id, management_key: input.management_key })).status === 200, 'withdrawal');
    const withdrawn = await receipt();
    check(withdrawn.state === 'withdrawn' && withdrawn.body === null && Array.isArray(withdrawn.responses) && withdrawn.responses.length === 0, 'withdrawal hides answer and body');
    check(!(await store.publicItems()).some((row: { id: string }) => row.id === id), 'withdrawn item absent from public view');
    passed.push('withdrawal removes answer and body from receipt and public view');
  } catch (error) { failure = String(error); }
  finally {
    if (cleanupAllowed) {
      try {
        await store.readiness(false);
        // Recover the synthetic target even if submission committed without acknowledgement.
        const row = await store.first('SELECT id FROM contributions WHERE retry_hash=?', await sha(input.retry_key));
        if (row) { id = row.id; await store.withdraw(row.id, input.management_key); }
        const state = await store.first('SELECT enabled,ready_until FROM service WHERE id=1');
        check(state.enabled === 0 && state.ready_until === 0, 'cleanup paused');
        if (id) check((await store.rows('SELECT id FROM responses WHERE contribution_id=?', id)).length === 0, 'cleanup no retained answers');
      } catch (error) { failure = (failure ? failure + '; ' : '') + 'cleanup: ' + String(error); }
    }
  }
  return Response.json({ status: failure ? 'FAIL' : 'PASS', id, passed, ...(failure ? { error: failure } : {}),
    limits: 'Local workerd with existing remote D1; synthetic sequential calls, not deployed HTTP, concurrent-race or physical-erasure evidence.' }, { status: failure ? 500 : 200 });
}
