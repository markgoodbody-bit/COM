#Requires -Version 5.1
[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ExpectedSourceSha256 = '8ff0b791dfb3bcde0367edf5c65de0ba3f73aee973b4b953fcbf98667f2412c4'
$ExpectedSourceBytes = 539443

$documents = [Environment]::GetFolderPath('MyDocuments')
if ([string]::IsNullOrWhiteSpace($documents)) {
    $documents = Join-Path $env:USERPROFILE 'Documents'
}
$root = Join-Path $documents 'Campfire-Square'
$appDir = Join-Path $root 'App'
$updatesDir = Join-Path $root 'Updates'
$installed = Join-Path $appDir 'Campfire-Square.ps1'
New-Item -ItemType Directory -Force -Path $updatesDir | Out-Null

function Get-Sha256File([string]$Path) {
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try {
        $stream = [System.IO.File]::OpenRead($Path)
        try {
            return ([BitConverter]::ToString($sha.ComputeHash($stream))).Replace('-','').ToLowerInvariant()
        }
        finally { $stream.Dispose() }
    }
    finally { $sha.Dispose() }
}

function Count-Literal([string]$Text, [string]$Needle) {
    if ([string]::IsNullOrEmpty($Needle)) { return 0 }
    $count = 0
    $index = 0
    while ($true) {
        $found = $Text.IndexOf($Needle, $index, [StringComparison]::Ordinal)
        if ($found -lt 0) { break }
        $count++
        $index = $found + $Needle.Length
    }
    return $count
}

function As-Lf([string]$Text) {
    return $Text.Replace("`r`n", "`n").Replace("`r", "`n")
}

if (-not (Test-Path -LiteralPath $installed)) {
    throw "Campfire Square source not found: $installed"
}

$beforeItem = Get-Item -LiteralPath $installed
$beforeSha = Get-Sha256File $installed
if ($beforeSha -ne $ExpectedSourceSha256 -or [int64]$beforeItem.Length -ne $ExpectedSourceBytes) {
    throw "REFUSED: installed Campfire Square is not exact R28F. Expected sha256 $ExpectedSourceSha256 / $ExpectedSourceBytes bytes; found $beforeSha / $($beforeItem.Length) bytes. Nothing changed."
}

$utf8Strict = New-Object System.Text.UTF8Encoding($false,$true)
$sourceBytes = [System.IO.File]::ReadAllBytes($installed)
try { $text = $utf8Strict.GetString($sourceBytes) }
catch { throw "REFUSED: installed source is not strict UTF-8. Nothing changed. $($_.Exception.Message)" }
finally { $sourceBytes = $null }

if ($text.Contains("`r")) {
    throw 'REFUSED: installed R28F source unexpectedly contains CR characters. Nothing changed.'
}

$oldSafe = As-Lf @'
function Safe-Property($Object, [string]$Name, $Default = $null) {
    if ($null -eq $Object) { return $Default }
    if (@($Object.PSObject.Properties.Name) -contains $Name) {
        return $Object.$Name
    }
    return $Default
}
'@
$newSafe = As-Lf @'
function Safe-Property($Object, [string]$Name, $Default = $null) {
    if ($null -eq $Object) { return $Default }
    if ($Object -is [System.Collections.IDictionary]) {
        if ($Object.Contains($Name)) { return $Object[$Name] }
    }
    if (@($Object.PSObject.Properties.Name) -contains $Name) {
        return $Object.$Name
    }
    return $Default
}
'@
if ((Count-Literal $text $oldSafe) -ne 1) {
    throw 'REFUSED: Safe-Property anchor is not exact/unique. Nothing changed.'
}
$text = $text.Replace($oldSafe, $newSafe)

$oldTimeoutHead = As-Lf @'
            if ([DateTime]::TryParse($startedText, [ref]$started)) {
                if (([DateTime]::UtcNow - $started.ToUniversalTime()).TotalMinutes -gt 5) {
                    $lastWorkerStatus = $null
'@
$newTimeoutHead = As-Lf @'
            if ([DateTime]::TryParse($startedText, [ref]$started)) {
                if (([DateTime]::UtcNow - $started.ToUniversalTime()).TotalMinutes -gt 5) {
                    $workerPid = [int](Safe-Property $state 'active_worker_pid' 0)
                    $workerAlive = $false
                    if ($workerPid -gt 0) {
                        try {
                            $null = Get-Process -Id $workerPid -ErrorAction Stop
                            $workerAlive = $true
                        }
                        catch { $workerAlive = $false }
                    }

                    if ($workerAlive) {
                        if ([string](Safe-Property $state 'active_dispatch_phase' '') -ne 'LATE_WORKER') {
                            $state.active_dispatch_phase = 'LATE_WORKER'
                            [void](Set-CcWriteRelayState $state)
                            [void](Write-CcWriteRelayLedgerEvent 'CC_WRITE_RELAY_WORKER_BEYOND_GRACE' ([pscustomobject]@{
                                request_id=$active
                                worker_pid=$workerPid
                                meaning='WORKER_STILL_RUNNING_NOT_OUTCOME_UNKNOWN'
                                square_retry=$false
                            }))
                        }
                        return
                    }

                    if (Test-Path -LiteralPath $statusPath) {
                        $lateWorkerStatus = $null
                        try { $lateWorkerStatus = Read-Utf8JsonFile $statusPath } catch { }
                        if ($null -ne $lateWorkerStatus) {
                            $lateTerminal = [string](Safe-Property $lateWorkerStatus 'status' '')
                            if (@('VERIFIED','REFUSED','FAILED_NO_WRITE','WRITE_OCCURRED_UNVERIFIED','OUTCOME_UNKNOWN') -contains $lateTerminal) {
                                $lateResponse = Safe-Property $lateWorkerStatus 'response' $null
                                if ($null -eq $lateResponse) {
                                    $lateResponse = New-CcWriteRelayResponse $active $lateTerminal $null ([ordered]@{ write_occurred=$null }) 'Worker reached a terminal state without a response envelope.'
                                }
                                $lateResponsePath = Write-CcWriteRelayResponseFile $active $lateResponse
                                [void](Write-CcWriteRelayLedgerEvent 'CC_WRITE_RELAY_RESPONSE_WRITTEN' ([pscustomobject]@{
                                    request_id=$active; status=$lateTerminal; response_path=$lateResponsePath; square_retry=$false
                                    recovered_after_grace=$true
                                }))
                                if (@('WRITE_OCCURRED_UNVERIFIED','OUTCOME_UNKNOWN') -contains $lateTerminal) {
                                    $lateResponseData = Safe-Property $lateResponse 'data' $null
                                    [void](Write-CcWriteRelayLedgerEvent 'CC_WRITE_RELAY_ATTENTION_REQUIRED' ([pscustomobject]@{
                                        request_id=$active
                                        status=$lateTerminal
                                        reason=[string](Safe-Property $lateResponse 'reason' '')
                                        public_comment_id=Safe-Property $lateResponseData 'public_comment_id' $null
                                        public_body_sha256=Safe-Property $lateResponseData 'public_body_sha256' $null
                                        read_must_remain_available=$true
                                        square_retry=$false
                                    }))
                                    Disable-CcWriteRelay
                                }
                                $state.active_request_id=$null; $state.active_worker_pid=$null; $state.active_started_at_utc=$null; $state.active_dispatch_phase=$null
                                [void](Set-CcWriteRelayState $state)
                                return
                            }
                        }
                    }

                    $lastWorkerStatus = $null
'@
if ((Count-Literal $text $oldTimeoutHead) -ne 1) {
    throw 'REFUSED: CC worker grace-window anchor is not exact/unique. Nothing changed.'
}
$text = $text.Replace($oldTimeoutHead, $newTimeoutHead)

$oldBodyCheck = "                Add-WitnessCheck 'body-exact' (`$actualBody -ceq `$intendedBody) 'public body matches exact intended text'"
$newBodyCheck = As-Lf @'
                $bodyExact = ($actualBody -ceq $intendedBody)
                $bodyExactDetail = if ($bodyExact) { 'public body matches exact intended text' } else { 'public body differs from exact intended text' }
                Add-WitnessCheck 'body-exact' $bodyExact $bodyExactDetail
'@
if ($newBodyCheck.EndsWith("`n")) { $newBodyCheck = $newBodyCheck.Substring(0, $newBodyCheck.Length - 1) }
if ((Count-Literal $text $oldBodyCheck) -ne 2) {
    throw 'REFUSED: body-exact witness anchor count is not exactly 2. Nothing changed.'
}
$text = $text.Replace($oldBodyCheck, $newBodyCheck)

$requiredAfter = @(
    'if ($Object -is [System.Collections.IDictionary])',
    "meaning='WORKER_STILL_RUNNING_NOT_OUTCOME_UNKNOWN'",
    'recovered_after_grace=$true',
    "'public body differs from exact intended text'",
    "if (@(`$Action.PSObject.Properties.Name) -contains 'closes_correction_debt_id') { throw 'CC REMOTE ROUTINE REFUSED: correction-debt closure is outside this lane.' }"
)
foreach ($needle in $requiredAfter) {
    if (-not $text.Contains($needle)) {
        throw "REFUSED: post-patch invariant missing: $needle. Nothing changed."
    }
}

$timestamp = [DateTime]::UtcNow.ToString('yyyyMMdd_HHmmss')
$staged = Join-Path $updatesDir ("Campfire-Square.R28F-CC-WRITE-HOTFIX.$timestamp.ps1")
$backup = Join-Path $appDir ("Campfire-Square.R28F-BEFORE-CC-WRITE-HOTFIX.$timestamp.ps1")
[System.IO.File]::WriteAllText($staged, $text, [System.Text.UTF8Encoding]::new($false))

$tokens = $null
$parseErrors = $null
[void][System.Management.Automation.Language.Parser]::ParseFile($staged, [ref]$tokens, [ref]$parseErrors)
if (@($parseErrors).Count -ne 0) {
    Remove-Item -LiteralPath $staged -Force -ErrorAction SilentlyContinue
    throw ("REFUSED: staged hotfix has PowerShell parse error(s): " + ((@($parseErrors) | ForEach-Object { $_.Message }) -join ' | ') + '. Installed source unchanged.')
}

$targetSha = Get-Sha256File $staged
$targetBytes = (Get-Item -LiteralPath $staged).Length
if ($targetSha -eq $beforeSha) {
    Remove-Item -LiteralPath $staged -Force -ErrorAction SilentlyContinue
    throw 'REFUSED: staged hotfix is byte-identical to R28F; expected changes were not produced.'
}

Copy-Item -LiteralPath $installed -Destination $backup -Force
if ((Get-Sha256File $backup) -ne $ExpectedSourceSha256) {
    Remove-Item -LiteralPath $backup -Force -ErrorAction SilentlyContinue
    Remove-Item -LiteralPath $staged -Force -ErrorAction SilentlyContinue
    throw 'REFUSED: backup did not preserve exact R28F bytes. Installed source unchanged.'
}

Copy-Item -LiteralPath $staged -Destination $installed -Force
$installedAfterSha = Get-Sha256File $installed
$installedAfterBytes = (Get-Item -LiteralPath $installed).Length
if ($installedAfterSha -ne $targetSha -or $installedAfterBytes -ne $targetBytes) {
    Copy-Item -LiteralPath $backup -Destination $installed -Force
    throw 'INSTALL FAILED: post-copy target identity mismatch. Exact R28F backup was restored.'
}

Write-Host ''
Write-Host 'CC CAMPFIRE WRITE HOTFIX INSTALLED' -ForegroundColor Green
Write-Host "before sha256 : $beforeSha"
Write-Host "after sha256  : $installedAfterSha"
Write-Host "after bytes   : $installedAfterBytes"
Write-Host "backup        : $backup"
Write-Host "staged source : $staged"
Write-Host ''
Write-Host 'Changed: IDictionary read, late-worker terminal propagation, truthful body-exact witness detail.'
Write-Host 'Unchanged: correction debts, witness investigations, grants, quotas, authority, correction-debt closure rules.'
Write-Host 'Close and reopen Campfire Square if it was running while this patch was installed.'
