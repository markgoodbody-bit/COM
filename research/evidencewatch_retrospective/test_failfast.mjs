// Execute the actual post-preflight harness loop with offline dependencies.
// Does not test source/packet gates, real engine/provider behaviour, or disk durability.
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs';
import vm from 'node:vm';
import test from 'node:test';

const sourceText = fs.readFileSync(new URL('./run_brierley_retrospective.mjs', import.meta.url), 'utf8');
function between(start, end) {
  assert.equal(sourceText.split(start).length, 2, `unique start anchor: ${start}`);
  assert.equal(sourceText.split(end).length, 2, `unique end anchor: ${end}`);
  const from = sourceText.indexOf(start);
  const to = sourceText.indexOf(end, from);
  assert.ok(to > from, 'ordered source anchors');
  return sourceText.slice(from, to);
}
const helpers = between('function syntheticSource(', 'async function main()');
const loop = between('  const providerReceipts = [];', '\nmain().catch(');
// loop includes the original main closing brace; only its preflight is excluded.
const script = new vm.Script(`${helpers}\nasync function exercise() {\n${loop}\nexercise()`);

async function exercise(failAt = null, responseMissing = false, outputExists = false) {
  let calls = 0;
  let creates = 0;
  let written;
  let stdout = '';
  let analyze;
  const processStub = { env: { NVIDIA_API_KEY: 'offline-placeholder' },
    stdout: { write: text => { stdout += text; } }, exitCode: 0 };
  class Engine {
    createWatch() { creates++; }
    async observe(input) {
      calls++;
      if (!(calls === failAt && responseMissing)) await analyze();
      return { status: calls === failAt ? 'ANALYSIS_FAILED' :
        (calls % 2 ? 'BASELINE_ESTABLISHED' : 'NO_MATERIAL_DELTA'),
        sourceId: input.source.id, error: calls === failAt ? 'synthetic failure' : null };
    }
    getSnapshot() { return { currentState: { status: 'supported' }, alerts: [] }; }
  }
  const context = vm.createContext({
    Buffer, MODEL: 'offline', ENDPOINT: 'offline://no-network',
    COMMON_CLAIM: 'synthetic', EXPECTED_PROVIDER_CALLS: 88,
    source: { head: 'synthetic-source', blobs: { file: 'synthetic-blob' } },
    packetInfo: { sha256: 'synthetic-packet', packet: { case_count: 44,
      cases: Array.from({ length: 44 }, (_, i) => ({ case_id: `c${i}`,
        preprint_abstract: 'before', published_abstract: 'after' })) } },
    paths: { output: 'memory-output', ledger: 'memory-ledger' },
    process: processStub, EvidenceWatchEngine: Engine, JsonlLedger: class {},
    createNvidiaAnalyzer({ fetchImpl }) { analyze = () => fetchImpl('offline://no-network', {}); return {}; },
    fetch: async url => {
      assert.equal(url, 'offline://no-network');
      return { status: 200, ok: true, clone: () => ({ text: async () => '{"synthetic":true}' }) };
    },
    sha256Buffer: value => crypto.createHash('sha256').update(value).digest('hex'),
    fail: message => { throw new Error(message); },
    fs: { writeFileSync(path, text, options) {
      assert.equal(path, 'memory-output');
      assert.equal(options.flag, 'wx');
      if (outputExists) throw new Error('EEXIST');
      assert.equal(written, undefined, 'exactly one sealed output');
      written = JSON.parse(text);
    } },
  });
  await script.runInContext(context, { timeout: 1000 });
  return { calls, creates, written, stdout, exitCode: processStub.exitCode };
}

for (const failureAt of [1, 2, 43, 44, 87, 88]) {
  for (const missingResponse of [false, true]) {
    test(`stop at analysis ${failureAt}, missing response ${missingResponse}`, async () => {
      const result = await exercise(failureAt, missingResponse);
      const output = result.written;
      assert.equal(result.calls, failureAt);
      assert.equal(result.creates, Math.ceil(failureAt / 2));
      assert.equal(result.exitCode, 3);
      assert.equal(output.status, 'PARTIAL_RUN_ABORTED_ON_ANALYSIS_FAILURE');
      assert.equal(output.cases.length, Math.ceil(failureAt / 2));
      assert.equal(output.failure.case_id, `c${Math.floor((failureAt - 1) / 2)}`);
      assert.equal(output.failure.phase, failureAt % 2 ? 'preprint' : 'publication');
      assert.equal(output.failure.error, 'synthetic failure');
      assert.equal(output.provider.attempted_analyses, failureAt);
      assert.equal(output.provider.observed_responses, failureAt - Number(missingResponse));
      assert.equal(output.provider_receipts.length, failureAt - Number(missingResponse));
      assert.equal(output.evidencewatch.commit, 'synthetic-source');
      assert.equal(output.packet.sha256, 'synthetic-packet');
      assert.equal(output.ledger_path, 'memory-ledger');
      if (failureAt % 2) assert.equal(output.cases.at(-1).successor, null);
      const marker = result.stdout.indexOf('\nEVIDENCEWATCH_');
      const summary = JSON.parse(result.stdout.slice(0, marker));
      assert.equal(summary.output_sha256, crypto.createHash('sha256')
        .update(JSON.stringify(output, null, 2) + '\n').digest('hex'));
      assert.ok(result.stdout.includes('LIVE_RUN_ABORTED_PRE_UNBLIND'));
      assert.ok(!result.stdout.includes('LIVE_RUN_COMPLETE_PRE_UNBLIND'));
    });
  }
}
test('complete control processes all 88 analyses', async () => {
  const result = await exercise();
  assert.equal(result.calls, 88);
  assert.equal(result.written.cases.length, 44);
  assert.equal(result.written.status, 'OUTPUT_FROZEN_BEFORE_OWNER_LABEL_JOIN');
  assert.equal(result.written.provider.observed_calls, 88);
  assert.equal(result.exitCode, 0);
  assert.ok(result.stdout.includes('LIVE_RUN_COMPLETE_PRE_UNBLIND'));
});
test('existing partial output is never overwritten', async () => {
  await assert.rejects(exercise(1, false, true), /EEXIST/);
});
