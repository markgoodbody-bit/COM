#Requires -Version 5.1
[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ExpectedSourceSha256 = '5ebfae36f0dcf659514976c5b9f1641e4ba820e0b6a580db7332fc9e5252af4b'
$ExpectedSourceBytes = 548943

$Documents = [Environment]::GetFolderPath('MyDocuments')
if ([string]::IsNullOrWhiteSpace($Documents)) { $Documents = Join-Path $env:USERPROFILE 'Documents' }
$Root = Join-Path $Documents 'Campfire-Square'
$AppDir = Join-Path $Root 'App'
$UpdatesDir = Join-Path $Root 'Updates'
$Installed = Join-Path $AppDir 'Campfire-Square.ps1'

function Get-Sha256File([string]$Path) {
    $sha=[Security.Cryptography.SHA256]::Create()
    try {
        $stream=[IO.File]::OpenRead($Path)
        try { return ([BitConverter]::ToString($sha.ComputeHash($stream))).Replace('-','').ToLowerInvariant() }
        finally { $stream.Dispose() }
    }
    finally { $sha.Dispose() }
}
function As-Lf([string]$Text) { return ($Text -replace "`r`n","`n" -replace "`r","`n") }
function Count-Literal([string]$Text,[string]$Needle) {
    if ([string]::IsNullOrEmpty($Needle)) { return 0 }
    $count=0; $at=0
    while ($true) {
        $i=$Text.IndexOf($Needle,$at,[StringComparison]::Ordinal)
        if ($i -lt 0) { break }
        $count++; $at=$i+$Needle.Length
    }
    return $count
}
function Replace-One([string]$Text,[string]$Old,[string]$New,[string]$Label) {
    $n=Count-Literal $Text $Old
    if ($n -ne 1) { throw "REFUSED: $Label anchor count=$n, expected 1. Nothing changed." }
    return $Text.Replace($Old,$New)
}

if (-not (Test-Path -LiteralPath $Installed)) { throw "REFUSED: Campfire Square source not found: $Installed" }
$item=Get-Item -LiteralPath $Installed
$beforeSha=Get-Sha256File $Installed
if ($beforeSha -ne $ExpectedSourceSha256 -or $item.Length -ne $ExpectedSourceBytes) {
    throw "REFUSED: installed source is not exact Hotfix 2. Expected $ExpectedSourceSha256 / $ExpectedSourceBytes bytes; found $beforeSha / $($item.Length). Nothing changed."
}
$bytes=[IO.File]::ReadAllBytes($Installed)
$utf8=New-Object Text.UTF8Encoding($false,$true)
try { $text=$utf8.GetString($bytes) } finally { $bytes=$null }
if ($text.Contains("`r")) { throw 'REFUSED: installed source unexpectedly contains CR characters. Nothing changed.' }

# Repair 1: Windows PowerShell 5.1 binds $null to String.Empty for this overload.
# Pass a genuine null string so File.Replace can atomically replace without a backup path.
$brokenReplace='[System.IO.File]::Replace($tempPath,$statusPath,$null)'
$fixedReplace='[System.IO.File]::Replace($tempPath,$statusPath,[NullString]::Value)'
$text=Replace-One $text $brokenReplace $fixedReplace 'CC atomic status File.Replace null binding'

# Repair 2a: do not silently lose failure to measure the worker StartTime.
$oldCapture=As-Lf @'
            $workerStartUtc = $null
            try { $workerStartUtc = $process.StartTime.ToUniversalTime().ToString('o') } catch { }
            $state = Get-CcWriteRelayState
'@
$newCapture=As-Lf @'
            $workerStartUtc = $null
            $workerStartCaptureError = $null
            try { $workerStartUtc = $process.StartTime.ToUniversalTime().ToString('o') }
            catch { $workerStartCaptureError = $_.Exception.Message }
            $state = Get-CcWriteRelayState
'@
$text=Replace-One $text $oldCapture $newCapture 'CC dispatch worker StartTime capture'

$oldDispatchEvent="                request_id=`$requestId; worker_pid=`$process.Id; worker_start_time_utc=`$workerStartUtc; accepted_path=`$acceptedPath; square_retry=`$false"
$newDispatchEvent="                request_id=`$requestId; worker_pid=`$process.Id; worker_start_time_utc=`$workerStartUtc; worker_start_time_capture_error=`$workerStartCaptureError; accepted_path=`$acceptedPath; square_retry=`$false"
$text=Replace-One $text $oldDispatchEvent $newDispatchEvent 'CC dispatch worker StartTime evidence'

# Repair 2b: worker identity is three-state. UNKNOWN is not DEAD/MISMATCH.
$oldIdentity=As-Lf @'
                    $workerPid = [int](Safe-Property $state 'active_worker_pid' 0)
                    $storedWorkerStartText = [string](Safe-Property $state 'active_worker_start_time_utc' '')
                    $workerIdentityMatch = $false
                    if ($workerPid -gt 0 -and -not [string]::IsNullOrWhiteSpace($storedWorkerStartText)) {
                        $storedWorkerStart = [DateTime]::MinValue
                        if ([DateTime]::TryParse($storedWorkerStartText,[ref]$storedWorkerStart)) {
                            try {
                                $workerProcess = Get-Process -Id $workerPid -ErrorAction Stop
                                $workerIdentityMatch = ($workerProcess.StartTime.ToUniversalTime().Ticks -eq $storedWorkerStart.ToUniversalTime().Ticks)
                            }
                            catch { $workerIdentityMatch = $false }
                        }
                    }

                    if ($workerIdentityMatch -and $elapsedMinutes -le 30) {
                        if ([string](Safe-Property $state 'active_dispatch_phase' '') -ne 'LATE_WORKER') {
                            $state.active_dispatch_phase = 'LATE_WORKER'
                            [void](Set-CcWriteRelayState $state)
                            [void](Write-CcWriteRelayLedgerEvent 'CC_WRITE_RELAY_WORKER_BEYOND_GRACE' ([pscustomobject]@{
                                request_id=$active
                                worker_pid=$workerPid
                                worker_start_time_utc=$storedWorkerStart.ToUniversalTime().ToString('o')
                                elapsed_minutes=[math]::Round($elapsedMinutes,2)
                                hard_ceiling_minutes=30
                                meaning='SAME_WORKER_STILL_RUNNING_NOT_OUTCOME_UNKNOWN'
                                square_retry=$false
                            }))
                        }
                        return
                    }

                    if ($workerIdentityMatch -and $elapsedMinutes -gt 30) {
                        [void](Write-CcWriteRelayLedgerEvent 'CC_WRITE_RELAY_WORKER_HARD_CEILING_REACHED' ([pscustomobject]@{
                            request_id=$active
                            worker_pid=$workerPid
                            worker_start_time_utc=$storedWorkerStart.ToUniversalTime().ToString('o')
                            elapsed_minutes=[math]::Round($elapsedMinutes,2)
                            hard_ceiling_minutes=30
                            worker_may_still_be_running=$true
                            meaning='NO_RETRY_AMBIGUITY_PATH_REQUIRED_AFTER_BOUNDED_LATE_WINDOW'
                            square_retry=$false
                        }))
                    }
                    elseif ($workerPid -gt 0 -and -not $workerIdentityMatch) {
                        [void](Write-CcWriteRelayLedgerEvent 'CC_WRITE_RELAY_WORKER_IDENTITY_NOT_ESTABLISHED' ([pscustomobject]@{
                            request_id=$active
                            worker_pid=$workerPid
                            stored_worker_start_time_utc=if ([string]::IsNullOrWhiteSpace($storedWorkerStartText)) { $null } else { $storedWorkerStartText }
                            meaning='PID_ALONE_IS_NOT_WORKER_IDENTITY'
                            square_retry=$false
                        }))
                    }
'@
$newIdentity=As-Lf @'
                    $workerPid = [int](Safe-Property $state 'active_worker_pid' 0)
                    $storedWorkerStartText = [string](Safe-Property $state 'active_worker_start_time_utc' '')
                    $workerIdentityState = 'UNKNOWN'
                    $workerIdentityReason = 'START_TIME_NOT_CAPTURED'
                    $workerIdentityError = $null
                    $storedWorkerStart = [DateTime]::MinValue

                    if ($workerPid -le 0) {
                        $workerIdentityReason = 'WORKER_PID_NOT_AVAILABLE'
                    }
                    elseif ([string]::IsNullOrWhiteSpace($storedWorkerStartText)) {
                        $workerIdentityReason = 'START_TIME_NOT_CAPTURED'
                    }
                    elseif (-not [DateTime]::TryParse($storedWorkerStartText,[ref]$storedWorkerStart)) {
                        $workerIdentityReason = 'STORED_START_TIME_UNPARSEABLE'
                    }
                    else {
                        try {
                            $workerProcess = Get-Process -Id $workerPid -ErrorAction Stop
                            try {
                                $currentWorkerStart = $workerProcess.StartTime.ToUniversalTime()
                                if ($currentWorkerStart.Ticks -eq $storedWorkerStart.ToUniversalTime().Ticks) {
                                    $workerIdentityState = 'MATCH'
                                    $workerIdentityReason = 'PID_AND_START_TIME_MATCH'
                                }
                                else {
                                    $workerIdentityState = 'MISMATCH'
                                    $workerIdentityReason = 'PID_REUSED_OR_DIFFERENT_PROCESS'
                                }
                            }
                            catch {
                                $workerIdentityState = 'UNKNOWN'
                                $workerIdentityReason = 'CURRENT_START_TIME_UNREADABLE'
                                $workerIdentityError = $_.Exception.Message
                            }
                        }
                        catch {
                            $workerIdentityState = 'UNKNOWN'
                            $workerIdentityReason = 'PROCESS_LOOKUP_FAILED'
                            $workerIdentityError = $_.Exception.Message
                        }
                    }

                    if ($elapsedMinutes -gt 30 -and @('MATCH','UNKNOWN') -contains $workerIdentityState) {
                        [void](Write-CcWriteRelayLedgerEvent 'CC_WRITE_RELAY_WORKER_HARD_CEILING_REACHED' ([pscustomobject]@{
                            request_id=$active
                            worker_pid=$workerPid
                            worker_identity_state=$workerIdentityState
                            worker_identity_reason=$workerIdentityReason
                            worker_identity_error=$workerIdentityError
                            stored_worker_start_time_utc=if ([string]::IsNullOrWhiteSpace($storedWorkerStartText)) { $null } else { $storedWorkerStartText }
                            elapsed_minutes=[math]::Round($elapsedMinutes,2)
                            hard_ceiling_minutes=30
                            worker_may_still_be_running=($workerIdentityState -ne 'MISMATCH')
                            meaning='NO_RETRY_AMBIGUITY_PATH_REQUIRED_AFTER_BOUNDED_LATE_WINDOW'
                            square_retry=$false
                        }))
                    }
                    elseif ($workerIdentityState -eq 'MISMATCH') {
                        [void](Write-CcWriteRelayLedgerEvent 'CC_WRITE_RELAY_WORKER_IDENTITY_MISMATCH' ([pscustomobject]@{
                            request_id=$active
                            worker_pid=$workerPid
                            worker_identity_state=$workerIdentityState
                            worker_identity_reason=$workerIdentityReason
                            stored_worker_start_time_utc=$storedWorkerStart.ToUniversalTime().ToString('o')
                            meaning='PID_PRESENT_BUT_NOT_ORIGINAL_WORKER'
                            square_retry=$false
                        }))
                    }
'@
$text=Replace-One $text $oldIdentity $newIdentity 'CC tri-state worker identity'

# Re-read terminal status before bounded waiting. Only if no terminal status is
# recoverable do MATCH and UNKNOWN stay live until the existing 30-minute ceiling.
$anchorTail=As-Lf @'
                            }
                        }
                    }

                    $lastWorkerStatus = $null
                    $lastWorkerStatusReadError = $lateStatusReadError
