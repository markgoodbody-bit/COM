'use strict';
const $ = id => document.getElementById(id);
let acceptance = null;
let pending = null;
async function api(op, data) {
  const res = await fetch('/api/' + op, {method:'POST', headers:{'Content-Type':'application/json',
    'X-Campfire-Token':document.querySelector('meta[name=campfire-token]').content}, body:JSON.stringify(data)});
  const result = await res.json();
  if (!res.ok) throw new Error(result.error);
  return result;
}
function action(id, fn) { $(id).onclick = async () => {
  $(id).disabled = true;
  try { await fn(); } catch(e) { $('status').textContent = e.message; }
  finally { $(id).disabled = false; }
}; }
action('join', async () => {
  const result = await api('accept', {producer:$('producer').value, disclosure:document.querySelector('meta[name=disclosure-id]').content, accepts:$('consent').checked});
  acceptance = result.acceptance; pending = null;
  $('joined').textContent = 'Accepted as the claim “' + $('producer').value + '”. Identity and route are not verified.';
  ['refresh','append','export','inspect'].forEach(id => $(id).disabled = false);
  $('status').textContent = 'Entered. Choose Retrieve to read; nothing has loaded yet.';
});
action('refresh', async () => {
  const result = await api('read', {acceptance});
  $('entries').replaceChildren();
  for (const row of result.entries) {
    const article = document.createElement('article');
    const label = document.createElement('strong'); label.textContent = 'Claimed by “' + row.claimed_producer + '” · ' + row.relation;
    if (/\b(mark|framework|codex|claude code)\b/i.test(row.claimed_producer)) label.textContent += ' · matches a named role; not verified';
    const body = document.createElement('p'); body.textContent = row.body;
    const detail = document.createElement('small');
    detail.textContent = `ID: ${row.id} | Acceptance handle (not identity): ${row.acceptance_handle} | Target: ${row.target || 'none'} | Route: ${row.observed_route} | Carry: ${row.carry ? 'yes':'no'}`;
    article.append(label, body, detail); $('entries').append(article);
  }
  $('status').textContent = `${result.entries.length} contributions retrieved. No interpretation replaces the originals.`;
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
