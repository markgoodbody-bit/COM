'use strict';
const { test } = require('node:test');
const assert = require('node:assert/strict');
const { validateCase, parseCase, encodeCase, makeCase } = require('./../case_intake.js');

// The companion case_card.py validator rejects ASCII controls other than TAB and LF.
// Do not silently turn an author-supplied CR into an invented line break.
const base = () => ({
  title: 'Shared lift report',
  claims: [{ kind: 'change', text: 'Lift changed service', evidence: 'reported' }]
});
const cases = [
  ['title', d => { d.title = 'Before\rAfter'; }],
  ['claim text', d => { d.claims[0].text = 'Before\rAfter'; }],
  ['source', d => { d.claims[0].source = 'Before\rAfter'; }],
  ['party boundary', d => { d.parties = [{ name: 'Tenant', boundary: 'Before\rAfter' }]; }],
  ['possibility condition', d => { d.possibilities = [{party: 'Tenant', description: 'Ask', state: 'possible', condition: 'Before\rAfter'}]; }],
  ['correction clock basis', d => { d.correction = { clock_basis: 'Before\rAfter' }; }],
  ['return unresolved', d => { d.return = { unresolved: 'Before\rAfter' }; }]
];
for (const [field, mutate] of cases) {
  test('reject imported and exported carriage return in ' + field, () => {
    const data = base(); mutate(data);
    assert.throws(() => validateCase(data), /contains control characters/);
    assert.throws(() => parseCase(JSON.stringify(data)), /contains control characters/);
    assert.throws(() => encodeCase(data), /contains control characters/);
  });
}
test('leave authored line feed and tab unchanged', () => {
  const data = base();
  data.title = 'Before\nAfter';
  data.claims[0].text = 'Line\tname';
  const wire = encodeCase(data);
  assert.equal(parseCase(wire).title, 'Before\nAfter');
  assert.equal(parseCase(wire).claims[0].text, 'Line\tname');
});
test('makeCase also refuses carriage return rather than normalizing text', () => {
  const data = base();
  data.claims[0].text = 'Before\rAfter';
  assert.throws(() => makeCase(data), /contains control characters/);
});
