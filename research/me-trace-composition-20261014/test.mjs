import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {check,inspect} from './check.mjs';
const original=JSON.parse(readFileSync(new URL('./examples.json',import.meta.url),'utf8'));
const copy=()=>structuredClone(original);

test('three declared compositions discriminate unknown staleness without world approval',()=>{
  const results=check(original);
  assert.deepEqual(results.map(r=>r.status),['PREMISES_RECORDED_NOT_VERIFIED','PREMISES_RECORDED_NOT_VERIFIED','INCOMPLETE']);
  assert.deepEqual(results[2].missing,['relevant_change','warrant_gap']);
  assert.ok(results.every(r=>r.world_truth==='NOT_CHECKED' && r.ethical_approval==='NOT_COMPUTED' && !r.actuation));
});
test('practice without transfer/retention cannot earn recorded formation dependencies',()=>{
  const p=copy();delete p.examples[0].premises.transfer;p.examples[0].premises.retention.status='UNKNOWN';
  assert.deepEqual(check(p)[0].missing,['transfer','retention']);
});
test('joint skill inventory without route/permission/maintainers cannot earn prospect dependencies',()=>{
  const p=copy();for(const name of ['joint_route','authority','maintenance']) p.examples[1].premises[name].status='UNKNOWN';
  assert.deepEqual(check(p)[1].missing,['joint_route','authority','maintenance']);
});
test('elapsed time alone still cannot make stale-account premises complete',()=>{
  const p=copy();p.examples[2].premises.account_time.proposition='Recorded one hundred years ago.';
  assert.equal(check(p)[2].status,'INCOMPLETE');
});
test('mis-typed moral output, hidden value decision and unsupported rule are refused',()=>{
  const p=copy();p.examples[0].output_kind='ETHICALLY_GOOD';assert.throws(()=>check(p),/OUTPUT/);
  const q=copy();q.examples[1].value_binding.expression_type='CONDITIONAL_INFERENCE';assert.throws(()=>check(q),/VALUE/);
  const r=copy();r.examples[0].check='moral_score';assert.throws(()=>check(r),/UNKNOWN/);
});
test('source/STOP consistency tests do not fetch or adjudicate source/world claims',()=>{
  assert.equal(original.sources.ME08.commit,'e2ef746e931161cb70ac46a4eaa122442134e86b');
  assert.equal(original.sources.TRACE04.blob,'fe67f4e931ebbf00456652ef33923dc1a391dd9b');
  assert.equal(original.sources.PR73.commit,'12fd57a322130cf40ca8c71888fa89315635235f');
  const p=copy();p.examples[0].source_refs=['imaginary'];assert.throws(()=>check(p),/SOURCE/);
  const q=copy();q.handoff.actuation_authorised=true;assert.throws(()=>check(q),/HANDOFF/);
  const r=copy();r.sources.TRACE04.commit='latest';assert.throws(()=>check(r),/PIN/);
});
test('known ceiling: a consistent invented lie still passes declarations, not reality',()=>{
  const p=copy();p.examples[0].premises.transfer.proposition='False assertion supplied with the expected label.';
  assert.equal(inspect(p.examples[0],p.sources).status,'PREMISES_RECORDED_NOT_VERIFIED');
  assert.equal(inspect(p.examples[0],p.sources).world_truth,'NOT_CHECKED');
});