'@
$replacementTail=As-Lf @'
                            }
                        }
                    }

                    if ($elapsedMinutes -le 30 -and @('MATCH','UNKNOWN') -contains $workerIdentityState) {
                        $desiredPhase = if ($workerIdentityState -eq 'MATCH') { 'LATE_WORKER' } else { 'LATE_WORKER_IDENTITY_UNKNOWN' }
                        if ([string](Safe-Property $state 'active_dispatch_phase' '') -ne $desiredPhase) {
                            $state.active_dispatch_phase = $desiredPhase
                            [void](Set-CcWriteRelayState $state)
                            [void](Write-CcWriteRelayLedgerEvent 'CC_WRITE_RELAY_WORKER_BEYOND_GRACE' ([pscustomobject]@{
                                request_id=$active
                                worker_pid=$workerPid
                                worker_identity_state=$workerIdentityState
                                worker_identity_reason=$workerIdentityReason
                                worker_identity_error=$workerIdentityError
                                stored_worker_start_time_utc=if ([string]::IsNullOrWhiteSpace($storedWorkerStartText)) { $null } else { $storedWorkerStartText }
                                elapsed_minutes=[math]::Round($elapsedMinutes,2)
                                hard_ceiling_minutes=30
                                meaning=if ($workerIdentityState -eq 'MATCH') { 'SAME_WORKER_STILL_RUNNING_NOT_OUTCOME_UNKNOWN' } else { 'WORKER_IDENTITY_UNKNOWN_NOT_DEAD' }
                                square_retry=$false
                            }))
                        }
                        return
                    }

                    $lastWorkerStatus = $null
                    $lastWorkerStatusReadError = $lateStatusReadError
