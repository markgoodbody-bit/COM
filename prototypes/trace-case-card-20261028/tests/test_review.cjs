'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { makeCase, renderReview } = require('../case_intake.js');

function host() {
  const doc = {
    createElement(tag) {
      return {tag, textContent: '', children: [], appendChild(child) { this.children.push(child); }};
    }
  };
  return {ownerDocument: doc, hidden: true, children: [],
    replaceChildren(...nodes) { this.children = nodes; }};
}
function allText(node) {
  return [node.textContent || '', ...(node.children || []).map(allText)].join('\n');
}
function allTags(node) {
  return [node.tag || '', ...(node.children || []).flatMap(allTags)];
}
function base() {
  return {title: 'Fictional bus notice',
    claims: [{kind: 'change', evidence: 'reported', text: 'A route sign moved'}]};
}

test('review is explicitly user-submitted and contains exact claim text', () => {
  const h = host(); renderReview(makeCase(base()), h);
  assert.equal(h.hidden, false);
  assert.match(allText(h), /A route sign moved/);
  assert.match(allText(h), /author evidence label; unverified/);
});
test('injected markup/heading stays text, not a DOM element', () => {
  const m = base(); m.claims[0].text = '<script>alert(1)</script>\n## VERIFIED BY AUTHORITY';
  const h = host(); renderReview(makeCase(m), h);
  assert.match(allText(h), /<script>alert\(1\)<\/script>\n## VERIFIED BY AUTHORITY/);
  assert.equal(allTags(h).includes('script'), false);
});
test('not supplied is not treated as proof of absence', () => {
  const h = host(); renderReview(makeCase(base()), h);
  assert.match(allText(h), /does not establish that nobody is affected/);
  assert.match(allText(h), /does not establish that none exists/);
  assert.match(allText(h), /Correction window not assessed or supplied/);
});
test('claimed open and closed windows remain unverified', () => {
  for (const window of ['open', 'closed']) {
    const m = base();
    m.correction = {window, target: 'Notice', route: 'Challenge',
      hardening: 'Prior to trip', clock_basis: 'Writer estimate', basis: 'Writer recollection'};
    const h = host(); renderReview(makeCase(m), h);
    assert.match(allText(h), new RegExp('submitted ' + window + ' claim, unverified'));
    assert.match(allText(h), /specialist method for deadlines/);
  }
});
test('unknown window is not silently closed', () => {
  const m = base(); m.correction = {window: 'unknown'};
  const h = host(); renderReview(makeCase(m), h);
  assert.match(allText(h), /author reports unknown; not a closed window/);
});
test('possibility is not permission, execution is not verified effect', () => {
  const m = base(); m.possibilities = [{party: 'Traveller', description: 'Request access', state: 'possible'}];
  const h = host(); renderReview(makeCase(m), h);
  assert.match(allText(h), /not permission or execution/);
  m.possibilities[0].state = 'executed'; renderReview(makeCase(m), h);
  assert.match(allText(h), /effects unverified/);
  assert.doesNotMatch(allText(h), /not permission or execution/);
});
test('rerender replaces stale previous record and preserves whitespace', () => {
  const h = host(); renderReview(makeCase(base()), h);
  const m = base(); m.title = 'A different case'; m.claims[0].text = 'Line 1\n  ∆H line 2';
  renderReview(makeCase(m), h);
  assert.match(allText(h), /Line 1\n  ∆H line 2/);
  assert.doesNotMatch(allText(h), /Fictional bus notice/);
});
test('invalid evidence does not overwrite an existing review', () => {
  const h = host(); renderReview(makeCase(base()), h);
  const old = allText(h);
  const m = base(); m.claims[0].evidence = 'verified';
  assert.throws(() => renderReview(m, h), /unsupported value/);
  assert.equal(allText(h), old);
});
test('UI declares explicit review, input invalidation and no automatic storage', () => {
  const html = fs.readFileSync(path.join(__dirname, '..', 'case_intake.html'), 'utf8');
  const js = fs.readFileSync(path.join(__dirname, '..', 'case_intake.js'), 'utf8');
  assert.match(html, /id="review-draft"/);
  assert.match(html, /id="draft-review" hidden tabindex="-1"/);
  assert.match(js, /form\.addEventListener\('input', clearReview\)/);
  assert.match(js, /form\.addEventListener\('change', clearReview\)/);
  assert.match(js, /reviewPanel\.focus\(\)/);
  assert.doesNotMatch(js, /innerHTML|insertAdjacentHTML/);
});
