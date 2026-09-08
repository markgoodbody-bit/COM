import { Store, newKey, Problem } from '../door-receiver-20260908/src/store.js';
import { handle } from '../door-receiver-20260908/src/handler.js';
import { lostAcknowledgement } from './lost-ack-test';

function check(value: unknown, label: string): asserts value {
  if (!value) throw Error(label);
}
async function refused(work: () => Promise<unknown>, code: string) {
  try { await work(); } catch (error) {
    check(error instanceof Problem && error.code === code, 'wrong failure: ' + code);
    return;
  }
  throw Error('unexpected success: ' + code);
}

// Test runner only. Never deploy. No user text, keys or URLs are accepted.
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    if (url.hostname !== '127.0.0.1' || url.search || request.headers.has('origin') ||
        request.method !== 'POST' || !['/run', '/lost-ack'].includes(url.pathname) ||
        request.headers.get('X-PSFH-Evaluation') !== 'synthetic-only')
      return new Response('Local evaluation only', { status: 403 });
    if (url.pathname === '/lost-ack') return lostAcknowledgement(env);
    const store = new Store(env.DB);
    const passed: string[] = [];
    let id: string | undefined;
    try {
      const guard = await handle(new Request('https://example.invalid/api/posts'), {
        DB: env.DB, SYNTHETIC_ONLY: 'true', APP_ORIGIN: 'https://example.invalid'
      });
      check(guard.status === 503 && (await guard.json() as {error: string}).error === 'LOCAL_SYNTHETIC_PROTOTYPE_ONLY', 'public guard');
      passed.push('original non-loopback guard retained');
      await store.readiness(false);
      const input = { body: 'SYNTHETIC remote-binding lifecycle', display_name: 'Synthetic fixture', retry_key: newKey(), management_key: newKey() };
      const client = 'synthetic-binding-' + crypto.randomUUID();
      await refused(() => store.submit(input, client), 'INTAKE_PAUSED');
      passed.push('paused new intake refused');
      await store.readiness(true);
      const first = await store.submit(input, client); id = first.id;
      const fresh = new Store(env.DB);
      check((await fresh.receipt(id, input.management_key)).body === input.body, 'fresh binding read');
      passed.push('stored receipt read through fresh Store');
      await store.readiness(false);
      check((await store.submit(input, client)).id === id, 'retry identity');
      check((await store.first('SELECT COUNT(*) AS n FROM contributions WHERE id=?', id)).n === 1, 'no duplicate');
      await refused(() => store.submit({...input, body: 'different'}, client), 'RETRY_CONTENT_CONFLICT');
      passed.push('same retry recovers while paused; changed retry refused');
      check(!(await store.publicItems()).some(row => row.id === id), 'pending privacy');
      await store.moderate(id, {action: 'publish', revision: 1, reason: 'Synthetic review'}, 'synthetic-operator');
      await store.respond(id, {revision: 1, body: 'Synthetic separate response'}, 'synthetic-operator');
      check((await store.publicItems()).find(row => row.id === id)?.responses.length === 1, 'separate response');
      passed.push('private pending, reviewed publication, separate response');
      const replacement = await store.revise(id, input.management_key, {revision: 1, body: 'Synthetic replacement', display_name: ''});
      check(replacement.revision === 2 && replacement.state === 'pending', 'revision state');
      check(!(await store.publicItems()).some(row => row.id === id), 'replacement unpublishes');
      check((await store.rows('SELECT id FROM responses WHERE contribution_id=?', id)).length === 0, 'old response removed');
      await refused(() => store.moderate(id, {action: 'publish', revision: 1, reason: 'Stale'}, 'synthetic-operator'), 'MODERATION_STATE_CONFLICT');
      passed.push('replacement requires fresh review; stale approval refused');
      const before = await store.rows('SELECT action FROM events WHERE contribution_id=? ORDER BY id', id);
      // Fail the event write in the real Store.moderate batch, not a mock batch.
      await env.DB.prepare("CREATE TRIGGER eval_reject_decline BEFORE INSERT ON events WHEN NEW.action='decline' BEGIN SELECT RAISE(ABORT,'SYNTHETIC_AUDIT_FAILURE'); END").run();
      let auditFailed = false;
      try { await store.moderate(id, {action:'decline', revision:2, reason:'Synthetic rollback'}, 'synthetic-operator'); }
      catch (error) { check(String(error).includes('SYNTHETIC_AUDIT_FAILURE'), 'wrong audit failure'); auditFailed = true; }
      finally { await env.DB.prepare('DROP TRIGGER eval_reject_decline').run(); }
      check(auditFailed, 'audit failure missing');
      check((await store.receipt(id, input.management_key)).state === 'pending', 'state rollback');
      check(JSON.stringify(await store.rows('SELECT action FROM events WHERE contribution_id=? ORDER BY id', id)) === JSON.stringify(before), 'audit rollback');
      passed.push('actual moderation batch rolls state and audit back together');
      await store.moderate(id, {action:'decline',revision:2,reason:'Synthetic decline'}, 'synthetic-operator');
      await store.reconsider(id, input.management_key, 'Synthetic reconsideration');
      await store.moderate(id, {action:'publish',revision:2,reason:'Synthetic reconsidered review'}, 'synthetic-operator');
      await store.withdraw(id, input.management_key);
      await refused(() => store.moderate(id, {action:'publish',revision:2,reason:'Stale after withdrawal'}, 'synthetic-operator'), 'MODERATION_STATE_CONFLICT');
      const last = await store.receipt(id, input.management_key);
      check(last.state === 'withdrawn' && last.body === null, 'withdrawal');
      check(!(await store.publicItems()).some(row => row.id === id), 'withdrawn public');
      const actions = (await store.rows('SELECT action FROM events WHERE contribution_id=? ORDER BY id', id)).map(row => row.action);
      check(JSON.stringify(actions) === JSON.stringify(['received','publish','revised','decline','reconsideration','publish','withdrawn']), 'exact audit events');
      passed.push('decline/reconsider/publish/withdraw and exact seven-event audit');
      return Response.json({status:'PASS', source:'f06967a103d9f5c952b10bce56c00b0e88acc49f', id, passed, actions, limits:'Local workerd with remote D1 binding; not deployed HTTP service, crash durability or physical erasure.'});
    } catch (error) {
      return Response.json({status:'FAIL',id,passed,error:String(error)}, {status:500});
    } finally {
      await store.readiness(false);
    }
  }
} satisfies ExportedHandler<Env>;