'@
$text=Replace-One $text $anchorTail $replacementTail 'CC bounded wait after terminal status re-read'

foreach ($required in @(
    '[System.IO.File]::Replace($tempPath,$statusPath,[NullString]::Value)',
    "worker_start_time_capture_error=`$workerStartCaptureError",
    "`$workerIdentityState = 'UNKNOWN'",
    "meaning='WORKER_IDENTITY_UNKNOWN_NOT_DEAD'",
    "meaning='PID_PRESENT_BUT_NOT_ORIGINAL_WORKER'",
    "meaning='RETRIEVAL_FAILED_NOT_STATUS_ABSENT'",
    "if (@(`$Action.PSObject.Properties.Name) -contains 'closes_correction_debt_id') { throw 'CC REMOTE ROUTINE REFUSED: correction-debt closure is outside this lane.' }"
)) {
    if (-not $text.Contains($required)) { throw "REFUSED: post-patch invariant missing: $required. Nothing changed." }
}
if ($text.Contains('[System.IO.File]::Replace($tempPath,$statusPath,$null)')) {
    throw 'REFUSED: broken File.Replace null binding still present. Nothing changed.'
}

New-Item -ItemType Directory -Force -Path $UpdatesDir | Out-Null
$stamp=[DateTime]::UtcNow.ToString('yyyyMMdd_HHmmss')
$staged=Join-Path $UpdatesDir ("Campfire-Square.CC-WRITE-HOTFIX2-REPAIR.$stamp.ps1")
$backup=Join-Path $AppDir ("Campfire-Square.BEFORE-CC-WRITE-HOTFIX2-REPAIR.$stamp.ps1")
[IO.File]::WriteAllText($staged,$text,[Text.UTF8Encoding]::new($false))

