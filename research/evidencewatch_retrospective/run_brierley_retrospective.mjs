#!/usr/bin/env node
/**
 * Fail-closed execution harness for the frozen EvidenceWatch Brierley challenge.
 *
 * Dry-run is the default and performs zero provider calls.
 *
 * Dry-run:
 *   node research/evidencewatch_retrospective/run_brierley_retrospective.mjs \
 *     --evidencewatch /path/to/evidencewatch \
 *     --packet /path/to/evidencewatch_brierley_packet.json \
 *     --output /path/to/pre_unblind_output.json \
 *     --ledger /path/to/brierley-ledger.jsonl
 *
 * Live:
 *   NVIDIA_API_KEY=... node research/evidencewatch_retrospective/run_brierley_retrospective.mjs \
 *     --live \
 *     --evidencewatch /path/to/evidencewatch \
 *     --packet /path/to/evidencewatch_brierley_packet.json \
 *     --output /path/to/pre_unblind_output.json \
 *     --ledger /path/to/brierley-ledger.jsonl
 */

import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { pathToFileURL } from 'node:url';

const EXPECTED_EVIDENCEWATCH_COMMIT = '9c96c8390d65f4fb452b2a106bcdb4fa0418ea6f';
const EXPECTED_BLOBS = {
  'src/ledger.mjs': 'df04ac27819c6f681b2534b27045628270a42dbb',
  'src/nvidia-analyzer.mjs': '19886ffbaa806c428ab8fb9c183134e5c702b6cf',
  'src/engine.mjs': 'e08c4028c0780186bd4353ddb9975aa2e0aee10f',
  'package.json': 'b93683b35aec26c97fb0855979effeea26e4110e',
};
const MODEL = 'nvidia/nemotron-3-super-120b-a12b';
const ENDPOINT = 'https://integrate.api.nvidia.com/v1/chat/completions';
const COMMON_CLAIM = 'The substantive findings and conclusions stated in this study abstract.';
const EXPECTED_CASES = 44;
const EXPECTED_PROVIDER_CALLS = EXPECTED_CASES * 2;
const PACKET_SCHEMA = 'evidencewatch-brierley-blinded-packet-v1';

function fail(message) {
  throw new Error(message);
}

function parseArgs(argv) {
  const out = {
    live: false,
    evidencewatch: '',
    packet: '',
    output: '',
    ledger: '',
  };
  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === '--live') {
      out.live = true;
      continue;
    }
    if (['--evidencewatch', '--packet', '--output', '--ledger'].includes(arg)) {
      const value = argv[index + 1];
      if (!value || value.startsWith('--')) fail(`Missing value for ${arg}`);
      out[arg.slice(2)] = value;
      index += 1;
      continue;
    }
    fail(`Unknown argument: ${arg}`);
  }
  for (const key of ['evidencewatch', 'packet', 'output', 'ledger']) {
    if (!out[key]) fail(`Missing required --${key}`);
  }
  return out;
}

function sha256Buffer(value) {
  return crypto.createHash('sha256').update(value).digest('hex');
}

function git(repoPath, args) {
  return execFileSync('git', ['-C', repoPath, ...args], {
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
  }).trim();
}

function verifyEvidenceWatchCheckout(root) {
  const resolved = path.resolve(root);
  if (!fs.existsSync(resolved)) fail(`EvidenceWatch checkout not found: ${resolved}`);

  const head = git(resolved, ['rev-parse', 'HEAD']);
  if (head !== EXPECTED_EVIDENCEWATCH_COMMIT) {
    fail(`EvidenceWatch HEAD mismatch: expected ${EXPECTED_EVIDENCEWATCH_COMMIT}, observed ${head}`);
  }

  const observedBlobs = {};
  for (const [relativePath, expected] of Object.entries(EXPECTED_BLOBS)) {
    const fullPath = path.join(resolved, relativePath);
    if (!fs.existsSync(fullPath)) fail(`Pinned EvidenceWatch file missing: ${relativePath}`);
    const observed = git(resolved, ['hash-object', relativePath]);
    observedBlobs[relativePath] = observed;
    if (observed !== expected) {
      fail(`EvidenceWatch Git blob mismatch for ${relativePath}: expected ${expected}, observed ${observed}`);
    }
  }

  return { root: resolved, head, blobs: observedBlobs };
}

