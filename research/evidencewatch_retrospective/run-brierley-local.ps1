[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$EvidenceWatchPath,

    [switch]$Live,

    [string]$RunRoot = (Join-Path $HOME "EvidenceWatchRuns")
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$ExpectedEvidenceWatchCommit = "9c96c8390d65f4fb452b2a106bcdb4fa0418ea6f"
$ExpectedPacketSha256 = "f12762d4867da361e9eb72e3a12c30e82b734f005b09d527b7b19c7aee2ae1cc"
$ExpectedKeySha256 = "75c64ca3235812b2cccf0d5dc2801698dd23f20a393f627106026d619eb299c9"

$ExpectedOwnerBlobs = @{
    "abstract_scoring.csv" = "da5d608019200a14b31c9d605df8e27ced2eaa21"
    "all_pairs.tsv"        = "3c26344ffc84ca43656477dd2229ac6530d4735f"
}

$ExpectedComBlobs = @{
    "research/evidencewatch_retrospective/brierley_major_vs_nochange_manifest_v2.json" = "4d12bf1b66ae45ef161901616ed6a2258eb03ba3"
    "research/evidencewatch_retrospective/verify_brierley_manifest.py"                 = "df7f501d3e18ae8df6dea57cb0901daf6b2c6dae"
    "research/evidencewatch_retrospective/build_blinded_brierley_packet.py"            = "b285348ca24722a20f6c3913ccba93659ce56f3e"
    "research/evidencewatch_retrospective/score_trivial_baselines.py"                  = "8f442453aea3348cbb2c71da51c989bc9fae9433"
    "research/evidencewatch_retrospective/run_brierley_retrospective.mjs"              = "9b156be82c76fa06059a234c8a438a1ce0b16292"
    "research/evidencewatch_retrospective/score_brierley_unblinded.py"                 = "b12d9e23bb2c90186229d9c0bd142937aad3eb2b"
}

function Invoke-Checked {
    param(
        [Parameter(Mandatory = $true)]
        [string]$FilePath,

        [Parameter()]
        [string[]]$ArgumentList = @()
    )

    & $FilePath @ArgumentList
    if ($LASTEXITCODE -ne 0) {
        throw "$FilePath failed with exit code $LASTEXITCODE"
    }
}

function Get-GitOutput {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Repository,

        [Parameter(Mandatory = $true)]
        [string[]]$Arguments
    )

    $output = & git -C $Repository @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "git -C $Repository $($Arguments -join ' ') failed with exit code $LASTEXITCODE"
    }
    return ($output | Out-String).Trim()
}

function Assert-GitBlob {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Repository,

        [Parameter(Mandatory = $true)]
        [string]$RelativePath,

        [Parameter(Mandatory = $true)]
        [string]$Expected
    )

    $fullPath = Join-Path $Repository ($RelativePath -replace '/', [IO.Path]::DirectorySeparatorChar)
    if (-not (Test-Path -LiteralPath $fullPath -PathType Leaf)) {
        throw "Required file missing: $RelativePath"
    }

    $observed = Get-GitOutput -Repository $Repository -Arguments @("hash-object", "--", $RelativePath)
    if ($observed -ne $Expected) {
        throw "Git blob mismatch for $RelativePath. Expected $Expected; observed $observed"
    }
}

function Assert-Sha256 {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,

        [Parameter(Mandatory = $true)]
        [string]$Expected
    )

    $observed = (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($observed -ne $Expected) {
        throw "SHA-256 mismatch for $Path. Expected $Expected; observed $observed"
    }
}

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$comRoot = (Resolve-Path (Join-Path $scriptDir "..\..")).Path
$evidenceWatchRoot = (Resolve-Path $EvidenceWatchPath).Path

Write-Host "EvidenceWatch Brierley retrospective v2 local runner"
Write-Host "COM:           $comRoot"
Write-Host "EvidenceWatch: $evidenceWatchRoot"
Write-Host "Mode:          $(if ($Live) { 'LIVE REQUESTED' } else { 'DRY RUN / ZERO PROVIDER CALLS' })"
Write-Host ""

