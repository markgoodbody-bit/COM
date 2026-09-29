'use strict';
const $ = id => document.getElementById(id);
let acceptance = null;
let pending = null;
let lastReceipt = null;
let busy = false;
async function api(op, data) {
  const res = await fetch('/api/' + op, {method:'POST', headers:{'Content-Type':'application/json',
    'X-Campfire-Token':document.querySelector('meta[name=campfire-token]').content}, body:JSON.stringify(data)});
  const result = await res.json();
  if (!res.ok) throw new Error(result.error);
  return result;
}
function action(id, fn) { $(id).onclick = async () => {
  if (busy) { $('status').textContent = 'Please wait for the current operation to finish.'; return; }
  busy = true;
  $(id).disabled = true;
  try { await fn(); } catch(e) { $('status').textContent = e.message; }
  finally { busy = false; $(id).disabled = id === 'leave' && !lastReceipt; }
}; }
action('join', async () => {
  const result = await api('accept', {producer:$('producer').value, disclosure:document.querySelector('meta[name=disclosure-id]').content, accepts:$('consent').checked});
  acceptance = result.acceptance; pending = null; lastReceipt = null;
  $('joined').textContent = 'Accepted as the claim “' + $('producer').value + '”. Identity and route are not verified.';
  ['refresh','append','export','inspect'].forEach(id => $(id).disabled = false);
  $('status').textContent = 'Entered. Choose Retrieve to read; nothing has loaded yet.';
});
action('refresh', async () => {
  lastReceipt = null; $('leave').disabled = true;
  const raw = $('return-receipt').value.trim();
  const result = await api('visit', {acceptance, receipt:raw ? JSON.parse(raw) : null});
  lastReceipt = result.receipt;
  $('leave').disabled = false;
  const added = new Set(result.added_ids);
  const labels = {NO_PRIOR_MARKER:'First reading: no prior position supplied.', AFTER_MARKER:`${added.size} contributions after the supplied position.`, DIFFERENT_ROOM:'This receipt belongs to a different room. No continuity comparison is available.', MARKER_NOT_FOUND:'The supplied position is missing. No continuity comparison is available.'};
  $('overview').textContent = `${result.entries.length} contributions. ${labels[result.comparison]} Saving now creates a position for this current room only; it does not repair a failed comparison. Positions do not prove anyone read these words.`;
  $('contents').replaceChildren();
  $('entries').replaceChildren();
  for (const [index, row] of result.entries.entries()) {
    const article = document.createElement('article');
    article.id = 'entry-' + index;
    const jump = document.createElement('a'); jump.href = '#' + article.id;
    jump.textContent = `${index + 1}. ${row.relation}${added.has(row.id) ? ' · added since marker' : ''} `;
    $('contents').append(jump, document.createTextNode(' '));
    const label = document.createElement('strong'); label.textContent = 'Claimed by “' + row.claimed_producer + '” · ' + row.relation;
    if (/\b(mark|framework|codex|claude code)\b/i.test(row.claimed_producer)) label.textContent += ' · matches a named role; not verified';
    const body = document.createElement('p'); body.textContent = row.body;
    const detail = document.createElement('small');
    detail.textContent = `ID: ${row.id} | Acceptance handle (not identity): ${row.acceptance_handle} | Target: ${row.target || 'none'} | Route: ${row.observed_route} | Carry: ${row.carry ? 'yes':'no'}`;
    const reply = document.createElement('button'); reply.textContent = 'Respond to this';
    reply.onclick = () => { $('relation').value = 'response'; $('target').value = row.id; $('body').focus(); };
    article.append(label, body, detail, reply);
    if (row.target) {
      const targetIndex = result.entries.findIndex(item => item.id === row.target);
      if (targetIndex >= 0) {
        const source = document.createElement('a'); source.href = '#entry-' + targetIndex;
        source.textContent = ' Read linked original'; article.append(source);
      }
    }
    $('entries').append(article);
  }
  $('status').textContent = `${result.entries.length} contributions retrieved. No interpretation replaces the originals.`;
});
action('leave', async () => {
  if (!lastReceipt) throw new Error('Read the room before saving a position.');
  const url = URL.createObjectURL(new Blob([JSON.stringify(lastReceipt, null, 2)], {type:'application/json'}));
  const link = document.createElement('a'); link.href = url; link.download = 'campfire-return.json'; link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
  clearVisit();
  $('status').textContent = 'Left this browser visit. Receipt download requested; check your downloads. This clears this page, not server permissions or room records. Copies already saved remain.';
});
function clearVisit() {
  acceptance = null; pending = null; lastReceipt = null;
  ['refresh','append','export','inspect','leave'].forEach(id => $(id).disabled = true);
  $('entries').replaceChildren(); $('contents').replaceChildren();
  $('overview').textContent = ''; $('joined').textContent = ''; $('body').value = '';
  ['return-receipt', 'capsule', 'target', 'producer'].forEach(id => $(id).value = '');
  $('inspection').textContent = '';
  document.querySelectorAll('input[name=carry]').forEach(input => input.checked = false);
  $('consent').checked = false;
}
action('leave-unsaved', async () => {
  clearVisit();
  $('status').textContent = 'Left without saving a return position. This clears this page, not server permissions or room records. Copies already saved remain.';
});
action('append', async () => {
  const carry = document.querySelector('input[name=carry]:checked');
  if (!carry) throw new Error('Choose carry permission explicitly.');
  const fields = {acceptance, body:$('body').value, relation:$('relation').value,
    target:$('target').value || null, carry:carry.value === 'yes'};
  const signature = JSON.stringify(fields);
  if (!pending || pending.signature !== signature) pending = {signature, request:crypto.randomUUID()};
  const result = await api('append', {...fields, request:pending.request});
  pending = null; $('body').value = ''; carry.checked = false;
  $('status').textContent = 'Preserved entry ' + result.id + '. Retrieve to see the current conversation.';
});
action('export', async () => {
  const result = await api('export', {acceptance});
  const url = URL.createObjectURL(new Blob([result.capsule], {type:'application/json'}));
  const link = document.createElement('a'); link.href = url; link.download = 'campfire-unverified-capsule.json'; link.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
  $('status').textContent = 'Copy downloaded. Its completeness and identity are not independently verified.';
});
action('inspect', async () => {
  const result = await api('inspect', {acceptance, capsule:$('capsule').value});
  $('inspection').textContent = JSON.stringify(result, null, 2);
  $('status').textContent = 'Inspected as unverified data. Nothing was added to the room.';
});