function validatePacket(packetPath) {
  const resolved = path.resolve(packetPath);
  const bytes = fs.readFileSync(resolved);
  const text = bytes.toString('utf8');
  const packet = JSON.parse(text);

  if (packet.schema !== PACKET_SCHEMA) fail(`Unexpected packet schema: ${packet.schema}`);
  if (packet.status !== 'BLINDED_INPUT_NO_OWNER_LABELS') fail(`Unexpected packet status: ${packet.status}`);
  if (packet.case_count !== EXPECTED_CASES) fail(`Expected packet case_count=${EXPECTED_CASES}, got ${packet.case_count}`);
  if (!Array.isArray(packet.cases) || packet.cases.length !== EXPECTED_CASES) {
    fail(`Expected ${EXPECTED_CASES} packet cases`);
  }

  const forbidden = [
    'ABSTRACT_MAJOR_CHANGE',
    'ABSTRACT_NO_CHANGE',
    '"role"',
    '"preprint_doi"',
    '"published_doi"',
    '"source_row"',
    'evidencewatch-brierley-blind-v1',
  ];
  for (const token of forbidden) {
    if (text.includes(token)) fail(`Blinding leak found in packet: ${token}`);
  }

  const seen = new Set();
  for (const entry of packet.cases) {
    const keys = Object.keys(entry).sort();
    const expectedKeys = ['case_id', 'preprint_abstract', 'published_abstract'];
    if (JSON.stringify(keys) !== JSON.stringify(expectedKeys)) {
      fail(`Unexpected packet keys for case ${entry.case_id || '(unknown)'}: ${keys.join(', ')}`);
    }
    if (!/^case-\d{3}$/.test(String(entry.case_id || ''))) {
      fail(`Invalid opaque case id: ${entry.case_id}`);
    }
    if (seen.has(entry.case_id)) fail(`Duplicate case id: ${entry.case_id}`);
    seen.add(entry.case_id);
    if (!String(entry.preprint_abstract || '').trim()) fail(`Empty preprint abstract: ${entry.case_id}`);
    if (!String(entry.published_abstract || '').trim()) fail(`Empty published abstract: ${entry.case_id}`);
  }

  return {
    resolved,
    packet,
    sha256: sha256Buffer(bytes),
  };
}

function ensureFreshLivePaths(outputPath, ledgerPath) {
  const output = path.resolve(outputPath);
  const ledger = path.resolve(ledgerPath);
  if (output === ledger) fail('Output and ledger paths must differ');
  for (const candidate of [output, ledger, `${ledger}.lock`]) {
    if (fs.existsSync(candidate)) {
      fail(`Refusing live run because path already exists: ${candidate}`);
    }
  }
  fs.mkdirSync(path.dirname(output), { recursive: true });
  fs.mkdirSync(path.dirname(ledger), { recursive: true });
  return { output, ledger };
}

function syntheticSource(caseId, phase) {
  const publication = phase === 'publication';
  return {
    id: `${caseId}-${phase}`,
    url: `urn:evidencewatch-brierley:${caseId}:${phase}`,
    role: 'primary',
    stateAuthority: true,
    independenceGroup: caseId,
    authorityAsOf: publication ? '2000-01-02T00:00:00.000Z' : '2000-01-01T00:00:00.000Z',
  };
}