$tokens=$null; $parseErrors=$null
[void][System.Management.Automation.Language.Parser]::ParseFile($staged,[ref]$tokens,[ref]$parseErrors)
if (@($parseErrors).Count -gt 0) {
    $detail=@($parseErrors | ForEach-Object { $_.Message }) -join '; '
    throw "REFUSED: staged source parse failed: $detail. Nothing installed."
}

Copy-Item -LiteralPath $Installed -Destination $backup -Force
if ((Get-Sha256File $backup) -ne $beforeSha) { throw 'REFUSED: exact backup hash mismatch. Nothing installed.' }
$targetSha=Get-Sha256File $staged
$targetBytes=(Get-Item -LiteralPath $staged).Length
Copy-Item -LiteralPath $staged -Destination $Installed -Force
$afterSha=Get-Sha256File $Installed
$afterBytes=(Get-Item -LiteralPath $Installed).Length
if ($afterSha -ne $targetSha -or $afterBytes -ne $targetBytes) {
    Copy-Item -LiteralPath $backup -Destination $Installed -Force
    throw 'INSTALL FAILED: post-copy identity mismatch. Exact Hotfix-2 backup restored.'
}

Write-Host ''
Write-Host 'CC CAMPFIRE WRITE HOTFIX 2 REPAIR INSTALLED'
Write-Host "before sha256 : $beforeSha"
Write-Host "after sha256  : $afterSha"
Write-Host "after bytes   : $afterBytes"
Write-Host "backup        : $backup"
Write-Host "staged source : $staged"
Write-Host ''
Write-Host 'Changed: genuine null for atomic File.Replace; explicit StartTime capture evidence; MATCH/MISMATCH/UNKNOWN worker identity.'
Write-Host 'Unchanged: correction debts, witness investigations, grants, quotas, authority, correction-debt closure rules.'
Write-Host 'This installer performs no Square write. CC routine writes remain obligation-gated.'
Write-Host 'Close and reopen Campfire Square if it was running while this patch was installed.'