# Tool availability first.
foreach ($command in @("git", "python", "node")) {
    if (-not (Get-Command $command -ErrorAction SilentlyContinue)) {
        throw "Required command not found: $command"
    }
}

# Freeze-check the COM experiment files used by this run.
foreach ($entry in $ExpectedComBlobs.GetEnumerator()) {
    Assert-GitBlob -Repository $comRoot -RelativePath $entry.Key -Expected $entry.Value
}

$comHead = Get-GitOutput -Repository $comRoot -Arguments @("rev-parse", "HEAD")
Write-Host "COM HEAD:      $comHead"
Write-Host "COM experiment file blobs: VERIFIED"

# Freeze-check the private EvidenceWatch checkout.
$evidenceWatchHead = Get-GitOutput -Repository $evidenceWatchRoot -Arguments @("rev-parse", "HEAD")
if ($evidenceWatchHead -ne $ExpectedEvidenceWatchCommit) {
    throw "EvidenceWatch HEAD mismatch. Expected $ExpectedEvidenceWatchCommit; observed $evidenceWatchHead"
}
Write-Host "EvidenceWatch HEAD: VERIFIED $evidenceWatchHead"

# Create a new run directory every time. Live runs must never reuse ledgers/output.
New-Item -ItemType Directory -Path $RunRoot -Force | Out-Null
$stamp = Get-Date -Format "yyyyMMdd-HHmmssfff"
$mode = if ($Live) { "live" } else { "dry" }
$runDir = Join-Path $RunRoot "brierley-v2-$mode-$stamp"
New-Item -ItemType Directory -Path $runDir | Out-Null

$ownerDir = Join-Path $runDir "owner"
New-Item -ItemType Directory -Path $ownerDir | Out-Null

$scoringPath = Join-Path $ownerDir "abstract_scoring.csv"
$pairsPath = Join-Path $ownerDir "all_pairs.tsv"
$ownerBase = "https://raw.githubusercontent.com/preprinting-a-pandemic/preprint_changes/a07c570cf3be4481ba74c59ceee22e40f949990b/data"

Write-Host ""
Write-Host "Fetching the two pinned public owner files..."
Invoke-WebRequest -Uri "$ownerBase/abstract_scoring.csv" -OutFile $scoringPath
Invoke-WebRequest -Uri "$ownerBase/all_pairs.tsv" -OutFile $pairsPath

foreach ($entry in $ExpectedOwnerBlobs.GetEnumerator()) {
    $ownerPath = Join-Path $ownerDir $entry.Key
    $observed = (& git hash-object -- $ownerPath | Out-String).Trim()
    if ($LASTEXITCODE -ne 0) {
        throw "git hash-object failed for $ownerPath"
    }
    if ($observed -ne $entry.Value) {
        throw "Pinned owner blob mismatch for $($entry.Key). Expected $($entry.Value); observed $observed"
    }
}
Write-Host "Pinned owner file blobs: VERIFIED"

$manifest = Join-Path $comRoot "research\evidencewatch_retrospective\brierley_major_vs_nochange_manifest_v2.json"
$verify = Join-Path $comRoot "research\evidencewatch_retrospective\verify_brierley_manifest.py"
$builder = Join-Path $comRoot "research\evidencewatch_retrospective\build_blinded_brierley_packet.py"
$baselineScorer = Join-Path $comRoot "research\evidencewatch_retrospective\score_trivial_baselines.py"
$harness = Join-Path $comRoot "research\evidencewatch_retrospective\run_brierley_retrospective.mjs"
$unblindScorer = Join-Path $comRoot "research\evidencewatch_retrospective\score_brierley_unblinded.py"