function resultReceipt(result, elapsedMs) {
  return {
    engine_status: result?.status ?? null,
    source_id: result?.sourceId ?? null,
    relation: result?.analysis?.relation ?? null,
    current_state: result?.analysis?.currentState ?? null,
    summary: result?.analysis?.summary ?? null,
    material_reasons: result?.analysis?.materialReasons ?? [],
    alert_kind: result?.alert?.data?.kind ?? result?.alert?.kind ?? null,
    error: result?.error ?? null,
    elapsed_ms: elapsedMs,
  };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const source = verifyEvidenceWatchCheckout(args.evidencewatch);
  const packetInfo = validatePacket(args.packet);

  const dryPlan = {
    schema: 'evidencewatch-brierley-run-plan-v1',
    status: args.live ? 'LIVE_REQUESTED_NOT_YET_STARTED' : 'DRY_RUN_VALIDATED_NO_PROVIDER_CALLS',
    evidencewatch: {
      commit: source.head,
      blobs: source.blobs,
    },
    packet: {
      path: packetInfo.resolved,
      sha256: packetInfo.sha256,
      cases: packetInfo.packet.case_count,
    },
    provider: {
      model: MODEL,
      endpoint: ENDPOINT,
      expected_calls: EXPECTED_PROVIDER_CALLS,
    },
    common_claim: COMMON_CLAIM,
    output_path: path.resolve(args.output),
    ledger_path: path.resolve(args.ledger),
  };

  if (!args.live) {
    process.stdout.write(JSON.stringify(dryPlan, null, 2) + '\n');
    process.stdout.write('EVIDENCEWATCH_BRIERLEY_DRY_RUN_OK\n');
    return;
  }

  if (!process.env.NVIDIA_API_KEY) {
    fail('Live run requires NVIDIA_API_KEY in the environment');
  }

  const paths = ensureFreshLivePaths(args.output, args.ledger);

  // Import only after all fail-closed source/packet/path checks pass.
  const ledgerModule = await import(pathToFileURL(path.join(source.root, 'src', 'ledger.mjs')).href);
  const engineModule = await import(pathToFileURL(path.join(source.root, 'src', 'engine.mjs')).href);
  const analyzerModule = await import(pathToFileURL(path.join(source.root, 'src', 'nvidia-analyzer.mjs')).href);

  const { JsonlLedger } = ledgerModule;
  const { EvidenceWatchEngine } = engineModule;
  const { createNvidiaAnalyzer } = analyzerModule;

  const providerReceipts = [];
  let receiptContext = null;

  const receiptFetch = async (url, options) => {
    const startedAt = new Date().toISOString();
    const response = await fetch(url, options);
    const rawBody = await response.clone().text();
    providerReceipts.push({
      case_id: receiptContext?.case_id ?? null,
      phase: receiptContext?.phase ?? null,
      started_at: startedAt,
      completed_at: new Date().toISOString(),
      http_status: response.status,
      ok: response.ok,
      raw_response_body: rawBody,
    });
    return response;
  };

  const analyzer = createNvidiaAnalyzer({
    apiKey: process.env.NVIDIA_API_KEY,
    model: MODEL,
    endpoint: ENDPOINT,
    fetchImpl: receiptFetch,
  });

  const ledger = new JsonlLedger(paths.ledger);
  const engine = new EvidenceWatchEngine({ ledger, analyzer });
  const cases = [];
  const startedAt = new Date().toISOString();

  for (const entry of packetInfo.packet.cases) {
    const caseId = entry.case_id;
    const watchId = `brierley-${caseId}`;
    const preprintSource = syntheticSource(caseId, 'preprint');
    const publicationSource = syntheticSource(caseId, 'publication');
    const dependentId = `${caseId}-review-item`;

    engine.createWatch({
      id: watchId,
      claim: COMMON_CLAIM,
      sources: [preprintSource, publicationSource],
      dependents: [dependentId],
      createdAt: '2000-01-01T00:00:00.000Z',
    });

    receiptContext = { case_id: caseId, phase: 'preprint' };
    const baselineStarted = Date.now();
    const baseline = await engine.observe({
      watchId,
      source: preprintSource,
      content: entry.preprint_abstract,
      observedAt: '2000-01-01T00:00:00.000Z',
      reachable: true,
      candidateLinks: [],
    });
    const baselineElapsed = Date.now() - baselineStarted;

    receiptContext = { case_id: caseId, phase: 'publication' };
    const successorStarted = Date.now();
    const successor = await engine.observe({
      watchId,
      source: publicationSource,
      content: entry.published_abstract,
      observedAt: '2000-01-02T00:00:00.000Z',
      reachable: true,
      candidateLinks: [],
    });
    const successorElapsed = Date.now() - successorStarted;

    const snapshot = engine.getSnapshot(watchId);
    cases.push({
      case_id: caseId,
      baseline: resultReceipt(baseline, baselineElapsed),
      successor: resultReceipt(successor, successorElapsed),
      prediction_review: successor?.status === 'MATERIAL_DELTA',
      final_canonical_state: snapshot?.currentState ?? null,
      alert_count: snapshot?.alerts?.length ?? 0,
    });
  }

  receiptContext = null;

  if (providerReceipts.length !== EXPECTED_PROVIDER_CALLS) {
    fail(`Provider-call count mismatch: expected ${EXPECTED_PROVIDER_CALLS}, observed ${providerReceipts.length}`);
  }

  const output = {
    schema: 'evidencewatch-brierley-pre-unblind-output-v1',
    status: 'OUTPUT_FROZEN_BEFORE_OWNER_LABEL_JOIN',
    started_at: startedAt,
    completed_at: new Date().toISOString(),
    evidencewatch: {
      commit: source.head,
      blobs: source.blobs,
    },
    packet: {
      sha256: packetInfo.sha256,
      case_count: packetInfo.packet.case_count,
    },
    provider: {
      model: MODEL,
      endpoint: ENDPOINT,
      expected_calls: EXPECTED_PROVIDER_CALLS,
      observed_calls: providerReceipts.length,
    },
    common_claim: COMMON_CLAIM,
    cases,
    provider_receipts: providerReceipts,
    ledger_path: paths.ledger,
  };

  const rendered = JSON.stringify(output, null, 2) + '\n';
  fs.writeFileSync(paths.output, rendered, { encoding: 'utf8', flag: 'wx' });
  const digest = sha256Buffer(Buffer.from(rendered, 'utf8'));

  process.stdout.write(JSON.stringify({
    status: output.status,
    cases: cases.length,
    provider_calls: providerReceipts.length,
    packet_sha256: packetInfo.sha256,
    output_sha256: digest,
    output_path: paths.output,
    ledger_path: paths.ledger,
  }, null, 2) + '\n');
  process.stdout.write('EVIDENCEWATCH_BRIERLEY_LIVE_RUN_COMPLETE_PRE_UNBLIND\n');
}

main().catch((error) => {
  console.error(error?.stack || error?.message || String(error));
  process.exitCode = 1;
});
