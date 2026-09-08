import { Store, newKey, sha } from '../door-receiver-20260908/src/store.js';
import { handle } from '../door-receiver-20260908/src/handler.js';

// Fault only the acknowledgement AFTER the actual remote INSERT resolves.
// No receiver implementation is replaced, and no credentials leave this request.
export async function lostAcknowledgement(env: Env): Promise<Response> {
  const store = new Store(env.DB);
  let injected = false;
  let id: string | undefined;
  const keys = { retry_key: newKey(), management_key: newKey() };
  function wrap(statement: D1PreparedStatement, sql: string): D1PreparedStatement {
    return new Proxy(statement, {get(target, property) {
      if (property === 'bind') return (...args: unknown[]) => wrap(target.bind(...args), sql);
      if (property === 'run') return async () => {
        const result = await target.run();
        if (!injected && /^INSERT INTO contributions\b/.test(sql)) {
          injected = true; throw Error('SYNTHETIC_LOST_ACK_AFTER_REMOTE_COMMIT');
        }
        return result;
      };
      const value = Reflect.get(target, property, target);
      return typeof value === 'function' ? value.bind(target) : value;
    }});
  }
  const db = new Proxy(env.DB, {get(target, property) {
    if (property === 'prepare') return (sql: string) => wrap(target.prepare(sql), sql);
    const value = Reflect.get(target, property, target);
    return typeof value === 'function' ? value.bind(target) : value;
  }});
  const settings = {SYNTHETIC_ONLY:'true',APP_ORIGIN:'http://127.0.0.1:8791',RATE_SECRET:newKey(),ADMIN_TOKEN:newKey()};
  const input = {...keys,body:'SYNTHETIC uncertain acknowledgement',display_name:''};
  const request = () => new Request(settings.APP_ORIGIN + '/api/submit', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(input)});
  try {
    await store.readiness(true);
    const failed = await handle(request(), {...settings,DB:db});
    const failure = await failed.json() as {error: string};
    if (!injected || failed.status !== 503 || failure.error !== 'STORAGE_OR_SERVICE_FAILURE') throw Error('wrong injected failure');
    const row = await store.first('SELECT id FROM contributions WHERE retry_hash=?', await sha(keys.retry_key));
    if (!row) throw Error('remote write did not survive lost acknowledgement');
    id = row.id;
    await store.readiness(false);
    const recovered = await handle(request(), {...settings,DB:env.DB});
    const receipt = await recovered.json() as {id: string; state: string};
    if (recovered.status !== 200 || receipt.id !== id || receipt.state !== 'pending') throw Error('retry did not recover original');
    const count = await store.first('SELECT COUNT(*) AS n FROM contributions WHERE retry_hash=?', await sha(keys.retry_key));
    if (count.n !== 1) throw Error('retry duplicated contribution');
    const publicResponse = await handle(new Request(settings.APP_ORIGIN + '/api/posts'), {...settings,DB:env.DB});
    const publicText = await publicResponse.text();
    if (publicText.includes(id) || publicText.includes(keys.management_key) || publicText.includes(keys.retry_key)) throw Error('private material leaked');
    return Response.json({status:'PASS',id,injected_after_remote_commit:true,error_status:503,retry_status:200,stored_rows:count.n,limits:'Injected acknowledgement loss; not a real network outage or provider disaster-recovery test.'});
  } catch (error) {
    return Response.json({status:'FAIL',id,error:String(error)}, {status:500});
  } finally {
    await store.readiness(false);
    if (id) await store.withdraw(id,keys.management_key);
  }
}