$packet = Join-Path $runDir "brierley_packet.json"
$key = Join-Path $runDir "brierley_owner_key.json"
$baselines = Join-Path $runDir "brierley_trivial_baselines.json"
$preUnblind = Join-Path $runDir "brierley_pre_unblind_output.json"
$ledger = Join-Path $runDir "brierley_ledger.jsonl"
$scored = Join-Path $runDir "brierley_scored_output.json"

Write-Host ""
Write-Host "Verifying raw-owner v2 selection..."
Invoke-Checked -FilePath "python" -ArgumentList @($verify, $scoringPath, $pairsPath, $manifest)

Write-Host ""
Write-Host "Building blinded packet + separate owner key..."
Invoke-Checked -FilePath "python" -ArgumentList @($builder, $pairsPath, $manifest, $packet, $key)
Assert-Sha256 -Path $packet -Expected $ExpectedPacketSha256
Assert-Sha256 -Path $key -Expected $ExpectedKeySha256
Write-Host "Frozen packet/key identities: VERIFIED"

Write-Host ""
Write-Host "Recomputing frozen trivial lexical baselines..."
Invoke-Checked -FilePath "python" -ArgumentList @($baselineScorer, $pairsPath, $manifest, $baselines)

Write-Host ""
Write-Host "Running fail-closed harness dry-run..."
Invoke-Checked -FilePath "node" -ArgumentList @(
    $harness,
    "--evidencewatch", $evidenceWatchRoot,
    "--packet", $packet,
    "--output", $preUnblind,
    "--ledger", $ledger
)

if (Test-Path -LiteralPath $preUnblind) {
    throw "Dry-run unexpectedly created pre-unblind output: $preUnblind"
}
if (Test-Path -LiteralPath $ledger) {
    throw "Dry-run unexpectedly created ledger: $ledger"
}

Write-Host ""
Write-Host "DRY-RUN GATE PASSED. No provider call has occurred."
Write-Host "Run directory: $runDir"

if (-not $Live) {
    Write-Host ""
    Write-Host "To execute the frozen 88-call live run, reuse this command with -Live while NVIDIA_API_KEY exists in this PowerShell session."
    exit 0
}

if ([string]::IsNullOrWhiteSpace($env:NVIDIA_API_KEY)) {
    throw "Live mode requires NVIDIA_API_KEY already present in this PowerShell session. The runner will not prompt for, print, or store the key."
}

Write-Host ""
Write-Host "LIVE MODE: executing the frozen 44-case / 88-analysis run."
Write-Host "Provider endpoint is currently documented as a free Developer Program prototype/research endpoint; account quota/rate limits still apply."
Write-Host ""

Invoke-Checked -FilePath "node" -ArgumentList @(
    $harness,
    "--live",
    "--evidencewatch", $evidenceWatchRoot,
    "--packet", $packet,
    "--output", $preUnblind,
    "--ledger", $ledger
)

if (-not (Test-Path -LiteralPath $preUnblind -PathType Leaf)) {
    throw "Live harness returned without creating expected pre-unblind output: $preUnblind"
}
if (-not (Test-Path -LiteralPath $ledger -PathType Leaf)) {
    throw "Live harness returned without creating expected ledger: $ledger"
}

$preUnblindSha = (Get-FileHash -LiteralPath $preUnblind -Algorithm SHA256).Hash.ToLowerInvariant()

Write-Host ""
Write-Host "LIVE PRE-UNBLIND RUN COMPLETE."
Write-Host "Pre-unblind output: $preUnblind"
Write-Host "Pre-unblind SHA256: $preUnblindSha"
Write-Host "Ledger: $ledger"
Write-Host ""
Write-Host "STOP HERE. Owner labels have NOT been joined automatically."
Write-Host "Review/preserve the pre-unblind output hash first."
Write-Host ""
Write-Host "When you deliberately choose to unblind and score, run:"
Write-Host ('python "{0}" "{1}" "{2}" "{3}" "{4}"' -f $unblindScorer, $preUnblind, $key, $baselines, $scored)
