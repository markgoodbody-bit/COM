// Checks declared example dependencies ONLY. No network, world judgement or actuation.
import {readFileSync} from 'node:fs';
import {pathToFileURL} from 'node:url';
export const requirements = Object.freeze({
  retained_skill:['baseline','observation','practice_feedback','transfer','retention','maintenance','agency'],
  collective_prospect:['baseline','joint_route','actors','authority','maintenance','agency','burden'],
  stale_account:['account_time','intended_use','relevant_change','warrant_gap'],
});
const states=new Set(['ASSUMED_FOR_EXAMPLE','OBSERVED','REPORTED','INFERRED','UNKNOWN','DISPUTED']);
const types=new Set(['DEFINITION','NON_IDENTITY_REMINDER','CONDITIONAL_INFERENCE','NECESSARY_TIMING_CLAIM','UNRESOLVED_VALUE_CHOICE']);
export function inspect(example, sources) {
  if(!types.has(example.expression_type) || !Object.hasOwn(requirements,example.check)) throw Error('UNKNOWN_EXPRESSION_OR_RULE');
  if(example.expression_type !== 'CONDITIONAL_INFERENCE') throw Error('RULE_REQUIRES_CONDITIONAL_TYPE');
  if(!Array.isArray(example.source_refs) || !example.source_refs.length ||
     example.source_refs.some(ref=>!Object.hasOwn(sources,ref))) throw Error('SOURCE_REFERENCE_UNKNOWN');
  if(!example.scope || !example.claim || !['DESCRIPTIVE','DESCRIPTIVE_PROSPECT'].includes(example.output_kind)) throw Error('CLAIM_SCOPE_OR_OUTPUT_UNKNOWN');
  const missing=[];
  for(const key of requirements[example.check]) {
    const p=example.premises?.[key];
    if(p && (!states.has(p.status) || !p.proposition)) throw Error('INVALID_PREMISE_DECLARATION');
    if(!p || ['UNKNOWN','DISPUTED'].includes(p.status)) missing.push(key);
  }
  if(example.value_binding && (example.value_binding.expression_type !== 'UNRESOLVED_VALUE_CHOICE' ||
     !example.value_binding.source || !example.value_binding.decision)) throw Error('VALUE_NOT_EXPOSED_AS_CHOICE');
  return {id:example.id,status:missing.length?'INCOMPLETE':'PREMISES_RECORDED_NOT_VERIFIED',missing,
    world_truth:'NOT_CHECKED',ethical_approval:'NOT_COMPUTED',actuation:false};
}
export function check(packet) {
  if(packet.format !== 'off-book-composition-research/0.1') throw Error('UNKNOWN_FORMAT');
  for(const source of Object.values(packet.sources)) {
    if(!/^[a-f0-9]{40}$/.test(source.commit) || !/^[a-f0-9]{40}$/.test(source.blob) || !source.path || !source.repo) throw Error('SOURCE_PIN_INCOMPLETE');
  }
  if(new Set(packet.examples.map(x=>x.id)).size !== packet.examples.length) throw Error('DUPLICATE_EXAMPLE');
  if(packet.handoff.status !== 'STOP_HANDOFF' || packet.handoff.actuation_authorised !== false ||
     !packet.handoff.owner || !packet.handoff.reason) throw Error('HANDOFF_NOT_PRESERVED');
  return packet.examples.map(e=>inspect(e,packet.sources));
}
if(process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const packet=JSON.parse(readFileSync(new URL('./examples.json',import.meta.url),'utf8'));
  console.log(JSON.stringify({ceiling:packet.ceiling,results:check(packet),handoff:packet.handoff},null,2));
}
