/* Independent, offline case-card intake. Author labels are claims, not proof. */
(function (root) {
  'use strict';

  const LIMIT_BYTES = 131072;
  const LIMIT_ROWS = 24;
  const LIMIT_FIELD = 2000;
  const KINDS = ['baseline', 'change', 'consequence'];
  const EVIDENCE = ['observed', 'reported', 'inferred', 'disputed', 'unknown'];
  const STATES = ['possible', 'offered', 'permitted', 'chosen', 'attempted', 'executed'];
  const WINDOWS = ['not_assessed', 'unknown', 'open', 'closed'];
  const ALLOWED = {
    case: ['title', 'scope', 'claims', 'parties', 'possibilities', 'correction', 'return'],
    claim: ['kind', 'text', 'evidence', 'source'],
    party: ['name', 'aim', 'boundary'],
    possibility: ['party', 'description', 'state', 'condition'],
    correction: ['target', 'route', 'hardening', 'clock_basis', 'window', 'basis'],
    return: ['learned', 'unresolved', 'next']
  };

  function fail(message) { throw new Error(message); }
  function byteCount(input) { return new TextEncoder().encode(input).length; }
  function checkObject(value, key) {
    if (!value || typeof value !== 'object' || Array.isArray(value)) fail(key + ' must be an object');
    for (const field of Object.keys(value)) {
      if (!ALLOWED[key].includes(field)) fail(key + ' has unexpected keys');
    }
    return value;
  }
  function checkString(value, label, max, required) {
    if (value === undefined && !required) return undefined;
    if (typeof value !== 'string' || !value.replace(/\u0085/g, '').trim()) fail(label + ' must be nonempty text');
    if (Array.from(value).length > max) fail(label + ' is too long');
    if (/[\u202a-\u202e\u2066-\u2069\u200e\u200f\u061c]/u.test(value)) fail(label + ' contains directional format controls');
    if (/[\u0000-\u0008\u000b\u000c\u000e-\u001f]/u.test(value)) fail(label + ' contains control characters');
    for (let i = 0; i < value.length; i++) {
      const code = value.charCodeAt(i);
      if (code >= 0xd800 && code <= 0xdbff) {
        const next = value.charCodeAt(i + 1);
        if (!(next >= 0xdc00 && next <= 0xdfff)) fail(label + ' contains invalid surrogate');
        i++;
      } else if (code >= 0xdc00 && code <= 0xdfff) fail(label + ' contains invalid surrogate');
    }
    return value;
  }
  function checkEnum(value, label, allowed) {
    checkString(value, label, 40, true);
    if (!allowed.includes(value)) fail(label + ' has unsupported value');
  }
  function checkRows(data, key, kind, required) {
    if (data[key] === undefined && !required) return;
    const rows = data[key];
    if (!Array.isArray(rows) || rows.length > LIMIT_ROWS || (required && !rows.length)) fail(key + ' must be a bounded list');
    for (const row of rows) {
      checkObject(row, kind);
      if (kind === 'claim') {
        checkEnum(row.kind, 'claim.kind', KINDS);
        checkString(row.text, 'claim.text', LIMIT_FIELD, true);
        checkEnum(row.evidence, 'claim.evidence', EVIDENCE);
        checkString(row.source, 'claim.source', 500, false);
      } else if (kind === 'party') {
        checkString(row.name, 'party.name', 150, true);
        checkString(row.aim, 'party.aim', 500, false);
        checkString(row.boundary, 'party.boundary', 500, false);
      } else {
        checkString(row.party, 'possibility.party', 150, true);
        checkString(row.description, 'possibility.description', 1000, true);
        checkEnum(row.state, 'possibility.state', STATES);
        checkString(row.condition, 'possibility.condition', 500, false);
      }
    }
  }
  function validateCase(data) {
    checkObject(data, 'case');
    checkString(data.title, 'case.title', 180, true);
    checkString(data.scope, 'case.scope', 500, false);
    checkRows(data, 'claims', 'claim', true);
    if (!data.claims.some(c => c.kind === 'change')) fail('a change claim is required');
    checkRows(data, 'parties', 'party', false);
    checkRows(data, 'possibilities', 'possibility', false);
    if (data.correction !== undefined) {
      const c = checkObject(data.correction, 'correction');
      for (const key of ['target', 'route', 'hardening', 'clock_basis', 'basis']) {
        checkString(c[key], 'correction.' + key, 500, false);
      }
      if (c.window !== undefined) checkEnum(c.window, 'correction.window', WINDOWS);
      if (['open', 'closed'].includes(c.window) && !['target', 'route', 'hardening', 'clock_basis', 'basis'].every(k => c[k])) {
        fail('open/closed correction window requires target, route, hardening, clock_basis and basis');
      }
    }
    if (data.return !== undefined) {
      const r = checkObject(data.return, 'return');
      for (const key of ['learned', 'unresolved', 'next']) checkString(r[key], 'return.' + key, 1000, false);
    }
    if (byteCount(JSON.stringify(data)) > LIMIT_BYTES) fail('case exceeds 128 KiB');
    return data;
  }
  function pick(row, keyList) {
    const out = {};
    for (const key of keyList) {
      const value = row[key];
      if (value !== undefined && value !== '') out[key] = value;
    }
    return out;
  }
  function isBlankRow(row) { return Object.values(row).every(x => x === ''); }
  function makeCase(model) {
    checkObject(model, 'case');
    const out = pick(model, ['title', 'scope']);
    if (!Array.isArray(model.claims)) fail('claims must be a bounded list');
    out.claims = model.claims.filter(row => { checkObject(row, 'claim'); return !isBlankRow(row); }).map(row => {
      return pick(row, ALLOWED.claim);
    });
    for (const [key, kind] of [['parties', 'party'], ['possibilities', 'possibility']]) {
      if (model[key] === undefined) continue;
      if (!Array.isArray(model[key])) fail(key + ' must be a bounded list');
      const rows = model[key].filter(row => { checkObject(row, kind); return !isBlankRow(row); }).map(row => {
        return pick(row, ALLOWED[kind]);
      });
      if (rows.length) out[key] = rows;
    }
    if (model.correction !== undefined) {
      const c = checkObject(model.correction, 'correction');
      const picked = pick(c, ALLOWED.correction);
      if (Object.keys(picked).some(k => k !== 'window') || (picked.window && picked.window !== 'not_assessed')) out.correction = picked;
    }
    if (model.return !== undefined) {
      const r = checkObject(model.return, 'return');
      const picked = pick(r, ALLOWED.return);
      if (Object.keys(picked).length) out.return = picked;
    }
    return validateCase(out);
  }
  // Pre-scan JSON object keys, because JSON.parse silently replaces duplicate keys.
  // JSON.parse itself remains responsible for validating primitives, escapes and grammar.
  function rejectDuplicateKeys(raw) {
    let i = 0;
    const skip = () => { while (/\s/.test(raw[i] || '') && i < raw.length) i++; };
    function readString() {
      if (raw[i] !== '"') fail('invalid JSON');
      const start = i++;
      while (i < raw.length) {
        const ch = raw[i++];
        if (ch === '\\') { i++; continue; }
        if (ch === '"') return JSON.parse(raw.slice(start, i));
      }
      fail('invalid JSON');
    }
    function value(depth) {
      if (depth > 16) fail('JSON nesting limit exceeded');
      skip();
      if (raw[i] === '{') {
        i++; skip(); const keys = new Set();
        if (raw[i] === '}') { i++; return; }
        while (i < raw.length) {
          skip(); const key = readString();
          if (keys.has(key)) fail('duplicate JSON key');
          keys.add(key); skip();
          if (raw[i++] !== ':') fail('invalid JSON');
          value(depth + 1); skip();
          if (raw[i] === '}') { i++; return; }
          if (raw[i++] !== ',') fail('invalid JSON');
        }
        fail('invalid JSON');
      }
      if (raw[i] === '[') {
        i++; skip(); if (raw[i] === ']') { i++; return; }
        while (i < raw.length) {
          value(depth + 1); skip();
          if (raw[i] === ']') { i++; return; }
          if (raw[i++] !== ',') fail('invalid JSON');
        }
        fail('invalid JSON');
      }
      if (raw[i] === '"') { readString(); return; }
      const start = i;
      while (i < raw.length && !/[\s,}\]]/.test(raw[i])) i++;
      if (i === start) fail('invalid JSON');
    }
    value(0); skip();
    if (i !== raw.length) fail('invalid JSON');
  }
  function parseCase(raw) {
    if (typeof raw !== 'string') fail('input must be UTF-8 text');
    if (byteCount(raw) > LIMIT_BYTES) fail('input exceeds 128 KiB');
    try {
      rejectDuplicateKeys(raw);
      const data = JSON.parse(raw);
      return validateCase(data);
    } catch (e) {
      if (e instanceof SyntaxError) fail('invalid JSON');
      throw e;
    }
  }
  function encodeCase(data) {
    validateCase(data);
    const pretty = JSON.stringify(data, null, 2) + '\n';
    if (byteCount(pretty) > LIMIT_BYTES) fail('export exceeds 128 KiB');
    return pretty;
  }

  const API = { makeCase, validateCase, parseCase, encodeCase, byteCount };
  if (typeof module !== 'undefined' && module.exports) module.exports = API;
  if (typeof document === 'undefined') return;

  const el = id => document.getElementById(id);
  function collectRow(element) {
    const fields = {};
    for (const control of element.querySelectorAll('[data-field]')) fields[control.dataset.field] = control.value;
    return fields;
  }
  function addRow(kind, values = {}) {
    const template = el('template-' + kind);
    const row = template.content.firstElementChild.cloneNode(true);
    for (const control of row.querySelectorAll('[data-field]')) {
      if (Object.hasOwn(values, control.dataset.field)) control.value = values[control.dataset.field];
    }
    const remove = row.querySelector('[data-remove]');
    remove.addEventListener('click', () => row.remove());
    el('rows-' + kind).appendChild(row);
    return row;
  }
  function getFormModel() {
    return {
      title: el('case-title').value, scope: el('case-scope').value,
      claims: Array.from(el('rows-claims').children, collectRow),
      parties: Array.from(el('rows-parties').children, collectRow),
      possibilities: Array.from(el('rows-possibilities').children, collectRow),
      correction: collectRow(el('correction-fields')),
      return: collectRow(el('return-fields'))
    };
  }
  function replaceRows(kind, values) {
    el('rows-' + kind).replaceChildren();
    for (const value of values) addRow(kind, value);
    if (kind === 'claims' && !values.length) addRow('claims', {kind:'change'});
  }
  function setFields(id, values) {
    for (const control of el(id).querySelectorAll('[data-field]')) control.value = values[control.dataset.field] || (control.dataset.field === 'window' ? 'not_assessed' : '');
  }
  function loadCase(data) {
    // Called only after validation; no untrusted content is assigned as HTML.
    el('case-title').value = data.title;
    el('case-scope').value = data.scope || '';
    replaceRows('claims', data.claims);
    replaceRows('parties', data.parties || []);
    replaceRows('possibilities', data.possibilities || []);
    setFields('correction-fields', data.correction || {});
    setFields('return-fields', data.return || {});
  }
  function report(message, error = false) {
    const node = el('status'); node.textContent = message; node.dataset.error = String(error);
    node.focus();
  }
  document.addEventListener('DOMContentLoaded', () => {
    addRow('claims', {kind: 'change'});
    for (const b of document.querySelectorAll('[data-add]')) b.addEventListener('click', () => addRow(b.dataset.add));
    el('intake-form').addEventListener('submit', event => {
      event.preventDefault();
      try {
        const data = makeCase(getFormModel());
        const content = encodeCase(data);
        const blob = new Blob([content], {type:'application/json;charset=utf-8'});
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url; link.download = 'case-card-draft.json';
        link.style.display = 'none'; document.body.appendChild(link);
        link.click(); link.remove();
        setTimeout(() => URL.revokeObjectURL(url), 1000);
        report('JSON prepared as a local download. Keep it private; use case_card.py to make the printable card. No upload occurred.');
      } catch (e) { report('Not exported: ' + e.message, true); }
    });
    el('import-json').addEventListener('change', async event => {
      const file = event.target.files && event.target.files[0];
      if (!file) return;
      try {
        if (file.size > LIMIT_BYTES) fail('input exceeds 128 KiB');
        const data = parseCase(await file.text());
        loadCase(data);
        report('Local JSON imported for editing. Review all fields before exporting; no upload occurred.');
      } catch (e) { report('Import refused; existing form retained: ' + e.message, true); }
      finally { event.target.value = ''; }
    });
  });
})(typeof window !== 'undefined' ? window : globalThis);
