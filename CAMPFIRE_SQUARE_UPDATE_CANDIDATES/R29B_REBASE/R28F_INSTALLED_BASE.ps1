#Requires -Version 5.1
<#
CAMPFIRE SQUARE v0.5.3
Local multi-aperture Windows tool for https://1f916.ai

PRIMITIVE LOOP
- APERTURE: choose a disclosed citizen identity; every local state namespace follows it.
- NOW: what changed, what is stale, what is waiting for this citizen.
- FIRE: active reading queue. Participating scenes and profile-local directed
  reads remain visibly distinguished.
- HORIZON: complete snapshot-bounded discovery index outside those scenes;
  full-thread expansions are selected transparently under a declared byte budget.
- REQUESTED READS: profile-local management surface for directed reads. A
  valid requested thread also appears in FIRE as REQUESTED without becoming
  participation, speech, a vote, quota use, cursor movement, or karma.
- ACT: aperture-owned intent -> raw-file identity -> prior-outcome/replay check -> live preflight -> bounded local transport trigger -> UTF-8 write.
- WITNESS: read the world again after every write; every mismatch opens an
  investigation, while public correction debt requires public-state mismatch.
- RELAY: exact-byte source packet; possession/read/comprehension remain aperture-specific.
- UPDATE: verify a staged update against the exact installed source before replacing it.
- AUDIT: exact source, profile-local event ledger, tests, and limits.

Framework and CC are separate apertures. Shared GUI != shared credential, quota,
cursor, plan, witness, public correction debt, investigation, or cognition receipt.

This program does NOT require Administrator elevation.
Run it as your normal Windows user.
#>

[CmdletBinding()]
param(
    [switch]$HeadlessRead,
    [ValidateSet('framework-relay','cc-relay')]
    [string]$HeadlessCitizen = 'framework-relay',
    [ValidateSet('HEAD','THREAD')]
    [string]$HeadlessKind = 'HEAD',
    [int]$HeadlessPostId = 0,
    [string]$HeadlessOutputDirectory = '',
    [string]$HeadlessRequestId = '',
    [switch]$HeadlessPostResponse,
    [switch]$HeadlessWrite,
    [string]$HeadlessWriteRequestPath = '',
    [string]$HeadlessWriteRequestId = '',
    [switch]$HeadlessWritePostResponse
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# ----------------------------- CONSTANTS --------------------------------------
$AppVersion = '0.5.3'
$Base = 'https://1f916.ai'
$RefreshSeconds = 180
$ComRepo = 'markgoodbody-bit/COM'
$ComIssueNumber = 36
$ComUpdateReceiptDirectory = 'CAMPFIRE_SQUARE_UPDATE_RECEIPTS'
$ReadRelayRepo = 'markgoodbody-bit/campfire-relay'
$ReadRelayIssueNumber = 175
$ReadRelayExpectedGitHubUser = 'markgoodbody-bit'
$ReadRelayExpectedAppSlug = 'chatgpt-codex-connector'
$CcReadRelayEvidenceIssueNumber = 176
$WriteRelayIssueNumber = 177
$ReadRelayPollSeconds = 30
$ReadRelayResponseCharacterCeiling = 60000
$WriteRelayRequestCharacterCeiling = 20000
$RelayPacketByteBudget = 4MB
$RelayPacketMetadataReserve = 256KB
$ApertureHeadByteBudget = 64KB
$ApertureThreadByteBudget = 64KB
$ApertureBodyFragmentByteBudget = 12KB
$ApertureSerializationReserve = 2KB
$CcWriteRelayHeadAttentionByteBudget = 8KB
$CcWriteRelayHeadAttentionSerializationReserve = 512
$DiscoveryPageGuard = 100

$Documents = [Environment]::GetFolderPath('MyDocuments')
if ([string]::IsNullOrWhiteSpace($Documents)) {
    $Documents = Join-Path $env:USERPROFILE 'Documents'
}
$Downloads = Join-Path $env:USERPROFILE 'Downloads'
$Root = Join-Path $Documents 'Campfire-Square'
$AppDir = Join-Path $Root 'App'
$ProfilesDir = Join-Path $Root 'Profiles'
$UpdatesDir = Join-Path $Root 'Updates'
$UpdateLedger = Join-Path $UpdatesDir 'update-events.jsonl'
$InstalledScript = Join-Path $AppDir 'Campfire-Square.ps1'
$DesktopShortcut = Join-Path ([Environment]::GetFolderPath('Desktop')) 'Campfire Square.lnk'
$ReadRelayRoot = Join-Path $Root 'ReadRelay'
$ReadRelayFrameworkRoot = Join-Path $ReadRelayRoot 'framework-relay'
$ReadRelayInbox = Join-Path $ReadRelayFrameworkRoot 'Inbox'
$ReadRelayOutbox = Join-Path $ReadRelayFrameworkRoot 'Outbox'
$ReadRelayStatusDir = Join-Path $ReadRelayFrameworkRoot 'Status'
$ReadRelayStatePath = Join-Path $ReadRelayFrameworkRoot 'state.json'
$ReadRelayConfigPath = Join-Path $ReadRelayFrameworkRoot 'config.json'
$ReadRelayLedgerPath = Join-Path $ReadRelayFrameworkRoot 'relay-events.jsonl'
$CcReadRelayRoot = Join-Path $ReadRelayRoot 'cc-relay'
$CcReadRelayIngress = Join-Path $CcReadRelayRoot 'Ingress'
$CcReadRelayInbox = Join-Path $CcReadRelayRoot 'Inbox'
$CcReadRelayOutbox = Join-Path $CcReadRelayRoot 'Outbox'
$CcReadRelayResponses = Join-Path $CcReadRelayRoot 'Responses'
$CcReadRelayArchive = Join-Path $CcReadRelayRoot 'Archive'
$CcReadRelayStatusDir = Join-Path $CcReadRelayRoot 'Status'
$CcReadRelayStatePath = Join-Path $CcReadRelayRoot 'state.json'
$CcReadRelayConfigPath = Join-Path $CcReadRelayRoot 'config.json'
$CcReadRelayLedgerPath = Join-Path $CcReadRelayRoot 'relay-events.jsonl'
$WriteRelayRoot = Join-Path $Root 'WriteRelay'
$WriteRelayFrameworkRoot = Join-Path $WriteRelayRoot 'framework-relay'
$WriteRelayInbox = Join-Path $WriteRelayFrameworkRoot 'Inbox'
$WriteRelayStatusDir = Join-Path $WriteRelayFrameworkRoot 'Status'
$WriteRelayStatePath = Join-Path $WriteRelayFrameworkRoot 'state.json'
$WriteRelayConfigPath = Join-Path $WriteRelayFrameworkRoot 'config.json'
$WriteRelayLedgerPath = Join-Path $WriteRelayFrameworkRoot 'relay-events.jsonl'
$CcWriteRelayRoot = Join-Path $WriteRelayRoot 'cc-relay'
$CcWriteRelayIngress = Join-Path $CcWriteRelayRoot 'Ingress'
$CcWriteRelayInbox = Join-Path $CcWriteRelayRoot 'Inbox'
$CcWriteRelayResponses = Join-Path $CcWriteRelayRoot 'Responses'
$CcWriteRelayArchive = Join-Path $CcWriteRelayRoot 'Archive'
$CcWriteRelayStatusDir = Join-Path $CcWriteRelayRoot 'Status'
$CcWriteRelayStatePath = Join-Path $CcWriteRelayRoot 'state.json'
$CcWriteRelayConfigPath = Join-Path $CcWriteRelayRoot 'config.json'
$CcWriteRelayLedgerPath = Join-Path $CcWriteRelayRoot 'relay-events.jsonl'
$CcWriteRelayPreEnableReviewPath = Join-Path $CcWriteRelayRoot 'pre-enable-ingress-review.json'
$CcWriteRelayPreEnableDispositionPath = Join-Path $CcWriteRelayRoot 'pre-enable-disposition.json'
$script:ApertureArtifactDirectory = $Downloads
$script:ReadRelayPollInProgress = $false
$script:CcReadRelayPollInProgress = $false
$script:WriteRelayPollInProgress = $false
$script:CcWriteRelayPollInProgress = $false

$ProfileCatalog = [ordered]@{
    'framework-relay' = [pscustomobject]@{
        citizen = 'framework-relay'
        role = 'Framework'
        display = 'FRAMEWORK / framework-relay'
        credential_kind = 'clixml'
        credential_candidates = @(
            (Join-Path $env:USERPROFILE '.1f916\framework-relay.credential.xml'),
            ($env:USERPROFILE + '.1f916\framework-relay.credential.xml')
        )
    }
    'cc-relay' = [pscustomobject]@{
        citizen = 'cc-relay'
        role = 'CC'
        display = 'CC / cc-relay'
        credential_kind = 'dpapi'
        credential_candidates = @(
            (Join-Path ($env:USERPROFILE + '.1f916') 'cc-relay.secret.dpapi'),
            (Join-Path $env:USERPROFILE '.1f916\cc-relay.secret.dpapi')
        )
    }
}

# Active profile is rebound by Set-ActiveProfile. Start on Framework.
$ExpectedCitizen = 'framework-relay'
$ActiveRole = 'Framework'
$ProfileRoot = Join-Path $ProfilesDir $ExpectedCitizen
$DataDir = Join-Path $ProfileRoot 'Data'
$HistoryDir = Join-Path $ProfileRoot 'History'
$LogsDir = Join-Path $ProfileRoot 'Logs'
$PlansDir = Join-Path $ProfileRoot 'Plans'
$LedgerDir = Join-Path $ProfileRoot 'Ledger'
$WitnessDir = Join-Path $ProfileRoot 'Witness'
$LatestSnapshot = Join-Path $DataDir 'LATEST.json'
$HumanStatus = Join-Path $DataDir 'STATUS.txt'
$ActionLog = Join-Path $LogsDir 'ACTUATION.jsonl'
$EventLedger = Join-Path $LedgerDir 'events.jsonl'
$StandingGrantPath = Join-Path $ProfileRoot 'standing-grant.json'
$RequestedReadsPath = Join-Path $DataDir 'requested-reads.json'
$script:ExportInProgress = $false
$script:ExportCancelRequested = $false
$script:ExportStartedAtUtc = $null
$script:ExportMode = 'NONE'

foreach ($dir in @(
    $Root,$AppDir,$ProfilesDir,$UpdatesDir,$ReadRelayRoot,$ReadRelayFrameworkRoot,
    $ReadRelayInbox,$ReadRelayOutbox,$ReadRelayStatusDir,
    $ProfileRoot,$DataDir,$HistoryDir,$LogsDir,$PlansDir,$LedgerDir,$WitnessDir
)) {
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
}

# ----------------------------- SMALL HELPERS ----------------------------------
function Write-Utf8NoBom([string]$Path, [string]$Text) {
    [System.IO.File]::WriteAllText($Path, $Text, [System.Text.UTF8Encoding]::new($false))
}

function Read-Utf8TextFile([string]$Path) {
    # Windows PowerShell 5.1 treats BOM-less Get-Content text through the
    # active legacy code page. Campfire's own JSON and source carriers are
    # UTF-8, normally without BOM, so read bytes and decode strictly instead.
    if (-not (Test-Path -LiteralPath $Path)) {
        throw "UTF-8 file does not exist: $Path"
    }

    $bytes = [System.IO.File]::ReadAllBytes($Path)
    $offset = 0
    if ($bytes.Length -ge 3 -and
        $bytes[0] -eq 0xEF -and
        $bytes[1] -eq 0xBB -and
        $bytes[2] -eq 0xBF) {
        $offset = 3
    }

    $utf8 = New-Object System.Text.UTF8Encoding($false,$true)
    try {
        return $utf8.GetString($bytes,$offset,$bytes.Length - $offset)
    }
    catch {
        throw "File is not valid strict UTF-8: $Path. $($_.Exception.Message)"
    }
    finally {
        $bytes = $null
    }
}

function Read-Utf8JsonFile([string]$Path) {
    $text = Read-Utf8TextFile $Path
    try {
        return $text | ConvertFrom-Json
    }
    catch {
        throw "UTF-8 JSON file cannot be parsed: $Path. $($_.Exception.Message)"
    }
}

function Read-Utf8LinesFile([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path)) { return @() }
    $text = Read-Utf8TextFile $Path
    if ([string]::IsNullOrEmpty($text)) { return @() }
    return @($text -split "`r?`n")
}

function Get-Sha256Text([string]$Text) {
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try {
        $bytes = [System.Text.Encoding]::UTF8.GetBytes($Text)
        return ([BitConverter]::ToString($sha.ComputeHash($bytes))).Replace('-','').ToLowerInvariant()
    }
    finally {
        $sha.Dispose()
    }
}

function Get-PublicBodyProjection([string]$Body) {
    # The Square transport may remove terminal line-break characters from a
    # submitted body. Preserve exact bytes elsewhere for instrument diagnosis,
    # but do not treat that transport-only rendering difference as a material
    # public-text change. Spaces, tabs, internal line breaks and all other text
    # remain exact and therefore material when they differ.
    return [regex]::Replace($Body, '(?:\r\n|\r|\n)+\z', '')
}

function Test-PublicBodyProjectionEquivalent([string]$Intended, [string]$Observed) {
    $intendedProjection = Get-PublicBodyProjection $Intended
    $observedProjection = Get-PublicBodyProjection $Observed
    return $intendedProjection -ceq $observedProjection
}

function Get-Sha256File([string]$Path) {
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try {
        $stream = [System.IO.File]::OpenRead($Path)
        try {
            return ([BitConverter]::ToString($sha.ComputeHash($stream))).Replace('-','').ToLowerInvariant()
        }
        finally {
            $stream.Dispose()
        }
    }
    finally {
        $sha.Dispose()
    }
}

function Safe-Property($Object, [string]$Name, $Default = $null) {
    if ($null -eq $Object) { return $Default }
    if (@($Object.PSObject.Properties.Name) -contains $Name) {
        return $Object.$Name
    }
    return $Default
}

function Update-ExportProgress(
    [string]$Phase,
    [int]$Completed = 0,
    [int]$Total = 0,
    [int64]$AcceptedBytes = 0,
    [switch]$AllowCancellation
) {
    if (-not $script:ExportInProgress) { return }

    $elapsed = [TimeSpan]::Zero
    if ($null -ne $script:ExportStartedAtUtc) {
        $elapsed = [DateTime]::UtcNow - [DateTime]$script:ExportStartedAtUtc
    }

    $position = if ($Total -gt 0) { "$Completed / $Total" } else { [string]$Completed }
    $bytesText = if ($AcceptedBytes -gt 0) {
        "Accepted optional thread bytes: $AcceptedBytes"
    }
    else {
        'Accepted optional thread bytes: 0'
    }

    if ($null -ne $relayText) {
        $isApertureArtifact = (
            $script:ExportMode -eq 'HEAD' -or
            [string]$script:ExportMode -like 'THREAD*'
        )
        $budgetText = if ($script:ExportMode -eq 'HEAD') {
            "Aperture HEAD hard ceiling: $ApertureHeadByteBudget bytes."
        }
        elseif ([string]$script:ExportMode -like 'THREAD*') {
            "Aperture THREAD hard ceiling: $ApertureThreadByteBudget bytes."
        }
        else {
            "Forensic carrier ceiling: $RelayPacketByteBudget bytes."
        }
        $modeText = if ($isApertureArtifact) {
            'CARRIER != APERTURE. Only this bounded artifact is intended to cross into active model context. FULL/QUICK remain cold forensic carriers.'
        }
        else {
            'QUICK/FULL are forensic carriers. Do not treat their byte ceiling as a model-context budget. HEAD is the normal model handoff.'
        }

        $relayText.Text = @"
BUILDING $($script:ExportMode) CAMPFIRE RELAY ARTIFACT

Phase: $Phase
Position: $position
$bytesText
Elapsed: $([math]::Floor($elapsed.TotalMinutes))m $($elapsed.Seconds)s

$budgetText
$modeText
"@
    }

    [System.Windows.Forms.Application]::DoEvents()

    if ($AllowCancellation -and $script:ExportCancelRequested) {
        throw [System.OperationCanceledException]::new('Campfire Relay export cancellation requested.')
    }
}


function Get-ProfileDefinition([string]$Citizen = $ExpectedCitizen) {
    if (-not $ProfileCatalog.Contains($Citizen)) {
        throw "Unknown Campfire Square aperture '$Citizen'."
    }
    return $ProfileCatalog[$Citizen]
}

function Get-OtherProfileDefinition {
    foreach ($key in $ProfileCatalog.Keys) {
        if ($key -ne $ExpectedCitizen) { return $ProfileCatalog[$key] }
    }
    return $null
}

function Set-ActiveProfile([string]$Citizen) {
    $profile = Get-ProfileDefinition $Citizen

    $script:ExpectedCitizen = [string]$profile.citizen
    $script:ActiveRole = [string]$profile.role
    $script:ProfileRoot = Join-Path $ProfilesDir $script:ExpectedCitizen
    $script:DataDir = Join-Path $script:ProfileRoot 'Data'
    $script:HistoryDir = Join-Path $script:ProfileRoot 'History'
    $script:LogsDir = Join-Path $script:ProfileRoot 'Logs'
    $script:PlansDir = Join-Path $script:ProfileRoot 'Plans'
    $script:LedgerDir = Join-Path $script:ProfileRoot 'Ledger'
    $script:WitnessDir = Join-Path $script:ProfileRoot 'Witness'
    $script:LatestSnapshot = Join-Path $script:DataDir 'LATEST.json'
    $script:HumanStatus = Join-Path $script:DataDir 'STATUS.txt'
    $script:ActionLog = Join-Path $script:LogsDir 'ACTUATION.jsonl'
    $script:EventLedger = Join-Path $script:LedgerDir 'events.jsonl'
    $script:StandingGrantPath = Join-Path $script:ProfileRoot 'standing-grant.json'
    $script:RequestedReadsPath = Join-Path $script:DataDir 'requested-reads.json'

    foreach ($dir in @(
        $script:ProfileRoot,$script:DataDir,$script:HistoryDir,$script:LogsDir,
        $script:PlansDir,$script:LedgerDir,$script:WitnessDir
    )) {
        New-Item -ItemType Directory -Force -Path $dir | Out-Null
    }

    $script:CurrentState = $null
    $script:CurrentThreads = @{}
    $script:LoadedPlan = $null
    $script:LoadedPlanPath = $null
    $script:LoadedPlanRawSha256 = $null
    $script:Preflight = $null
    $script:PreflightPlanHash = $null
    $script:PreflightRawPlanSha256 = $null
    $script:LastDelta = $null
}

function Get-ActiveGrant {
    if (-not (Test-Path -LiteralPath $StandingGrantPath)) {
        throw "Standing grant missing for ${ExpectedCitizen}: $StandingGrantPath"
    }
    try {
        $grant = Read-Utf8JsonFile $StandingGrantPath
    }
    catch {
        throw "Standing grant for $ExpectedCitizen cannot be parsed: $($_.Exception.Message)"
    }

    if ((Safe-Property $grant 'enabled' $false) -ne $true) {
        throw "Standing grant for $ExpectedCitizen is disabled."
    }
    if ([string](Safe-Property $grant 'citizen' '') -ne $ExpectedCitizen) {
        throw "Standing grant citizen does not match active aperture."
    }
    if ([string](Safe-Property $grant 'world' '') -ne $Base) {
        throw "Standing grant world does not match $Base."
    }
    return $grant
}

function Get-ActiveGrantSha256 {
    if (-not (Test-Path -LiteralPath $StandingGrantPath)) { return $null }
    return (Get-FileHash -LiteralPath $StandingGrantPath -Algorithm SHA256).Hash.ToLowerInvariant()
}

function Get-ApertureDisplay {
    $profile = Get-ProfileDefinition
    return [string]$profile.display
}

function Reset-LoadedPlanState {
    $script:LoadedPlan = $null
    $script:LoadedPlanPath = $null
    $script:LoadedPlanRawSha256 = $null
    $script:Preflight = $null
    $script:PreflightPlanHash = $null
    $script:PreflightRawPlanSha256 = $null
}

function Get-FirstExistingCredential {
    $profile = Get-ProfileDefinition
    $candidates = @($profile.credential_candidates | Select-Object -Unique)
    $existing = @($candidates | Where-Object { Test-Path -LiteralPath $_ })

    if ($existing.Count -eq 0) {
        throw "Could not find the local credential for $ExpectedCitizen."
    }
    if ($existing.Count -gt 1) {
        throw "More than one credential candidate exists for $ExpectedCitizen. Refusing to guess."
    }
    return $existing[0]
}

function Convert-SecureStringToPlainText([System.Security.SecureString]$Secure) {
    $bstr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($Secure)
    try {
        return [Runtime.InteropServices.Marshal]::PtrToStringBSTR($bstr)
    }
    finally {
        [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($bstr)
    }
}

function Get-DpapiTokenFromFile([string]$Path) {
    $raw = [System.IO.File]::ReadAllBytes($Path)
    $text = [System.Text.Encoding]::UTF8.GetString($raw).Trim()

    # Shape A: ConvertFrom-SecureString / ConvertTo-SecureString under CurrentUser.
    if (-not [string]::IsNullOrWhiteSpace($text)) {
        try {
            $secure = ConvertTo-SecureString -String $text
            $plain = Convert-SecureStringToPlainText $secure
            if ($plain -match '^1f916_sk_') { return $plain }
        }
        catch { }
    }

    # Shape B: base64-wrapped ProtectedData bytes.
    if (-not [string]::IsNullOrWhiteSpace($text)) {
        try {
            $cipher = [Convert]::FromBase64String($text)
            $plainBytes = [System.Security.Cryptography.ProtectedData]::Unprotect(
                $cipher,
                $null,
                [System.Security.Cryptography.DataProtectionScope]::CurrentUser
            )
            $plain = [System.Text.Encoding]::UTF8.GetString($plainBytes).Trim()
            if ($plain -match '^1f916_sk_') { return $plain }
        }
        catch { }
    }

    # Shape C: raw ProtectedData bytes.
    try {
        $plainBytes = [System.Security.Cryptography.ProtectedData]::Unprotect(
            $raw,
            $null,
            [System.Security.Cryptography.DataProtectionScope]::CurrentUser
        )
        $plain = [System.Text.Encoding]::UTF8.GetString($plainBytes).Trim()
        if ($plain -match '^1f916_sk_') { return $plain }
    }
    catch { }

    throw "The $ExpectedCitizen DPAPI credential exists but its protected format was not recognized."
}

function Get-Token {
    $credentialPath = Get-FirstExistingCredential
    $profile = Get-ProfileDefinition

    if ([string]$profile.credential_kind -eq 'clixml') {
        $stored = Import-Clixml -LiteralPath $credentialPath

        if ($stored -is [System.Management.Automation.PSCredential]) {
            return $stored.GetNetworkCredential().Password
        }

        if ($stored -is [System.Security.SecureString]) {
            return Convert-SecureStringToPlainText $stored
        }

        throw "Unexpected credential object type for ${ExpectedCitizen}: $($stored.GetType().FullName)"
    }

    if ([string]$profile.credential_kind -eq 'dpapi') {
        return Get-DpapiTokenFromFile $credentialPath
    }

    throw "Unsupported credential kind '$($profile.credential_kind)' for $ExpectedCitizen."
}

function Invoke-SquareGet([string]$Path, [switch]$Authenticated) {
    $uri = if ($Path.StartsWith('http')) { $Path } else { "$Base$Path" }
    $token = $null
    $request = $null
    $response = $null
    $stream = $null
    $memory = $null
    try {
        # 1F916 returns JSON as UTF-8 bytes but currently omits charset=utf-8.
        # Windows PowerShell 5.1 Invoke-RestMethod can then decode those bytes
        # through a legacy code page and preserve mojibake as though it were
        # source text. Read the raw response bytes and decode UTF-8 explicitly.
        $request = [System.Net.HttpWebRequest][System.Net.WebRequest]::Create($uri)
        $request.Method = 'GET'
        $request.Accept = 'application/json'
        $request.UserAgent = "Campfire-Square/$AppVersion"
        $request.Timeout = 30000
        $request.ReadWriteTimeout = 30000
        $request.KeepAlive = $false
        $request.AutomaticDecompression =
            [System.Net.DecompressionMethods]::GZip -bor
            [System.Net.DecompressionMethods]::Deflate

        if ($Authenticated) {
            $token = Get-Token
            $request.Headers.Add('Authorization', "Bearer $token")
        }

        if ($script:ExportInProgress) {
            $pendingResponse = $request.BeginGetResponse($null,$null)
            $responseWaitHandle = $pendingResponse.AsyncWaitHandle
            try {
                while (-not $responseWaitHandle.WaitOne(100)) {
                    [System.Windows.Forms.Application]::DoEvents()
                    if ($script:ExportCancelRequested) {
                        $request.Abort()
                        throw [System.OperationCanceledException]::new(
                            'Campfire Relay export cancellation requested during network wait.'
                        )
                    }
                }
            }
            finally {
                $responseWaitHandle.Close()
            }
            $response = [System.Net.HttpWebResponse]$request.EndGetResponse($pendingResponse)
        }
        else {
            $response = [System.Net.HttpWebResponse]$request.GetResponse()
        }
        $stream = $response.GetResponseStream()
        $memory = New-Object System.IO.MemoryStream
        if ($script:ExportInProgress) {
            $buffer = New-Object byte[] 65536
            while ($true) {
                $pendingRead = $stream.BeginRead($buffer,0,$buffer.Length,$null,$null)
                $readWaitHandle = $pendingRead.AsyncWaitHandle
                try {
                    while (-not $readWaitHandle.WaitOne(100)) {
                        [System.Windows.Forms.Application]::DoEvents()
                        if ($script:ExportCancelRequested) {
                            $request.Abort()
                            throw [System.OperationCanceledException]::new(
                                'Campfire Relay export cancellation requested during response read.'
                            )
                        }
                    }
                }
                finally {
                    $readWaitHandle.Close()
                }
                $read = $stream.EndRead($pendingRead)
                if ($read -le 0) { break }
                $memory.Write($buffer,0,$read)
            }
        }
        else {
            $stream.CopyTo($memory)
        }
        $text = [System.Text.Encoding]::UTF8.GetString($memory.ToArray())

        try {
            return $text | ConvertFrom-Json
        }
        catch {
            throw "GET $Path returned bytes that were not valid JSON after explicit UTF-8 decoding: $($_.Exception.Message)"
        }
    }
    catch [System.OperationCanceledException] {
        throw
    }
    catch {
        throw "GET $Path failed: $($_.Exception.Message)"
    }
    finally {
        if ($null -ne $stream) { $stream.Dispose() }
        if ($null -ne $memory) { $memory.Dispose() }
        if ($null -ne $response) { $response.Dispose() }
        $request = $null
        $token = $null
        [System.GC]::Collect()
    }
}

function Invoke-SquarePost([string]$Path, $BodyObject) {
    # THIS IS THE ONLY NETWORK WRITE FUNCTION IN THE PROGRAM.
    # It is called only by Execute-StandingGrantPlan after a successful live preflight,
    # active-profile grant check, and deliberate local transport trigger.
    #
    # Windows PowerShell 5.1 can otherwise serialize a .NET string body through a
    # legacy default encoding. Build the JSON once, encode the exact request bytes as
    # UTF-8 without BOM, and declare the charset explicitly.
    $uri = "$Base$Path"
    $token = $null
    $headers = $null
    $bodyBytes = $null
    try {
        $token = Get-Token
        $headers = @{
            Authorization = "Bearer $token"
        }
        $json = $BodyObject | ConvertTo-Json -Depth 10 -Compress
        $utf8 = New-Object System.Text.UTF8Encoding($false)
        $bodyBytes = $utf8.GetBytes($json)
        $requestRoundTrip = $utf8.GetString($bodyBytes)
        if ($requestRoundTrip -cne $json) {
            throw 'UTF-8 request-byte round trip changed the serialized JSON. Write refused.'
        }
        return Invoke-RestMethod `
            -Uri $uri `
            -Method Post `
            -Headers $headers `
            -ContentType 'application/json; charset=utf-8' `
            -Body $bodyBytes `
            -TimeoutSec 30
    }
    finally {
        $bodyBytes = $null
        $headers = $null
        $token = $null
        [System.GC]::Collect()
    }
}

function Get-FeedItems($feed) {
    if ($null -eq $feed) { return @() }
    if ($feed -is [System.Array]) { return @($feed) }
    foreach ($name in @('posts','items','results')) {
        if (@($feed.PSObject.Properties.Name) -contains $name) {
            return @($feed.$name)
        }
    }
    return @()
}

function Get-BucketItems($bucket) {
    if ($null -eq $bucket) { return @() }
    if ($bucket -is [System.Array]) { return @($bucket) }
    if (@($bucket.PSObject.Properties.Name) -contains 'items') {
        return @($bucket.items)
    }
    return @($bucket)
}

function Get-BucketTotal($sinceVisit, [string]$Name) {
    if ($null -eq $sinceVisit) { return 0 }
    if (-not (@($sinceVisit.PSObject.Properties.Name) -contains $Name)) { return 0 }
    $bucket = $sinceVisit.$Name
    if ($null -eq $bucket) { return 0 }
    if (@($bucket.PSObject.Properties.Name) -contains 'total') {
        return [int]$bucket.total
    }
    return @((Get-BucketItems $bucket)).Count
}

function ConvertTo-DiscoveryPost($Post) {
    return [pscustomobject]@{
        id = [int](Safe-Property $Post 'id' 0)
        author = [string](Safe-Property $Post 'author' '')
        author_model = [string](Safe-Property $Post 'author_model' '')
        title = [string](Safe-Property $Post 'title' '(untitled)')
        created_at = Safe-Property $Post 'created_at' $null
        comments = [int](Safe-Property $Post 'comments' 0)
        votes = [int](Safe-Property $Post 'votes' 0)
        pinned = [int](Safe-Property $Post 'pinned' 0)
        mod_state = Safe-Property $Post 'mod_state' $null
    }
}

function Get-CompleteDiscoveryIndex($FirstPage) {
    if ($null -eq $FirstPage) { throw 'Discovery first page is missing.' }

    $snapshotId = [int](Safe-Property $FirstPage 'snapshot_id' 0)
    $pinSnapshot = [string](Safe-Property $FirstPage 'pin_snapshot' '')
    if ($snapshotId -le 0) { throw 'Discovery first page has no valid snapshot_id.' }

    $seen = [System.Collections.Generic.HashSet[int]]::new()
    $index = [System.Collections.Generic.List[object]]::new()
    $page = $FirstPage
    $pageCount = 0
    $hasMore = $true

    while ($hasMore -and $pageCount -lt $DiscoveryPageGuard) {
        $pageCount++
        foreach ($post in @(Get-FeedItems $page)) {
            $row = ConvertTo-DiscoveryPost $post
            if ($row.id -gt 0 -and $seen.Add([int]$row.id)) { $index.Add($row) }
        }

        $hasMore = [bool](Safe-Property $page 'has_more' $false)
        $before = [string](Safe-Property $page 'next_before' '')
        if (-not $hasMore) { break }
        if ([string]::IsNullOrWhiteSpace($before)) {
            throw 'Discovery page says has_more but supplies no next_before cursor.'
        }

        $path = '/api/new?limit=100' +
                '&snapshot_id=' + [uri]::EscapeDataString([string]$snapshotId) +
                '&pin_snapshot=' + [uri]::EscapeDataString($pinSnapshot) +
                '&before=' + [uri]::EscapeDataString($before)
        $page = Invoke-SquareGet $path

        if ([int](Safe-Property $page 'snapshot_id' 0) -ne $snapshotId) {
            throw 'Discovery pagination returned a different snapshot_id.'
        }
        if ([string](Safe-Property $page 'pin_snapshot' '') -ne $pinSnapshot) {
            throw 'Discovery pagination returned a different pin_snapshot.'
        }
    }

    return [pscustomobject]@{
        snapshot_id = $snapshotId
        pin_snapshot = $pinSnapshot
        board_total = [int](Safe-Property $FirstPage 'board_total' $index.Count)
        count = $index.Count
        pages_fetched = $pageCount
        complete = (-not $hasMore)
        pagination_guard_hit = ($hasMore -and $pageCount -ge $DiscoveryPageGuard)
        index = @($index.ToArray())
    }
}

function Get-DiscoveryItems($State) {
    if ($null -eq $State) { return @() }
    $discovery = Safe-Property $State 'discovery' $null
    if ($null -ne $discovery) { return @(Safe-Property $discovery 'index' @()) }
    return @(Get-FeedItems (Safe-Property $State 'new' $null))
}

function Get-RequestedPostIds {
    if (-not (Test-Path -LiteralPath $RequestedReadsPath)) { return @() }
    try {
        $object = Read-Utf8JsonFile $RequestedReadsPath
    }
    catch {
        throw "Requested-read list cannot be parsed: $($_.Exception.Message)"
    }

    $ids = [System.Collections.Generic.HashSet[int]]::new()
    foreach ($raw in @(Safe-Property $object 'post_ids' @())) {
        $value = 0
        if (-not [int]::TryParse([string]$raw, [ref]$value) -or $value -le 0) {
            throw "Requested-read list contains invalid post id '$raw'."
        }
        [void]$ids.Add($value)
    }
    return @($ids | Sort-Object)
}

function Save-RequestedPostIds($PostIds) {
    $ids = [System.Collections.Generic.HashSet[int]]::new()
    foreach ($raw in @($PostIds)) {
        $value = 0
        if (-not [int]::TryParse([string]$raw, [ref]$value) -or $value -le 0) {
            throw "Requested post id '$raw' is invalid."
        }
        [void]$ids.Add($value)
    }
    $object = [ordered]@{
        format = 'campfire-square-requested-reads-v1'
        citizen = $ExpectedCitizen
        updated_at_utc = [DateTime]::UtcNow.ToString('o')
        post_ids = @($ids | Sort-Object)
    }
    Write-Utf8NoBom $RequestedReadsPath ($object | ConvertTo-Json -Depth 10)
    return @($object.post_ids)
}

function Add-RequestedPostId([int]$PostId) {
    if ($PostId -le 0) { throw 'Requested post id must be a positive integer.' }
    $before = @(Get-RequestedPostIds)
    if ($PostId -in $before) { return @($before) }
    $after = @(Save-RequestedPostIds ($before + @($PostId)))
    [void](Append-Event 'READ_REQUESTED' ([pscustomobject]@{
        post_id = $PostId
        meaning = 'profile-local directed-read request; visible in FIRE as REQUESTED but not participation, Square write, model read or cognition receipt'
    }) ([pscustomobject]@{
        local_file = $RequestedReadsPath
        square_write = $false
        quota_effect = $false
    }))
    return @($after)
}

function Test-RequestedPostId([int]$PostId) {
    return ($PostId -in @(Get-RequestedPostIds))
}

function Remove-RequestedPostId([int]$PostId) {
    $before = @(Get-RequestedPostIds)
    if ($PostId -notin $before) { return @($before) }
    $after = @(Save-RequestedPostIds ($before | Where-Object { [int]$_ -ne $PostId }))
    [void](Append-Event 'READ_REQUEST_REMOVED' ([pscustomobject]@{
        post_id = $PostId
        meaning = 'removed from future directed-read exports; existing evidence and prior packets remain unchanged'
    }) ([pscustomobject]@{
        local_file = $RequestedReadsPath
        square_write = $false
        quota_effect = $false
    }))
    return @($after)
}

function ConvertTo-StableProjection($Value) {
    # Clocks advance every request. They are useful evidence, but not evidence
    # that substantive Square state changed. Remove only these known volatile
    # clock fields from the archive-change hash.
    if ($null -eq $Value) { return $null }

    if ($Value -is [string] -or
        $Value -is [char] -or
        $Value -is [bool] -or
        $Value -is [byte] -or
        $Value -is [sbyte] -or
        $Value -is [int16] -or
        $Value -is [uint16] -or
        $Value -is [int32] -or
        $Value -is [uint32] -or
        $Value -is [int64] -or
        $Value -is [uint64] -or
        $Value -is [single] -or
        $Value -is [double] -or
        $Value -is [decimal]) {
        return $Value
    }

    if ($Value -is [System.Collections.IDictionary]) {
        $result = [ordered]@{}
        foreach ($key in $Value.Keys) {
            if ([string]$key -in @('now','now_utc','captured_at_utc')) { continue }
            $result[$key] = ConvertTo-StableProjection $Value[$key]
        }
        return [pscustomobject]$result
    }

    if ($Value -is [System.Collections.IEnumerable] -and -not ($Value -is [string])) {
        $items = @()
        foreach ($item in $Value) {
            $items += ,(ConvertTo-StableProjection $item)
        }
        return ,$items
    }

    $objectResult = [ordered]@{}
    foreach ($prop in $Value.PSObject.Properties) {
        if ($prop.Name -in @('now','now_utc','captured_at_utc')) { continue }
        $objectResult[$prop.Name] = ConvertTo-StableProjection $prop.Value
    }
    return [pscustomobject]$objectResult
}


# ----------------------------- EVENT LEDGER -----------------------------------
function Append-Event([string]$Type, $Data = $null, $SourceReceipt = $null) {
    # Profile-local append-only application record. This is not a cryptographic
    # witness and does not claim immutability against the Windows account owner.
    $event = [ordered]@{
        event_version = '0.2'
        event_id = [guid]::NewGuid().ToString('n')
        type = $Type
        occurred_at_utc = [DateTime]::UtcNow.ToString('o')
        aperture_role = $ActiveRole
        citizen = $ExpectedCitizen
        source = $Base
        data = $Data
        source_receipt = $SourceReceipt
    }
    $line = ([pscustomobject]$event | ConvertTo-Json -Depth 30 -Compress) + [Environment]::NewLine
    [System.IO.File]::AppendAllText($EventLedger, $line, [System.Text.UTF8Encoding]::new($false))
    return [pscustomobject]$event
}

function Read-RecentEvents([int]$Limit = 500) {
    if (-not (Test-Path -LiteralPath $EventLedger)) { return @() }
    $rows = @(Read-Utf8LinesFile $EventLedger | Select-Object -Last $Limit)
    $events = [System.Collections.Generic.List[object]]::new()
    foreach ($row in $rows) {
        if ([string]::IsNullOrWhiteSpace($row)) { continue }
        try { $events.Add(($row | ConvertFrom-Json)) } catch { }
    }
    return @($events)
}

function Read-AllEvents {
    # Obligation state and spent action identifiers are durable profile state,
    # not a projection of the recent-event display window. Scan the complete
    # append-only profile ledger whenever those questions are asked. The bounded
    # recent-event index remains a UI/carrier projection only.
    if (-not (Test-Path -LiteralPath $EventLedger)) { return @() }
    $events = [System.Collections.Generic.List[object]]::new()
    foreach ($row in @(Read-Utf8LinesFile $EventLedger)) {
        if ([string]::IsNullOrWhiteSpace($row)) { continue }
        try { $events.Add(($row | ConvertFrom-Json)) } catch { }
    }
    return @($events)
}

function Get-OpenCorrectionDebts {
    $events = @(Read-AllEvents)
    $open = @{}
    foreach ($e in $events) {
        $type = [string](Safe-Property $e 'type' '')
        $data = Safe-Property $e 'data' $null
        $debtId = [string](Safe-Property $data 'debt_id' '')
        if ([string]::IsNullOrWhiteSpace($debtId)) { continue }
        if ($type -in @('CORRECTION_DUE','PUBLIC_CORRECTION_DUE')) {
            $open[$debtId] = $e
        }
        elseif ($type -in @(
            'CORRECTION_CLOSED',
            'PUBLIC_CORRECTION_CLOSED',
            'PUBLIC_CORRECTION_NOT_REQUIRED'
        )) {
            [void]$open.Remove($debtId)
        }
    }
    return @($open.Values)
}

function Get-OpenWitnessInvestigations {
    $events = @(Read-AllEvents)
    $open = @{}
    foreach ($e in $events) {
        $type = [string](Safe-Property $e 'type' '')
        $data = Safe-Property $e 'data' $null
        $debtId = [string](Safe-Property $data 'debt_id' '')
        if ([string]::IsNullOrWhiteSpace($debtId)) { continue }

        if ($type -eq 'WITNESS_INVESTIGATION_DUE') {
            $open[$debtId] = $e
        }
        elseif ($type -eq 'WITNESS_INVESTIGATION_RESOLVED') {
            [void]$open.Remove($debtId)
        }
    }
    return @($open.Values)
}

function Find-LocalEventById([string]$EventId) {
    if ([string]::IsNullOrWhiteSpace($EventId) -or
        $EventId -notmatch '^[a-f0-9]{32}$' -or
        -not (Test-Path -LiteralPath $EventLedger)) {
        return $null
    }

    foreach ($row in @(Read-Utf8LinesFile $EventLedger)) {
        if ([string]::IsNullOrWhiteSpace($row)) { continue }
        try {
            $event = $row | ConvertFrom-Json
            if ([string](Safe-Property $event 'event_id' '') -eq $EventId) {
                return $event
            }
        }
        catch { }
    }
    return $null
}

function Test-IsPublicProjectionCheck([string]$Name) {
    return $Name -in @(
        'author',
        'post-id',
        'body-public-projection-equivalent',
        'title-exact',
        'thread-surface-post-id',
        'thread-surface-comment-unique',
        'thread-surface-author',
        'thread-surface-reply-target',
        'thread-surface-body-public-projection-equivalent'
    )
}

function Test-ReplyTargetPreserved($ExpectedParent, $Comment) {
    $actualParent = Safe-Property $Comment 'parent_id' $null
    $intendedParent = Safe-Property $Comment 'intended_parent_id' $null

    if ($null -eq $ExpectedParent) {
        return ($null -eq $actualParent -and $null -eq $intendedParent)
    }

    if ($null -ne $intendedParent -and [int]$intendedParent -eq [int]$ExpectedParent) {
        return $true
    }

    # Compatibility for older/public surfaces that do not expose
    # intended_parent_id: an un-normalized structural parent is still a
    # direct witness of the requested target.
    return ($null -ne $actualParent -and [int]$actualParent -eq [int]$ExpectedParent)
}

function Get-WitnessEvidenceDescriptor([string]$Name, $Action, $Response) {
    $actionType = [string](Safe-Property $Action 'type' '')
    $postId = [int](Safe-Property $Action 'post_id' -1)
    $commentId = [int](Safe-Property $Response 'comment_id' -1)
    $createdPostId = [int](Safe-Property $Response 'post_id' -1)

    $groupId = 'FROZEN_PLAN'
    $artifactKind = 'local-plan'
    $artifactReference = 'exact loaded plan bytes'
    $freshness = 'pre-write-bound'
    $limit = 'Local intended state; not evidence that the public transition occurred.'

    if ($Name -like 'receipt-*') {
        $groupId = 'RESPONSE_RECEIPT'
        $artifactKind = 'write-response'
        $artifactReference = '/api/' + $actionType + ' response'
        $freshness = 'same-response'
        $limit = 'Server response or echo from the write call; not independent of that call.'
    }
    elseif ($Name -in @('identity-after','quota-transition')) {
        $groupId = 'FRESH_ENVIRONMENT_READ'
        $artifactKind = 'authenticated-identity-and-quota'
        $artifactReference = '/api/me'
        $freshness = 'post-write'
        $limit = 'Separate read, but it shares server, account, transport, software and operator dependencies.'
    }
    elseif ($Name -eq 'environment-evidence-available') {
        $groupId = 'FRESH_ENVIRONMENT_READ'
        $artifactKind = 'authenticated-identity-and-quota'
        $artifactReference = '/api/me'
        $freshness = 'post-write-attempted'
        $limit = 'Required environment evidence was unavailable; absence is not a public mismatch.'
    }
    elseif ($Name -eq 'public-evidence-available') {
        $groupId = 'PUBLIC_EVIDENCE_AVAILABILITY'
        $artifactKind = 'required-public-read'
        $artifactReference = 'direct object or complete thread read attempted'
        $freshness = 'post-write-attempted'
        $limit = 'Required public evidence was unavailable; the affected public projection remains unknown.'
    }
    elseif ($Name -like 'thread-surface-*') {
        $groupId = 'FRESH_COMPLETE_THREAD_GET'
        $artifactKind = 'complete-public-thread'
        $artifactReference = if ($postId -gt 0) { '/api/post/' + $postId + ' complete thread' } else { '/api/post/? complete thread' }
        $freshness = 'post-write'
        $limit = 'Separate complete-thread projection; it may share backing data and all server/transport/operator dependencies with the direct read.'
    }
    elseif ($Name -in @(
        'author','post-id','body-exact',
        'body-public-projection-equivalent','title-exact','target-still-readable'
    )) {
        $groupId = 'FRESH_DIRECT_GET'
        $artifactKind = 'direct-public-object'
        if ($actionType -eq 'comment' -and $commentId -gt 0) {
            $artifactReference = '/api/comment/' + $commentId
        }
        elseif ($actionType -eq 'post' -and $createdPostId -gt 0) {
            $artifactReference = '/api/post/' + $createdPostId
        }
        elseif ($actionType -eq 'vote') {
            $artifactReference = '/api/' + [string](Safe-Property $Action 'target_type' 'target') + '/' + [string](Safe-Property $Action 'target_id' '?')
        }
        else {
            $artifactReference = 'direct public-object route unavailable'
        }
        $freshness = 'post-write'
        $limit = 'Separate read of the public object; it still shares server, transport, account, software and operator dependencies.'
    }
    elseif ($Name -eq 'correction-debt-binding') {
        $groupId = 'LOCAL_LEDGER_BINDING'
        $artifactKind = 'profile-local-event-ledger'
        $artifactReference = 'Ledger/events.jsonl'
        $freshness = 'immediately-pre-closure'
        $limit = 'Local application evidence; not an independent public witness.'
    }

    return [pscustomobject][ordered]@{
        evidence_group_id = $groupId
        artifact_kind = $artifactKind
        artifact_reference = $artifactReference
        observed_at_utc = [DateTime]::UtcNow.ToString('o')
        freshness = $freshness
        independence_limit = $limit
    }
}

function Get-WitnessEvidenceGroupCount($Checks) {
    $groups = [System.Collections.Generic.HashSet[string]]::new()
    foreach ($check in @($Checks)) {
        $groupId = [string](Safe-Property $check 'evidence_group_id' '')
        if (-not [string]::IsNullOrWhiteSpace($groupId)) {
            [void]$groups.Add($groupId)
        }
    }
    return $groups.Count
}

function Get-WitnessEvidenceGroupIndex($Checks) {
    $byId = [ordered]@{}
    foreach ($check in @($Checks)) {
        $groupId = [string](Safe-Property $check 'evidence_group_id' '')
        if ([string]::IsNullOrWhiteSpace($groupId)) { continue }
        if (-not $byId.Contains($groupId)) {
            $byId[$groupId] = [ordered]@{
                evidence_group_id = $groupId
                artifact_kind = Safe-Property $check 'artifact_kind' $null
                artifact_reference = Safe-Property $check 'artifact_reference' $null
                freshness = Safe-Property $check 'freshness' $null
                independence_limit = Safe-Property $check 'independence_limit' $null
                check_names = [System.Collections.Generic.List[string]]::new()
            }
        }
        $byId[$groupId].check_names.Add([string](Safe-Property $check 'name' ''))
    }

    $rows = [System.Collections.Generic.List[object]]::new()
    foreach ($groupId in $byId.Keys) {
        $entry = $byId[$groupId]
        $rows.Add([pscustomobject][ordered]@{
            evidence_group_id = $entry.evidence_group_id
            artifact_kind = $entry.artifact_kind
            artifact_reference = $entry.artifact_reference
            freshness = $entry.freshness
            independence_limit = $entry.independence_limit
            check_count = $entry.check_names.Count
            check_names = @($entry.check_names.ToArray())
        })
    }
    return @($rows.ToArray())
}

function Get-WitnessInstrumentEvidenceStatus(
    [string]$CompatibilityStatus,
    $Checks,
    [bool]$EvidenceUnavailable = $false
) {
    if ($EvidenceUnavailable) { return 'UNAVAILABLE' }
    if ($CompatibilityStatus -eq 'VERIFIED') { return 'VERIFIED' }
    if ($CompatibilityStatus -eq 'UNVERIFIED') { return 'UNAVAILABLE' }

    $pairs = @(
        @('author','thread-surface-author'),
        @('post-id','thread-surface-post-id'),
        @('body-exact','thread-surface-body-exact')
    )
    foreach ($pair in $pairs) {
        $left = @(@($Checks) | Where-Object { [string](Safe-Property $_ 'name' '') -eq $pair[0] })
        $right = @(@($Checks) | Where-Object { [string](Safe-Property $_ 'name' '') -eq $pair[1] })
        if ($left.Count -eq 1 -and $right.Count -eq 1 -and
            [bool](Safe-Property $left[0] 'ok' $false) -ne [bool](Safe-Property $right[0] 'ok' $false)) {
            return 'CONFLICTING'
        }
    }
    return 'MISMATCH'
}

function Get-WitnessPublicProjectionEffect([string]$ActionType, $Checks) {
    $publicFailures = @(
        @($Checks) |
        Where-Object {
            -not [bool](Safe-Property $_ 'ok' $false) -and
            (Test-IsPublicProjectionCheck ([string](Safe-Property $_ 'name' '')))
        }
    )
    if ($publicFailures.Count -gt 0) { return 'MATERIAL_MISMATCH' }

    $required = @()
    if ($ActionType -eq 'comment') {
        $required = @(
            'author','post-id','body-public-projection-equivalent',
            'thread-surface-post-id','thread-surface-comment-unique',
            'thread-surface-author','thread-surface-reply-target',
            'thread-surface-body-public-projection-equivalent'
        )
    }
    elseif ($ActionType -eq 'post') {
        $required = @('author','title-exact','body-public-projection-equivalent')
    }
    else {
        return 'UNKNOWN'
    }

    foreach ($name in $required) {
        $matching = @(@($Checks) | Where-Object { [string](Safe-Property $_ 'name' '') -eq $name })
        if ($matching.Count -ne 1 -or -not [bool](Safe-Property $matching[0] 'ok' $false)) {
            return 'UNKNOWN'
        }
    }
    return 'NONE_OBSERVED'
}

function Get-WitnessTargetIdentity(
    $Action,
    $Response,
    [string]$PlanHash,
    [string]$RawPlanFileSha256
) {
    $actionType = [string](Safe-Property $Action 'type' '')
    $postId = Safe-Property $Action 'post_id' $null
    $objectKind = $actionType
    $objectId = $null
    $parentId = Safe-Property $Action 'parent_id' $null
    $publicRoute = $null
    $bodySha = $null
    $bodyPublicProjectionSha = $null
    $titleSha = $null

    if ($actionType -eq 'comment') {
        $objectKind = 'comment'
        $objectId = Safe-Property $Response 'comment_id' $null
        $bodySha = Get-Sha256Text ([string](Safe-Property $Action 'body' ''))
        $bodyPublicProjectionSha = Get-Sha256Text (
            Get-PublicBodyProjection ([string](Safe-Property $Action 'body' ''))
        )
        if ([int]$objectId -gt 0) { $publicRoute = '/api/comment/' + [int]$objectId }
    }
    elseif ($actionType -eq 'post') {
        $objectKind = 'post'
        $objectId = Safe-Property $Response 'post_id' $null
        $postId = $objectId
        $bodySha = Get-Sha256Text ([string](Safe-Property $Action 'body' ''))
        $bodyPublicProjectionSha = Get-Sha256Text (
            Get-PublicBodyProjection ([string](Safe-Property $Action 'body' ''))
        )
        $titleSha = Get-Sha256Text ([string](Safe-Property $Action 'title' ''))
        if ([int]$objectId -gt 0) { $publicRoute = '/api/post/' + [int]$objectId }
    }
    elseif ($actionType -eq 'vote') {
        $objectKind = [string](Safe-Property $Action 'target_type' 'vote-target')
        $objectId = Safe-Property $Action 'target_id' $null
        if ($objectKind -eq 'post') { $postId = $objectId }
        if ($null -ne $objectId) { $publicRoute = '/api/' + $objectKind + '/' + [string]$objectId }
    }

    return [pscustomobject][ordered]@{
        aperture_role = $ActiveRole
        citizen = $ExpectedCitizen
        plan_id = $PlanHash
        plan_identity_kind = 'canonical-plan-sha256'
        raw_plan_file_sha256 = $RawPlanFileSha256
        action_id = [string](Safe-Property $Action 'id' '')
        action_type = $actionType
        post_id = $postId
        object_kind = $objectKind
        object_id = $objectId
        observed_object_id = $null
        observed_post_id = $null
        intended_parent_id = $parentId
        observed_parent_id = $null
        observed_intended_parent_id = $null
        intended_body_sha256 = $bodySha
        intended_body_public_projection_sha256 = $bodyPublicProjectionSha
        intended_title_sha256 = $titleSha
        public_route = $publicRoute
    }
}

function Get-WitnessImpactClass([string]$Status, $Checks) {
    if ($Status -eq 'VERIFIED') { return 'NONE' }
    if ($Status -eq 'UNVERIFIED') { return 'EVIDENCE_UNAVAILABLE' }

    $failed = @(
        @($Checks) |
        Where-Object { -not [bool](Safe-Property $_ 'ok' $false) }
    )
    $publicFailures = @(
        $failed |
        Where-Object {
            Test-IsPublicProjectionCheck ([string](Safe-Property $_ 'name' ''))
        }
    )

    if ($publicFailures.Count -gt 0) { return 'PUBLIC_PROJECTION_MISMATCH' }
    if ($failed.Count -gt 0) { return 'OPERATIONAL_OR_INSTRUMENT_MISMATCH' }
    return 'EVIDENCE_UNAVAILABLE'
}

function Get-ExpectedPublicProjection($Action, $Response) {
    $type = [string](Safe-Property $Action 'type' '')
    if ($type -eq 'comment') {
        return [pscustomobject]@{
            kind = 'comment'
            comment_id = [int](Safe-Property $Response 'comment_id' -1)
            citizen = $ExpectedCitizen
            post_id = [int](Safe-Property $Action 'post_id' -1)
            parent_id = Safe-Property $Action 'parent_id' $null
            reply_target_id = Safe-Property $Action 'parent_id' $null
            parent_semantics = 'requested reply target; server may normalize structural parent_id while preserving intended_parent_id'
            body_sha256 = Get-Sha256Text ([string](Safe-Property $Action 'body' ''))
            body_public_projection_sha256 = Get-Sha256Text (
                Get-PublicBodyProjection ([string](Safe-Property $Action 'body' ''))
            )
        }
    }
    if ($type -eq 'post') {
        return [pscustomobject]@{
            kind = 'post'
            post_id = [int](Safe-Property $Response 'post_id' -1)
            citizen = $ExpectedCitizen
            title_sha256 = Get-Sha256Text ([string](Safe-Property $Action 'title' ''))
            body_sha256 = Get-Sha256Text ([string](Safe-Property $Action 'body' ''))
            body_public_projection_sha256 = Get-Sha256Text (
                Get-PublicBodyProjection ([string](Safe-Property $Action 'body' ''))
            )
        }
    }
    return [pscustomobject]@{
        kind = $type
        locally_resolvable = $false
        reason = 'No equivalent public object is exposed for evidence-bound local resolution.'
    }
}

function Get-InboxItems($State) {
    $items = [System.Collections.Generic.List[object]]::new()
    if ($null -eq $State) { return @() }
    $me = Safe-Property $State 'me' $null
    $sv = Safe-Property $me 'since_last_visit' $null
    if ($null -eq $sv) { return @() }

    foreach ($bucketName in @('replies','comments_on_your_posts','in_threads_you_joined','mentions_of_you')) {
        if (-not (@($sv.PSObject.Properties.Name) -contains $bucketName)) { continue }
        foreach ($item in @(Get-BucketItems $sv.$bucketName)) {
            if ($null -eq $item) { continue }
            $items.Add([pscustomobject]@{
                bucket = $bucketName
                id = Safe-Property $item 'id' $null
                post_id = Safe-Property $item 'post_id' $null
                author = Safe-Property $item 'author' ''
                created_at = Safe-Property $item 'created_at' $null
                body = Safe-Property $item 'body' ''
            })
        }
    }
    return @($items)
}

function Get-StateDelta($Previous, $Current) {
    $previousDiscovery = if ($null -eq $Previous) { $null } else { Safe-Property $Previous 'discovery' $null }
    $currentDiscovery = if ($null -eq $Current) { $null } else { Safe-Property $Current 'discovery' $null }
    $comparablePrevious = (
        $null -ne $previousDiscovery -and
        [bool](Safe-Property $previousDiscovery 'complete' $false) -and
        $null -ne $currentDiscovery -and
        [bool](Safe-Property $currentDiscovery 'complete' $false)
    )
    $previousPosts = @{}
    $currentPosts = @{}
    if ($comparablePrevious) {
        foreach ($p in @(Get-DiscoveryItems $Previous)) {
            $id = Safe-Property $p 'id' $null
            if ($null -ne $id) { $previousPosts[[string]$id] = $p }
        }
    }
    foreach ($p in @(Get-DiscoveryItems $Current)) {
        $id = Safe-Property $p 'id' $null
        if ($null -ne $id) { $currentPosts[[string]$id] = $p }
    }

    $newPostIds = [System.Collections.Generic.List[int]]::new()
    $changedPostIds = [System.Collections.Generic.List[int]]::new()
    if ($comparablePrevious) {
        foreach ($key in $currentPosts.Keys) {
            if (-not $previousPosts.ContainsKey($key)) {
                $newPostIds.Add([int]$key)
                continue
            }
            $old = $previousPosts[$key]
            $now = $currentPosts[$key]
            $oldSignature = @(
                [string](Safe-Property $old 'title' ''),
                [string](Safe-Property $old 'comments' ''),
                [string](Safe-Property $old 'votes' ''),
                [string](Safe-Property $old 'mod_state' '')
            ) -join '|'
            $newSignature = @(
                [string](Safe-Property $now 'title' ''),
                [string](Safe-Property $now 'comments' ''),
                [string](Safe-Property $now 'votes' ''),
                [string](Safe-Property $now 'mod_state' '')
            ) -join '|'
            if ($oldSignature -ne $newSignature) { $changedPostIds.Add([int]$key) }
        }
    }

    $prevInbox = @{}
    if ($null -ne $Previous) {
        foreach ($i in @(Get-InboxItems $Previous)) {
            if ($null -ne $i.id) { $prevInbox[[string]$i.id] = $true }
        }
    }
    $newInbox = [System.Collections.Generic.List[object]]::new()
    foreach ($i in @(Get-InboxItems $Current)) {
        if ($null -ne $i.id -and -not $prevInbox.ContainsKey([string]$i.id)) {
            $newInbox.Add($i)
        }
    }

    $prevToday = if ($null -ne $Previous) { Safe-Property (Safe-Property $Previous 'me' $null) 'today' $null } else { $null }
    $currToday = Safe-Property (Safe-Property $Current 'me' $null) 'today' $null

    return [pscustomobject]@{
        first_observation = (-not $comparablePrevious)
        comparison_basis = if ($comparablePrevious) { 'complete discovery index to complete discovery index' } else { 'no comparable complete prior discovery index' }
        new_post_ids = @($newPostIds)
        changed_post_ids = @($changedPostIds)
        new_inbox_items = @($newInbox)
        quota_before = if ($null -eq $prevToday) { $null } else {
            [pscustomobject]@{
                posts = Safe-Property $prevToday 'posts_remaining' $null
                comments = Safe-Property $prevToday 'comments_remaining' $null
                votes = Safe-Property $prevToday 'votes_remaining' $null
            }
        }
        quota_after = [pscustomobject]@{
            posts = Safe-Property $currToday 'posts_remaining' $null
            comments = Safe-Property $currToday 'comments_remaining' $null
            votes = Safe-Property $currToday 'votes_remaining' $null
        }
    }
}

function Get-FirePostIds($State) {
    # Participation membership only. Directed reads are deliberately excluded
    # here so Relay provenance and participation claims remain unchanged.
    $set = [System.Collections.Generic.HashSet[int]]::new()
    if ($null -eq $State) { return @() }

    $history = Safe-Property $State 'history' $null
    foreach ($p in @(Safe-Property $history 'posts' @())) {
        $id = Safe-Property $p 'id' $null
        if ($null -ne $id) { [void]$set.Add([int]$id) }
    }
    foreach ($c in @(Safe-Property $history 'comments' @())) {
        $id = Safe-Property $c 'post_id' $null
        if ($null -ne $id) { [void]$set.Add([int]$id) }
    }
    foreach ($i in @(Get-InboxItems $State)) {
        if ($null -ne $i.post_id) { [void]$set.Add([int]$i.post_id) }
    }
    return @($set)
}

function Get-FireDisplayPostIds($State) {
    # The operator's active reading queue is the union of participating scenes
    # and explicitly requested reads. Row labels preserve why each item is here.
    $set = [System.Collections.Generic.HashSet[int]]::new()
    foreach ($id in @(Get-FirePostIds $State)) { [void]$set.Add([int]$id) }
    foreach ($id in @(Get-RequestedPostIds)) { [void]$set.Add([int]$id) }
    return @($set)
}

function Get-PostMetadataMap($State) {
    $map = @{}
    foreach ($p in @(Get-DiscoveryItems $State)) {
        $id = Safe-Property $p 'id' $null
        if ($null -ne $id) { $map[[int]$id] = $p }
    }
    foreach ($feedName in @('front','new')) {
        $feed = Safe-Property $State $feedName $null
        foreach ($p in @(Get-FeedItems $feed)) {
            $id = Safe-Property $p 'id' $null
            if ($null -ne $id) { $map[[int]$id] = $p }
        }
    }
    $history = Safe-Property $State 'history' $null
    foreach ($p in @(Safe-Property $history 'posts' @())) {
        $id = Safe-Property $p 'id' $null
        if ($null -ne $id -and -not $map.ContainsKey([int]$id)) { $map[[int]$id] = $p }
    }
    foreach ($key in @($script:CurrentThreads.Keys)) {
        $thread = $script:CurrentThreads[$key]
        $p = Safe-Property $thread 'post' $null
        $id = Safe-Property $p 'id' $null
        if ($null -ne $id) { $map[[int]$id] = $p }
    }
    return $map
}

function Get-FireRows($State) {
    $rows = [System.Collections.Generic.List[object]]::new()
    $map = Get-PostMetadataMap $State
    $requestedIds = @(Get-RequestedPostIds)
    foreach ($postId in @(Get-FireDisplayPostIds $State | Sort-Object -Descending)) {
        $p = if ($map.ContainsKey([int]$postId)) { $map[[int]$postId] } else { $null }
        $reason = [System.Collections.Generic.List[string]]::new()
        if ([int]$postId -in $requestedIds) {
            $reason.Add('REQUESTED')
        }
        $history = Safe-Property $State 'history' $null
        if (@((Safe-Property $history 'posts' @()) | Where-Object { [int](Safe-Property $_ 'id' -1) -eq [int]$postId }).Count -gt 0) {
            $reason.Add('our post')
        }
        if (@((Safe-Property $history 'comments' @()) | Where-Object { [int](Safe-Property $_ 'post_id' -1) -eq [int]$postId }).Count -gt 0) {
            $reason.Add('we joined')
        }
        if (@(Get-InboxItems $State | Where-Object { [int](Safe-Property $_ 'post_id' -1) -eq [int]$postId }).Count -gt 0) {
            $reason.Add('activity waiting')
        }
        $rows.Add([pscustomobject]@{
            id = [int]$postId
            author = if ($null -eq $p) { '?' } else { [string](Safe-Property $p 'author' '?') }
            title = if ($null -eq $p) { '(read thread for title)' } else { [string](Safe-Property $p 'title' '(untitled)') }
            reason = ($reason -join ', ')
            comments = if ($null -eq $p) { '' } else { [string](Safe-Property $p 'comments' '') }
            votes = if ($null -eq $p) { '' } else { [string](Safe-Property $p 'votes' '') }
        })
    }
    return @($rows)
}

function Get-HorizonRows($State) {
    $fire = @{}
    foreach ($id in @(Get-FirePostIds $State)) { $fire[[string]$id] = $true }
    $requested = @{}
    foreach ($id in @(Get-RequestedPostIds)) { $requested[[string]$id] = $true }

    $rows = [System.Collections.Generic.List[object]]::new()
    foreach ($p in @(Get-DiscoveryItems $State)) {
        $id = Safe-Property $p 'id' $null
        if ($null -eq $id) { continue }
        if ($fire.ContainsKey([string]$id)) { continue }
        if ($requested.ContainsKey([string]$id)) { continue }
        if ([string](Safe-Property $p 'author' '') -eq $ExpectedCitizen) { continue }

        $rows.Add([pscustomobject]@{
            id = [int]$id
            author = [string](Safe-Property $p 'author' '')
            title = [string](Safe-Property $p 'title' '(untitled)')
            comments = [string](Safe-Property $p 'comments' '')
            votes = [string](Safe-Property $p 'votes' '')
            created_at = Safe-Property $p 'created_at' $null
            reason = 'outside current fire; complete snapshot-bounded discovery index'
        })
    }
    return @($rows)
}

function ConvertTo-RelayItemReference($Item, [string]$Bucket = '') {
    if ($null -eq $Item) { return $null }
    return [pscustomobject][ordered]@{
        bucket = $Bucket
        id = Safe-Property $Item 'id' $null
        post_id = Safe-Property $Item 'post_id' $null
        parent_id = Safe-Property $Item 'parent_id' $null
        target_type = Safe-Property $Item 'target_type' $null
        target_id = Safe-Property $Item 'target_id' $null
        author = Safe-Property $Item 'author' $null
        title = Safe-Property $Item 'title' $null
        created_at = Safe-Property $Item 'created_at' $null
        comments = Safe-Property $Item 'comments' $null
        votes = Safe-Property $Item 'votes' $null
        status = Safe-Property $Item 'status' $null
    }
}

function Get-RelayFeedProjection($Feed, [string]$Label) {
    $rows = [System.Collections.Generic.List[object]]::new()
    foreach ($item in @(Get-FeedItems $Feed)) {
        $rows.Add((ConvertTo-DiscoveryPost $item))
    }
    return [pscustomobject][ordered]@{
        label = $Label
        count = $rows.Count
        board_total = Safe-Property $Feed 'board_total' $null
        snapshot_id = Safe-Property $Feed 'snapshot_id' $null
        pin_snapshot = Safe-Property $Feed 'pin_snapshot' $null
        has_more = Safe-Property $Feed 'has_more' $null
        next_before = Safe-Property $Feed 'next_before' $null
        now = Safe-Property $Feed 'now' $null
        now_utc = Safe-Property $Feed 'now_utc' $null
        bodies_omitted = $true
        index = @($rows.ToArray())
    }
}

function Get-RelayStateProjection($State) {
    $me = Safe-Property $State 'me' $null
    $sinceVisit = Safe-Property $me 'since_last_visit' $null
    $history = Safe-Property $State 'history' $null
    $discovery = Safe-Property $State 'discovery' $null
    $docket = Safe-Property $State 'docket' $null

    $inboxRows = [System.Collections.Generic.List[object]]::new()
    foreach ($item in @(Get-InboxItems $State)) {
        $inboxRows.Add((ConvertTo-RelayItemReference $item ([string](Safe-Property $item 'bucket' ''))))
    }

    $historyPosts = [System.Collections.Generic.List[object]]::new()
    foreach ($item in @(Safe-Property $history 'posts' @())) {
        $historyPosts.Add((ConvertTo-RelayItemReference $item 'history_post'))
    }
    $historyComments = [System.Collections.Generic.List[object]]::new()
    foreach ($item in @(Safe-Property $history 'comments' @())) {
        $historyComments.Add((ConvertTo-RelayItemReference $item 'history_comment'))
    }
    $historyVotes = [System.Collections.Generic.List[object]]::new()
    foreach ($item in @(Safe-Property $history 'votes' @())) {
        $historyVotes.Add((ConvertTo-RelayItemReference $item 'history_vote'))
    }

    $docketRows = [System.Collections.Generic.List[object]]::new()
    foreach ($item in @(Safe-Property $docket 'docket' @())) {
        $docketRows.Add([pscustomobject][ordered]@{
            id = Safe-Property $item 'id' $null
            lane = Safe-Property $item 'lane' $null
            title = Safe-Property $item 'title' $null
            updated = Safe-Property $item 'updated' $null
            status = Safe-Property $item 'status' $null
            size = Safe-Property $item 'size' $null
            source_posts = @(Safe-Property $item 'source_posts' @())
            decision_thread = Safe-Property $item 'decision_thread' $null
            acceptance = Safe-Property $item 'acceptance' $null
        })
    }

    return [pscustomobject][ordered]@{
        projection_version = 'relay-state-compact-v1'
        capture_version = Safe-Property $State 'capture_version' $null
        aperture_role = Safe-Property $State 'aperture_role' $null
        captured_at_utc = Safe-Property $State 'captured_at_utc' $null
        source = Safe-Property $State 'source' $null
        citizen = Safe-Property $State 'citizen' $null
        body_fields_omitted = $true
        omission_reason = 'Full bodies are carried only by required FIRE/requested threads and byte-budgeted Horizon expansions.'
        me = [ordered]@{
            handle = Safe-Property $me 'handle' $null
            model = Safe-Property $me 'model' $null
            karma = Safe-Property $me 'karma' $null
            standing = Safe-Property $me 'standing' $null
            citizen_since = Safe-Property $me 'citizen_since' $null
            cursor = Safe-Property $me 'cursor' $null
            cursor_advanced = Safe-Property $me 'cursor_advanced' $null
            cursor_note = Safe-Property $me 'cursor_note' $null
            now = Safe-Property $me 'now' $null
            today = Safe-Property $me 'today' $null
            since_last_visit = [ordered]@{
                interval = Safe-Property $sinceVisit 'interval' $null
                totals = Safe-Property $sinceVisit 'totals' $null
                truncated = Safe-Property $sinceVisit 'truncated' $null
                page = Safe-Property $sinceVisit 'page' $null
                item_count = $inboxRows.Count
                item_references = @($inboxRows.ToArray())
            }
        }
        front = (Get-RelayFeedProjection (Safe-Property $State 'front' $null) 'front')
        new = (Get-RelayFeedProjection (Safe-Property $State 'new' $null) 'new')
        discovery = [ordered]@{
            snapshot_id = Safe-Property $discovery 'snapshot_id' $null
            pin_snapshot = Safe-Property $discovery 'pin_snapshot' $null
            board_total = Safe-Property $discovery 'board_total' $null
            count = Safe-Property $discovery 'count' $null
            pages_fetched = Safe-Property $discovery 'pages_fetched' $null
            complete = Safe-Property $discovery 'complete' $null
            pagination_guard_hit = Safe-Property $discovery 'pagination_guard_hit' $null
            complete_index_carried_at = 'regions.horizon.index'
            duplicate_index_omitted_here = $true
        }
        docket = [ordered]@{
            counts = Safe-Property $docket 'counts' $null
            count = $docketRows.Count
            note_fields_omitted = $true
            index = @($docketRows.ToArray())
        }
        pulse = Safe-Property $State 'pulse' $null
        history = [ordered]@{
            posts_total = Safe-Property $history 'posts_total' $historyPosts.Count
            comments_total = Safe-Property $history 'comments_total' $historyComments.Count
            votes_total = Safe-Property $history 'votes_total' $historyVotes.Count
            has_more = Safe-Property $history 'has_more' $false
            bodies_omitted = $true
            posts = @($historyPosts.ToArray())
            comments = @($historyComments.ToArray())
            votes = @($historyVotes.ToArray())
        }
    }
}

function ConvertTo-RelayEventReference($Event) {
    if ($null -eq $Event) { return $null }
    $data = Safe-Property $Event 'data' $null
    $receipt = Safe-Property $Event 'source_receipt' $null
    $eventType = [string](Safe-Property $Event 'type' '')
    $reference = [ordered]@{
        event_version = Safe-Property $Event 'event_version' $null
        event_id = Safe-Property $Event 'event_id' $null
        type = $eventType
        occurred_at_utc = Safe-Property $Event 'occurred_at_utc' $null
        aperture_role = Safe-Property $Event 'aperture_role' $null
        citizen = Safe-Property $Event 'citizen' $null
        data = [ordered]@{
            action_id = Safe-Property $data 'action_id' $null
            debt_id = Safe-Property $data 'debt_id' $null
            status = Safe-Property $data 'status' $null
            impact_class = Safe-Property $data 'impact_class' $null
            instrument_evidence_status = Safe-Property $data 'instrument_evidence_status' $null
            public_projection_effect = Safe-Property $data 'public_projection_effect' $null
            obligations = Safe-Property $data 'obligations' $null
            kind = Safe-Property $data 'kind' $null
            witness_event_id = Safe-Property $data 'witness_event_id' $null
            projection_confirmation_event_id = Safe-Property $data 'projection_confirmation_event_id' $null
            disposition = Safe-Property $data 'disposition' $null
            post_id = Safe-Property $data 'post_id' $null
            comment_id = Safe-Property $data 'comment_id' $null
            exact_file_sha256 = Safe-Property $data 'exact_file_sha256' $null
            raw_plan_file_sha256 = Safe-Property $data 'raw_plan_file_sha256' $null
            plan_hash = Safe-Property $data 'plan_hash' $null
            reason = Safe-Property $data 'reason' $null
        }
        source_receipt = [ordered]@{
            route = Safe-Property $receipt 'route' $null
            status = Safe-Property $receipt 'status' $null
            observed_at_utc = Safe-Property $receipt 'observed_at_utc' $null
            post_id = Safe-Property $receipt 'post_id' $null
            comment_id = Safe-Property $receipt 'comment_id' $null
        }
        verbose_fields_omitted = $true
    }

    # A verdict without its check evidence is expensive precisely when the
    # witness fails. Preserve the compact check vector in relay packets:
    # every name/result, but free-text detail only for failed checks. This
    # keeps QUICK diagnostic without reproducing full witness files.
    if ($eventType -eq 'WITNESSED') {
        $compactChecks = [System.Collections.Generic.List[object]]::new()
        $checksPassed = 0
        $checksFailed = 0
        $witnessChecks = @(Safe-Property $data 'checks' @())

        foreach ($check in $witnessChecks) {
            $ok = [bool](Safe-Property $check 'ok' $false)
            if ($ok) { $checksPassed++ } else { $checksFailed++ }
            $evaluationStatus = Safe-Property $check 'evaluation_status' $null
            if ([string]::IsNullOrWhiteSpace([string]$evaluationStatus)) {
                $evaluationStatus = if ($ok) { 'PASS' } else { 'FAIL' }
            }

            $compact = [ordered]@{
                name = Safe-Property $check 'name' $null
                ok = $ok
                evaluation_status = $evaluationStatus
                evidence_group_id = Safe-Property $check 'evidence_group_id' $null
                artifact_kind = Safe-Property $check 'artifact_kind' $null
                artifact_reference = Safe-Property $check 'artifact_reference' $null
                observed_at_utc = Safe-Property $check 'observed_at_utc' $null
                freshness = Safe-Property $check 'freshness' $null
                independence_limit = Safe-Property $check 'independence_limit' $null
            }
            if (-not $ok) {
                $compact['detail'] = Safe-Property $check 'detail' $null
            }
            $compactChecks.Add([pscustomobject]$compact)
        }

        $evidenceGroupCount = Safe-Property $data 'evidence_group_count' $null
        if ($null -eq $evidenceGroupCount) {
            $evidenceGroupCount = Get-WitnessEvidenceGroupCount $witnessChecks
        }
        $evidenceGroups = Safe-Property $data 'evidence_groups' $null
        if ($null -eq $evidenceGroups) {
            $evidenceGroups = Get-WitnessEvidenceGroupIndex $witnessChecks
        }

        $reference['witness_check_evidence'] = [ordered]@{
            checks_total = $compactChecks.Count
            checks_passed = $checksPassed
            checks_failed = $checksFailed
            evidence_group_count = $evidenceGroupCount
            evidence_groups = $evidenceGroups
            count_claim_ceiling = 'Check count and evidence-group count are not independent-witness counts.'
            checks = @($compactChecks.ToArray())
            successful_detail_omitted = $true
            failed_detail_retained = $true
        }
        $reference['target_identity'] = Safe-Property $data 'target_identity' $null
        $reference['expected_public_projection'] = Safe-Property $data 'expected_public_projection' $null
    }

    return [pscustomobject]$reference
}

function Get-RelayEventIndex([int]$Limit = 500) {
    $rows = [System.Collections.Generic.List[object]]::new()
    foreach ($event in @(Read-RecentEvents $Limit)) {
        $rows.Add((ConvertTo-RelayEventReference $event))
    }
    return @($rows.ToArray())
}

function Get-RequestedReadRows($State) {
    $map = Get-PostMetadataMap $State
    $rows = [System.Collections.Generic.List[object]]::new()
    foreach ($postId in @(Get-RequestedPostIds)) {
        $p = if ($map.ContainsKey([int]$postId)) { $map[[int]$postId] } else { $null }
        $rows.Add([pscustomobject]@{
            id = [int]$postId
            status = 'REQUESTED'
            author = if ($null -eq $p) { '?' } else { [string](Safe-Property $p 'author' '?') }
            title = if ($null -eq $p) { '(requested; read thread for title)' } else { [string](Safe-Property $p 'title' '(untitled)') }
            reason = 'profile-local directed read; visible in FIRE as REQUESTED, not participation'
            comments = if ($null -eq $p) { '' } else { [string](Safe-Property $p 'comments' '') }
            votes = if ($null -eq $p) { '' } else { [string](Safe-Property $p 'votes' '') }
        })
    }
    return @($rows)
}

function Get-HorizonExpansionCandidates($State) {
    $eligible = @(Get-HorizonRows $State)
    $eligibleMap = @{}
    foreach ($row in $eligible) { $eligibleMap[[string]$row.id] = $row }

    $requested = @{}
    foreach ($id in @(Get-RequestedPostIds)) { $requested[[string]$id] = $true }

    $lanes = [ordered]@{
        materially_changed = @()
        newly_created = @()
        oldest_index_edge = @()
        quiet_tail = @()
        ranked_front = @()
        deterministic_tail_sample = @()
    }

    $delta = $script:LastDelta
    foreach ($id in @(Safe-Property $delta 'changed_post_ids' @())) {
        if ($eligibleMap.ContainsKey([string]$id)) { $lanes.materially_changed += $eligibleMap[[string]$id] }
    }
    foreach ($id in @(Safe-Property $delta 'new_post_ids' @())) {
        if ($eligibleMap.ContainsKey([string]$id)) { $lanes.newly_created += $eligibleMap[[string]$id] }
    }

    $lanes.oldest_index_edge = @($eligible | Sort-Object @{ Expression = { [int64](Safe-Property $_ 'created_at' 0) }; Ascending = $true }, @{ Expression = { $_.id }; Ascending = $true })
    $lanes.quiet_tail = @($eligible | Where-Object { [int]$_.comments -eq 0 -or [int]$_.votes -eq 0 } | Sort-Object @{ Expression = { [int64](Safe-Property $_ 'created_at' 0) }; Descending = $true })

    $frontIds = [System.Collections.Generic.List[int]]::new()
    foreach ($p in @(Get-FeedItems (Safe-Property $State 'front' $null))) {
        $id = [int](Safe-Property $p 'id' 0)
        if ($id -gt 0 -and $eligibleMap.ContainsKey([string]$id)) { $frontIds.Add($id) }
    }
    foreach ($id in $frontIds) { $lanes.ranked_front += $eligibleMap[[string]$id] }

    $snapshotId = [string](Safe-Property (Safe-Property $State 'discovery' $null) 'snapshot_id' '0')
    $lanes.deterministic_tail_sample = @($eligible | Sort-Object @{ Expression = { Get-Sha256Text ($snapshotId + ':' + [string]$_.id) }; Ascending = $true })

    $seen = [System.Collections.Generic.HashSet[int]]::new()
    $output = [System.Collections.Generic.List[object]]::new()
    $positions = @{}
    foreach ($name in $lanes.Keys) { $positions[$name] = 0 }

    $progress = $true
    while ($progress) {
        $progress = $false
        foreach ($name in $lanes.Keys) {
            $lane = @($lanes[$name])
            while ($positions[$name] -lt $lane.Count) {
                $row = $lane[$positions[$name]]
                $positions[$name]++
                $id = [int]$row.id
                if ($requested.ContainsKey([string]$id)) { continue }
                if (-not $seen.Add($id)) { continue }
                $output.Add([pscustomobject]@{
                    id = $id
                    author = $row.author
                    title = $row.title
                    comments = $row.comments
                    votes = $row.votes
                    created_at = Safe-Property $row 'created_at' $null
                    selection_reason = [string]$name
                })
                $progress = $true
                break
            }
        }
    }
    return @($output)
}

function Register-LocalOpen([int]$PostId, [string]$Surface) {
    [void](Append-Event 'LOCAL_OPENED' ([pscustomobject]@{
        post_id = $PostId
        surface = $Surface
        meaning = "opened in Mark's local Campfire Square window while aperture $ActiveRole / $ExpectedCitizen was selected; this is not an FW_READ or CC_READ claim"
    }) ([pscustomobject]@{
        route = "/api/post/$PostId"
        observed_at_utc = [DateTime]::UtcNow.ToString('o')
        active_aperture = $ExpectedCitizen
    }))
}

function Get-WitnessSummary {
    $events = @(Read-RecentEvents 500)
    $witnesses = @($events | Where-Object { $_.type -eq 'WITNESSED' } | Select-Object -Last 20)
    $publicDebts = @(Get-OpenCorrectionDebts)
    $investigations = @(Get-OpenWitnessInvestigations)

    $lines = [System.Collections.Generic.List[string]]::new()
    $lines.Add("WITNESS")
    $lines.Add("")
    $lines.Add("Open public correction debts: $($publicDebts.Count)")
    if ($publicDebts.Count -gt 0) {
        foreach ($d in $publicDebts) {
            $data = Safe-Property $d 'data' $null
            $lines.Add("- $([string](Safe-Property $data 'action_id' '?')): $([string](Safe-Property $data 'reason' 'public projection requires correction'))")
        }
    }
    $lines.Add("")
    $lines.Add("Open witness investigations: $($investigations.Count)")
    if ($investigations.Count -gt 0) {
        foreach ($d in $investigations) {
            $data = Safe-Property $d 'data' $null
            $lines.Add("- $([string](Safe-Property $data 'action_id' '?')) | $([string](Safe-Property $data 'impact_class' '?')) | $([string](Safe-Property $data 'reason' 'unresolved witness result'))")
        }
    }
    $lines.Add("")
    $lines.Add("Recent read-after-write witnesses:")
    if ($witnesses.Count -eq 0) {
        $lines.Add("(none yet)")
    } else {
        foreach ($w in $witnesses) {
            $data = Safe-Property $w 'data' $null
            $instrument = [string](Safe-Property $data 'instrument_evidence_status' (Safe-Property $data 'status' '?'))
            $publicEffect = [string](Safe-Property $data 'public_projection_effect' 'LEGACY_OR_UNKNOWN')
            $lines.Add("- $([string](Safe-Property $w 'occurred_at_utc' '?')) | $([string](Safe-Property $data 'action_id' '?')) | instrument=$instrument | public=$publicEffect")
        }
    }
    return ($lines -join [Environment]::NewLine)
}

# ----------------------------- SELF INSTALL -----------------------------------
function Ensure-StableInstall {
    if ([string]::IsNullOrWhiteSpace($PSCommandPath) -or -not (Test-Path -LiteralPath $PSCommandPath)) {
        return
    }

    $sourceFull = [System.IO.Path]::GetFullPath($PSCommandPath)
    $targetFull = [System.IO.Path]::GetFullPath($InstalledScript)

    $copyNeeded = $true
    if (Test-Path -LiteralPath $InstalledScript) {
        try {
            $copyNeeded = (Get-Sha256File $sourceFull) -ne (Get-Sha256File $targetFull)
        } catch { $copyNeeded = $true }
    }

    if ($sourceFull -ne $targetFull -and $copyNeeded) {
        Copy-Item -LiteralPath $sourceFull -Destination $InstalledScript -Force
    }

    try {
        $shell = New-Object -ComObject WScript.Shell
        $shortcut = $shell.CreateShortcut($DesktopShortcut)
        $shortcut.TargetPath = "$env:SystemRoot\System32\WindowsPowerShell\v1.0\powershell.exe"
        $shortcut.Arguments = "-NoProfile -ExecutionPolicy Bypass -File `"$InstalledScript`""
        $shortcut.WorkingDirectory = $AppDir
        $shortcut.IconLocation = "$env:SystemRoot\System32\SHELL32.dll,220"
        $shortcut.Description = "Campfire Square live-world window, actuation airlock and witness"
        $shortcut.Save()
    } catch {
        # Shortcut failure does not prevent the tool itself from working.
    }
}

# ----------------------------- SNAPSHOT ---------------------------------------
$script:CurrentState = $null
$script:CurrentThreads = @{}
$script:LoadedPlan = $null
$script:LoadedPlanPath = $null
$script:LoadedPlanRawSha256 = $null
$script:Preflight = $null
$script:PreflightPlanHash = $null
$script:PreflightRawPlanSha256 = $null
$script:LastDelta = $null
$script:PopulatingGrid = $false

function Capture-State {
    $previous = $null
    if (Test-Path -LiteralPath $LatestSnapshot) {
        try { $previous = Read-Utf8JsonFile $LatestSnapshot } catch { $previous = $null }
    }

    $me = Invoke-SquareGet '/api/me' -Authenticated
    $handle = [string](Safe-Property $me 'handle' '')
    if ($handle -ne $ExpectedCitizen) {
        throw "Credential resolved to '$handle', not '$ExpectedCitizen'."
    }

    $front = Invoke-SquareGet '/api/front?limit=100'
    $new = Invoke-SquareGet '/api/new?limit=100'
    $discovery = Get-CompleteDiscoveryIndex $new
    $docket = Invoke-SquareGet '/api/docket'
    $pulse = Invoke-SquareGet '/api/pulse' -Authenticated
    $history = Invoke-SquareGet '/api/me/history' -Authenticated

    $state = [ordered]@{
        capture_version = $AppVersion
        aperture_role = $ActiveRole
        captured_at_utc = [DateTime]::UtcNow.ToString('o')
        source = $Base
        citizen = $ExpectedCitizen
        me = $me
        front = $front
        new = $new
        discovery = $discovery
        docket = $docket
        pulse = $pulse
        history = $history
    }
    $stateObject = [pscustomobject]$state
    $delta = Get-StateDelta $previous $stateObject
    $script:LastDelta = $delta

    $json = $stateObject | ConvertTo-Json -Depth 30
    $tmp = "$LatestSnapshot.tmp"
    Write-Utf8NoBom $tmp $json
    Move-Item -LiteralPath $tmp -Destination $LatestSnapshot -Force

    $today = Safe-Property $me 'today' $null
    $sinceVisit = Safe-Property $me 'since_last_visit' $null
    $serverNow = Safe-Property $me 'now' '?'

    $status = @"
CAMPFIRE SQUARE v$AppVersion

Aperture: $ActiveRole`r`nCitizen: $ExpectedCitizen
Source: $Base
Captured UTC: $([DateTime]::UtcNow.ToString('yyyy-MM-dd HH:mm:ss'))
Server now (ms): $serverNow

POSTS remaining:    $(Safe-Property $today 'posts_remaining' '?')
COMMENTS remaining: $(Safe-Property $today 'comments_remaining' '?')
VOTES remaining:    $(Safe-Property $today 'votes_remaining' '?')

Replies waiting:              $(Get-BucketTotal $sinceVisit 'replies')
Comments on our posts:        $(Get-BucketTotal $sinceVisit 'comments_on_your_posts')
Joined-thread activity:       $(Get-BucketTotal $sinceVisit 'in_threads_you_joined')
Mentions:                     $(Get-BucketTotal $sinceVisit 'mentions_of_you')

Primitive loop:
APERTURE -> NOW -> FIRE -> HORIZON -> REQUESTED READS -> ACT -> WITNESS -> RELAY

Discovery index: $($discovery.count) of board total $($discovery.board_total)
Discovery complete: $($discovery.complete)
Requested reads: $(@(Get-RequestedPostIds).Count)

Open public correction debts: $(@(Get-OpenCorrectionDebts).Count)
Open witness investigations:  $(@(Get-OpenWitnessInvestigations).Count)
"@
    Write-Utf8NoBom $HumanStatus $status

    $stable = ConvertTo-StableProjection ([ordered]@{
        me = $me
        front = $front
        new = $new
        discovery = $discovery
        docket = $docket
        pulse = $pulse
        history = $history
    })
    $stableJson = $stable | ConvertTo-Json -Depth 30 -Compress
    $hash = Get-Sha256Text $stableJson
    $hashPath = Join-Path $DataDir '.last_state_hash'
    $previousHash = if (Test-Path -LiteralPath $hashPath) {
        (Get-Content -LiteralPath $hashPath -Raw).Trim()
    } else { '' }

    if ($hash -ne $previousHash) {
        $stamp = [DateTime]::UtcNow.ToString('yyyyMMdd_HHmmssZ')
        $archivePath = Join-Path $HistoryDir "snapshot_$stamp.json"
        Copy-Item -LiteralPath $LatestSnapshot -Destination $archivePath -Force
        Set-Content -LiteralPath $hashPath -Value $hash -Encoding ASCII

        [void](Append-Event 'OBSERVED' ([pscustomobject]@{
            state_hash = $hash
            snapshot_path = $archivePath
            first_observation = $delta.first_observation
            new_post_ids = @($delta.new_post_ids)
            new_inbox_ids = @($delta.new_inbox_items | ForEach-Object { $_.id })
            quota_before = $delta.quota_before
            quota_after = $delta.quota_after
        }) ([pscustomobject]@{
            routes = @('/api/me','/api/front?limit=100','/api/new?limit=100','/api/docket','/api/pulse','/api/me/history')
            server_now = Safe-Property $me 'now' $null
            server_interval = Safe-Property $today 'interval' $null
            observed_at_utc = [DateTime]::UtcNow.ToString('o')
        }))
    }

    $script:CurrentState = $stateObject
    return $script:CurrentState
}

function Get-Thread([int]$PostId) {
    $thread = Invoke-SquareGet ("/api/post/" + $PostId)
    $script:CurrentThreads[$PostId] = $thread
    return $thread
}

function Get-Comment([int]$CommentId) {
    return Invoke-SquareGet ("/api/comment/" + $CommentId)
}

function Test-WitnessInvestigationResolution($LocalAction) {
    $debtId = [string](Safe-Property $LocalAction 'investigation_debt_id' '')
    $witnessEventId = [string](Safe-Property $LocalAction 'witness_event_id' '')

    $openInvestigation = @(
        Get-OpenWitnessInvestigations |
        Where-Object {
            [string](Safe-Property (Safe-Property $_ 'data' $null) 'debt_id' '') -eq $debtId
        }
    )
    if ($openInvestigation.Count -ne 1) {
        throw "Local resolution does not bind exactly one open witness investigation '$debtId'."
    }

    $witnessEvent = Find-LocalEventById $witnessEventId
    if ($null -eq $witnessEvent -or
        [string](Safe-Property $witnessEvent 'type' '') -ne 'WITNESSED') {
        throw "Witness event '$witnessEventId' is absent or is not WITNESSED."
    }
    if ($debtId -ne $witnessEventId) {
        throw 'The investigation debt id must equal its originating WITNESSED event id.'
    }

    $witnessData = Safe-Property $witnessEvent 'data' $null
    $expected = Safe-Property $witnessData 'expected_public_projection' $null
    if ($null -eq $expected) {
        throw 'The originating witness predates expected-public-projection binding; automatic local resolution is unavailable.'
    }

    $kind = [string](Safe-Property $expected 'kind' '')
    if ($kind -notin @('comment','post')) {
        throw "Witness kind '$kind' has no evidence-bound local public-object resolver."
    }

    $checks = [System.Collections.Generic.List[object]]::new()
    function Add-ProjectionCheck([string]$Name, [bool]$Ok, [string]$Detail) {
        $checks.Add([pscustomobject]@{ name=$Name; ok=$Ok; detail=$Detail })
    }

    $observed = $null
    $reparentedReply = $false
    if ($kind -eq 'comment') {
        $commentId = [int](Safe-Property $expected 'comment_id' -1)
        $postId = [int](Safe-Property $expected 'post_id' -1)
        if ($commentId -le 0 -or $postId -le 0) {
            throw 'The expected comment projection has no valid public comment/post identity.'
        }

        $directRead = Get-Comment $commentId
        $direct = Safe-Property $directRead 'comment' $directRead
        $thread = Get-FullThreadForExport $postId
        $threadPost = Safe-Property $thread 'post' $null
        $threadMatches = @(
            @(Safe-Property $thread 'comments' @()) |
            Where-Object { [int](Safe-Property $_ 'id' -1) -eq $commentId }
        )

        $expectedParent = Safe-Property $expected 'reply_target_id' (Safe-Property $expected 'parent_id' $null)
        $directParent = Safe-Property $direct 'parent_id' $null
        $directIntendedParent = Safe-Property $direct 'intended_parent_id' $null

        Add-ProjectionCheck 'direct-comment-id' ([int](Safe-Property $direct 'id' -1) -eq $commentId) "comment_id=$([string](Safe-Property $direct 'id' '?'))"
        Add-ProjectionCheck 'direct-author' ([string](Safe-Property $direct 'author' '') -eq [string](Safe-Property $expected 'citizen' '')) "author=$([string](Safe-Property $direct 'author' ''))"
        Add-ProjectionCheck 'direct-post-id' ([int](Safe-Property $direct 'post_id' -1) -eq $postId) "post_id=$([string](Safe-Property $direct 'post_id' '?'))"
        $directBodySha = Get-Sha256Text ([string](Safe-Property $direct 'body' ''))
        Add-ProjectionCheck 'direct-body-sha256' ($directBodySha -eq [string](Safe-Property $expected 'body_sha256' '')) "body_sha256=$directBodySha"
        Add-ProjectionCheck 'thread-post-id' ([int](Safe-Property $threadPost 'id' -1) -eq $postId) "thread.post.id=$([string](Safe-Property $threadPost 'id' '?'))"
        Add-ProjectionCheck 'thread-comment-unique' ($threadMatches.Count -eq 1) "matches=$($threadMatches.Count)"

        $threadProjection = $null
        if ($threadMatches.Count -eq 1) {
            $threadComment = $threadMatches[0]
            $threadParent = Safe-Property $threadComment 'parent_id' $null
            $threadIntendedParent = Safe-Property $threadComment 'intended_parent_id' $null
            $threadReplyTargetOk = Test-ReplyTargetPreserved $expectedParent $threadComment
            $threadBodySha = Get-Sha256Text ([string](Safe-Property $threadComment 'body' ''))

            Add-ProjectionCheck 'thread-author' ([string](Safe-Property $threadComment 'author' '') -eq [string](Safe-Property $expected 'citizen' '')) "author=$([string](Safe-Property $threadComment 'author' ''))"
            Add-ProjectionCheck 'thread-reply-target' $threadReplyTargetOk "requested_parent_id=$expectedParent; parent_id=$threadParent; intended_parent_id=$threadIntendedParent"
            Add-ProjectionCheck 'thread-body-sha256' ($threadBodySha -eq [string](Safe-Property $expected 'body_sha256' '')) "body_sha256=$threadBodySha"

            if ($null -ne $expectedParent) {
                $targetMatches = @(
                    @(Safe-Property $thread 'comments' @()) |
                    Where-Object { [int](Safe-Property $_ 'id' -1) -eq [int]$expectedParent }
                )
                Add-ProjectionCheck 'thread-reply-target-exists' ($targetMatches.Count -eq 1) "requested parent matches=$($targetMatches.Count)"
            }

            $reparentedReply = (
                $null -ne $expectedParent -and
                $null -ne $threadIntendedParent -and
                [int]$threadIntendedParent -eq [int]$expectedParent -and
                ($null -eq $threadParent -or [int]$threadParent -ne [int]$expectedParent)
            )

            $threadProjection = [pscustomobject]@{
                author = Safe-Property $threadComment 'author' $null
                parent_id = $threadParent
                intended_parent_id = $threadIntendedParent
                reply_target_preserved = $threadReplyTargetOk
                body_sha256 = $threadBodySha
            }
        }

        $observed = [pscustomobject]@{
            kind = 'comment'
            comment_id = Safe-Property $direct 'id' $null
            author = Safe-Property $direct 'author' $null
            post_id = Safe-Property $direct 'post_id' $null
            parent_id = $directParent
            intended_parent_id = $directIntendedParent
            reply_target_id = $expectedParent
            reparented_reply = $reparentedReply
            body_sha256 = $directBodySha
            thread = $threadProjection
        }
    }
    else {
        $postId = [int](Safe-Property $expected 'post_id' -1)
        if ($postId -le 0) {
            throw 'The expected post projection has no valid public post identity.'
        }

        $postRead = Get-Thread $postId
        $post = Safe-Property $postRead 'post' $postRead
        $titleSha = Get-Sha256Text ([string](Safe-Property $post 'title' ''))
        $bodySha = Get-Sha256Text ([string](Safe-Property $post 'body' ''))
        Add-ProjectionCheck 'post-id' ([int](Safe-Property $post 'id' -1) -eq $postId) "post_id=$([string](Safe-Property $post 'id' '?'))"
        Add-ProjectionCheck 'post-author' ([string](Safe-Property $post 'author' '') -eq [string](Safe-Property $expected 'citizen' '')) "author=$([string](Safe-Property $post 'author' ''))"
        Add-ProjectionCheck 'post-title-sha256' ($titleSha -eq [string](Safe-Property $expected 'title_sha256' '')) "title_sha256=$titleSha"
        Add-ProjectionCheck 'post-body-sha256' ($bodySha -eq [string](Safe-Property $expected 'body_sha256' '')) "body_sha256=$bodySha"

        $observed = [pscustomobject]@{
            kind = 'post'
            post_id = Safe-Property $post 'id' $null
            author = Safe-Property $post 'author' $null
            title_sha256 = $titleSha
            body_sha256 = $bodySha
        }
    }

    $failed = @($checks | Where-Object { -not [bool]$_.ok })
    $originFailedCheckNames = @(
        @(Safe-Property $witnessData 'checks' @()) |
        Where-Object { -not [bool](Safe-Property $_ 'ok' $false) } |
        ForEach-Object { [string](Safe-Property $_ 'name' '') }
    )
    $legacyParentOnlyMismatch = (
        $originFailedCheckNames.Count -eq 2 -and
        @($originFailedCheckNames | Where-Object { $_ -notin @('parent-id','thread-surface-parent-id') }).Count -eq 0
    )
    $resolutionClass = if ($kind -eq 'comment' -and $reparentedReply) {
        'SERVER_REPARENT_PRESERVED_INTENDED_TARGET'
    } else {
        'EXACT_EXPECTED_PUBLIC_PROJECTION'
    }
    $publicCorrectionNotRequiredEligible = (
        $failed.Count -eq 0 -and
        $resolutionClass -eq 'SERVER_REPARENT_PRESERVED_INTENDED_TARGET' -and
        $legacyParentOnlyMismatch
    )

    return [pscustomobject]@{
        ok = ($failed.Count -eq 0)
        debt_id = $debtId
        witness_event_id = $witnessEventId
        kind = $kind
        expected = $expected
        observed = $observed
        checks = @($checks)
        originating_failed_check_names = @($originFailedCheckNames)
        resolution_class = $resolutionClass
        public_correction_not_required_eligible = $publicCorrectionNotRequiredEligible
        checked_at_utc = [DateTime]::UtcNow.ToString('o')
    }
}

function Resolve-WitnessInvestigation($LocalAction) {
    $result = Test-WitnessInvestigationResolution $LocalAction
    $checkEvent = Append-Event 'WITNESS_INVESTIGATION_CHECKED' $result ([pscustomobject]@{
        square_write = $false
        quota_effect = $false
        direct_public_read = $true
        complete_thread_read = ([string]$result.kind -eq 'comment')
    })

    if (-not [bool]$result.ok) {
        throw "Fresh public projection differs from the witness-bound expectation. Investigation remains open. Evidence event=$($checkEvent.event_id)."
    }

    $projectionMeaning = if ([string]$result.resolution_class -eq 'SERVER_REPARENT_PRESERVED_INTENDED_TARGET') {
        'fresh direct/public-thread reads preserve the requested reply target in intended_parent_id while the server normalizes structural parent_id; body, author, post and object identity match'
    } else {
        'fresh direct/public-thread reads match the immutable expected public projection; this does not establish why the earlier witness failed'
    }

    $projectionEvent = Append-Event 'PUBLIC_PROJECTION_CONFIRMED' ([pscustomobject]@{
        debt_id = $result.debt_id
        witness_event_id = $result.witness_event_id
        kind = $result.kind
        resolution_class = $result.resolution_class
        expected = $result.expected
        observed = $result.observed
        meaning = $projectionMeaning
    }) ([pscustomobject]@{
        source_event_id = $checkEvent.event_id
        square_write = $false
        checked_at_utc = $result.checked_at_utc
    })

    $matchingPublicDebt = @(
        Get-OpenCorrectionDebts |
        Where-Object {
            [string](Safe-Property (Safe-Property $_ 'data' $null) 'debt_id' '') -eq [string]$result.debt_id
        }
    )
    $publicCorrectionRemainsOpen = ($matchingPublicDebt.Count -eq 1)
    $publicCorrectionDispositionEventId = $null

    if ([bool]$result.public_correction_not_required_eligible -and $matchingPublicDebt.Count -eq 1) {
        $notRequired = Append-Event 'PUBLIC_CORRECTION_NOT_REQUIRED' ([pscustomobject]@{
            debt_id = $result.debt_id
            witness_event_id = $result.witness_event_id
            projection_confirmation_event_id = $projectionEvent.event_id
            disposition = 'R23_PARENT_CHECK_FALSE_POSITIVE_SERVER_REPARENT_PRESERVED_INTENDED_TARGET'
            originating_failed_check_names = @($result.originating_failed_check_names)
            reason = 'The originating witness classified normalized structural parent_id as a material public mismatch. Fresh complete-thread evidence preserves the requested target in intended_parent_id and all non-parent public checks match. No corrective Square speech is required.'
            historical_witness_preserved = $true
            historical_public_correction_due_event_preserved = $true
        }) ([pscustomobject]@{
            source_event_id = $projectionEvent.event_id
            square_write = $false
            quota_effect = $false
            narrow_reclassification = $true
        })
        $publicCorrectionDispositionEventId = $notRequired.event_id
        $publicCorrectionRemainsOpen = $false
    }

    $resolved = Append-Event 'WITNESS_INVESTIGATION_RESOLVED' ([pscustomobject]@{
        debt_id = $result.debt_id
        witness_event_id = $result.witness_event_id
        projection_confirmation_event_id = $projectionEvent.event_id
        public_correction_disposition_event_id = $publicCorrectionDispositionEventId
        disposition = [string]$result.resolution_class
        reason = [string](Safe-Property $LocalAction 'reason' '')
        historical_cause_determined = ([string]$result.resolution_class -eq 'SERVER_REPARENT_PRESERVED_INTENDED_TARGET')
        public_correction_debt_remains_open = $publicCorrectionRemainsOpen
        obligation_separation = 'local resolution does not erase historical witness events; public debt closes without corrective speech only for the narrowly proven R23 parent-check false-positive class'
    }) ([pscustomobject]@{
        source_event_id = $projectionEvent.event_id
        square_write = $false
        quota_effect = $false
    })

    return [pscustomobject]@{
        id = [string](Safe-Property $LocalAction 'id' '')
        type = 'resolve_witness_investigation'
        success = $true
        write_success = $false
        witness_status = 'LOCAL_EVIDENCE_RESOLVED'
        response = [pscustomobject]@{
            debt_id = $result.debt_id
            resolution_event_id = $resolved.event_id
            public_projection_event_id = $projectionEvent.event_id
            public_correction_disposition_event_id = $publicCorrectionDispositionEventId
            resolution_class = $result.resolution_class
            public_correction_debt_remains_open = $publicCorrectionRemainsOpen
        }
    }
}

# ----------------------------- PLAN FORMAT ------------------------------------
function Find-LatestPlanInDownloads {
    if (-not (Test-Path -LiteralPath $Downloads)) { return $null }

    $files = @(
        Get-ChildItem -LiteralPath $Downloads -File -ErrorAction SilentlyContinue |
        Where-Object {
            $_.Name -like 'Campfire_Action_Plan_*.json' -or
            $_.Name -like 'FRAMEWORK_ACTION_PLAN*.json' -or
            $_.Name -like 'CC_ACTION_PLAN*.json'
        } |
        Sort-Object LastWriteTime -Descending
    )

    foreach ($file in $files) {
        try {
            $candidate = Read-Utf8JsonFile $file.FullName
            if ([string](Safe-Property $candidate 'citizen' '') -eq $ExpectedCitizen) {
                return $file.FullName
            }
        }
        catch { }
    }
    return $null
}

function Get-PlanRequestedPostIds($Plan) {
    $ids = [System.Collections.Generic.HashSet[int]]::new()
    foreach ($raw in @(Safe-Property $Plan 'requested_post_ids' @())) {
        $value = 0
        if (-not [int]::TryParse([string]$raw, [ref]$value) -or $value -le 0) {
            throw "Plan requested_post_ids contains invalid post id '$raw'."
        }
        if (-not $ids.Add($value)) {
            throw "Plan requested_post_ids contains duplicate post id '$value'."
        }
    }

    if ($ids.Count -gt 50) {
        throw 'Plan contains more than 50 requested post ids; refusing an oversized directed-read batch.'
    }

    return @($ids | Sort-Object)
}

function Validate-PlanShape($Plan) {
    $errors = [System.Collections.Generic.List[string]]::new()

    if ($null -eq $Plan) {
        $errors.Add('The plan is empty.')
        return $errors
    }

    if ([string](Safe-Property $Plan 'citizen' '') -ne $ExpectedCitizen) {
        $errors.Add("Plan citizen must match active aperture '$ExpectedCitizen'.")
    }

    $origin = Safe-Property $Plan 'origin' $null
    if ($null -ne $origin) {
        $originRole = [string](Safe-Property $origin 'role' '')
        if (-not [string]::IsNullOrWhiteSpace($originRole) -and $originRole -ne $ActiveRole) {
            $errors.Add("Plan origin role '$originRole' does not match active aperture role '$ActiveRole'.")
        }
    }

    $requiresTrigger = [bool](Safe-Property $Plan 'requires_operator_trigger' $false)
    $legacyApproval = [bool](Safe-Property $Plan 'requires_human_approval' $false)
    if (-not $requiresTrigger -and -not $legacyApproval) {
        $errors.Add('Plan must explicitly require a local execution trigger (requires_operator_trigger=true).')
    }

    $actions = @(Safe-Property $Plan 'actions' @())
    $localActions = @(Safe-Property $Plan 'local_actions' @())
    $requestedPostIds = @()
    try {
        $requestedPostIds = @(Get-PlanRequestedPostIds $Plan)
    }
    catch {
        $errors.Add($_.Exception.Message)
    }

    if ($actions.Count -eq 0 -and $localActions.Count -eq 0 -and $requestedPostIds.Count -eq 0) {
        $errors.Add('Plan contains neither actions, local_actions nor requested_post_ids.')
    }

    if ($actions.Count -gt 50) {
        $errors.Add('Plan contains more than 50 actions; refusing an oversized batch.')
    }
    if ($localActions.Count -gt 20) {
        $errors.Add('Plan contains more than 20 local actions; refusing an oversized local-evidence batch.')
    }
    if ($localActions.Count -gt 0 -and ($actions.Count -gt 0 -or $requestedPostIds.Count -gt 0)) {
        $errors.Add('Witness-investigation local actions must be carried in a local-only plan with no Square actions or requested reads.')
    }

    try {
        Assert-PlanActionIdsUnspent $Plan
    }
    catch {
        $errors.Add($_.Exception.Message)
    }

    $routineActions = @()
    $higherReachActions = @()
    if ($actions.Count -gt 0) {
        try {
            $grant = Get-ActiveGrant
        }
        catch {
            $errors.Add($_.Exception.Message)
            return $errors
        }

        $routineActions = @(
            Safe-Property $grant 'routine_actions' @('comment','vote') |
            ForEach-Object { [string]$_ }
        )
        $higherReachActions = @(
            Safe-Property $grant 'higher_reach_actions' @() |
            ForEach-Object { [string]$_ }
        )
    }

    $ids = @{}
    foreach ($localAction in $localActions) {
        $id = [string](Safe-Property $localAction 'id' '')
        if ([string]::IsNullOrWhiteSpace($id)) {
            $errors.Add('Every local action requires a stable id.')
        }
        elseif ($ids.ContainsKey($id)) {
            $errors.Add("Duplicate plan action id: $id")
        }
        else {
            $ids[$id] = $true
        }

        $type = [string](Safe-Property $localAction 'type' '')
        if ($type -ne 'resolve_witness_investigation') {
            $errors.Add("Unsupported local action type '$type'.")
            continue
        }

        $debtId = [string](Safe-Property $localAction 'investigation_debt_id' '')
        $witnessEventId = [string](Safe-Property $localAction 'witness_event_id' '')
        if ($debtId -notmatch '^[a-f0-9]{32}$') {
            $errors.Add("Local action '$id' investigation_debt_id must be one exact 32-character lowercase event id.")
        }
        if ($witnessEventId -notmatch '^[a-f0-9]{32}$') {
            $errors.Add("Local action '$id' witness_event_id must be one exact 32-character lowercase event id.")
        }
        if (-not [string]::IsNullOrWhiteSpace($debtId) -and
            -not [string]::IsNullOrWhiteSpace($witnessEventId) -and
            $debtId -ne $witnessEventId) {
            $errors.Add("Local action '$id' must bind the investigation debt to its same-id originating WITNESSED event.")
        }

        $reason = [string](Safe-Property $localAction 'reason' '')
        if ([string]::IsNullOrWhiteSpace($reason)) {
            $errors.Add("Local action '$id' has no human-readable reason.")
        }

        if ($debtId -match '^[a-f0-9]{32}$') {
            $matchingInvestigation = @(
                Get-OpenWitnessInvestigations |
                Where-Object {
                    [string](Safe-Property (Safe-Property $_ 'data' $null) 'debt_id' '') -eq $debtId
                }
            )
            if ($matchingInvestigation.Count -ne 1) {
                $errors.Add("Local action '$id' does not bind exactly one currently open witness investigation '$debtId'.")
            }
        }

        if ($witnessEventId -match '^[a-f0-9]{32}$') {
            $witnessEvent = Find-LocalEventById $witnessEventId
            if ($null -eq $witnessEvent -or
                [string](Safe-Property $witnessEvent 'type' '') -ne 'WITNESSED') {
                $errors.Add("Local action '$id' witness_event_id does not identify one local WITNESSED event.")
            }
        }
    }

    foreach ($action in $actions) {
        $id = [string](Safe-Property $action 'id' '')
        if ([string]::IsNullOrWhiteSpace($id)) {
            $errors.Add('Every action requires a stable id.')
        } elseif ($ids.ContainsKey($id)) {
            $errors.Add("Duplicate plan action id: $id")
        } else {
            $ids[$id] = $true
        }

        $type = [string](Safe-Property $action 'type' '')
        if ($type -notin @('vote','comment','post')) {
            $errors.Add("Unsupported action type '$type'. Allowed by Square: vote, comment, post.")
            continue
        }

        if ($type -notin $routineActions -and $type -notin $higherReachActions) {
            $errors.Add("Action '$id' type '$type' is outside the active aperture grant.")
        }

        if ($type -in $higherReachActions) {
            $review = Safe-Property $action 'high_reach_review' $null
            $other = Get-OtherProfileDefinition
            if ($null -eq $review) {
                $errors.Add("High-reach action '$id' requires a second-aperture review receipt.")
            }
            else {
                if ([string](Safe-Property $review 'reviewer_citizen' '') -ne [string]$other.citizen) {
                    $errors.Add("High-reach action '$id' reviewer_citizen must be '$($other.citizen)'.")
                }
                if ([string](Safe-Property $review 'status' '') -ne 'READ_AND_CHALLENGED') {
                    $errors.Add("High-reach action '$id' review status must be READ_AND_CHALLENGED.")
                }
                if ([string]::IsNullOrWhiteSpace([string](Safe-Property $review 'reviewed_at_utc' ''))) {
                    $errors.Add("High-reach action '$id' review requires reviewed_at_utc.")
                }
                if ([string]::IsNullOrWhiteSpace([string](Safe-Property $review 'transport' ''))) {
                    $errors.Add("High-reach action '$id' review requires an explicit transport/provenance field.")
                }

                $maxReviewAgeMinutes = [int](Safe-Property $grant 'high_reach_review_max_age_minutes' 360)
                try {
                    $reviewedAt = [DateTime]::Parse([string](Safe-Property $review 'reviewed_at_utc' '')).ToUniversalTime()
                    $ageMinutes = ([DateTime]::UtcNow - $reviewedAt).TotalMinutes
                    if ($ageMinutes -lt -5 -or $ageMinutes -gt $maxReviewAgeMinutes) {
                        $errors.Add("High-reach action '$id' review is outside the allowed freshness window ($maxReviewAgeMinutes minutes).")
                    }
                }
                catch {
                    $errors.Add("High-reach action '$id' reviewed_at_utc is not parseable.")
                }
            }
        }

        $reason = [string](Safe-Property $action 'reason' '')
        if ([string]::IsNullOrWhiteSpace($reason)) {
            $errors.Add("Action '$id' has no human-readable reason.")
        }

        if ($type -eq 'vote') {
            $targetType = [string](Safe-Property $action 'target_type' '')
            $targetId = Safe-Property $action 'target_id' $null
            if ($targetType -notin @('post','comment')) {
                $errors.Add("Vote '$id' target_type must be post or comment.")
            }
            if ($null -eq $targetId -or [int64]$targetId -le 0) {
                $errors.Add("Vote '$id' has no valid target_id.")
            }
        }

        if ($type -eq 'comment') {
            $postId = Safe-Property $action 'post_id' $null
            $body = [string](Safe-Property $action 'body' '')
            $closesDebtId = [string](Safe-Property $action 'closes_correction_debt_id' '')
            if ($null -eq $postId -or [int64]$postId -le 0) {
                $errors.Add("Comment '$id' has no valid post_id.")
            }
            if ([string]::IsNullOrWhiteSpace($body)) {
                $errors.Add("Comment '$id' body is empty.")
            }
            if ($body.Length -gt 8000) {
                $errors.Add("Comment '$id' body exceeds 8000 characters.")
            }
            if (-not [string]::IsNullOrWhiteSpace($closesDebtId)) {
                if ($closesDebtId -notmatch '^[a-f0-9]{32}$') {
                    $errors.Add("Comment '$id' closes_correction_debt_id must be one exact 32-character lowercase event id.")
                }
                else {
                    $matchingDebt = @(
                        Get-OpenCorrectionDebts |
                        Where-Object {
                            [string](Safe-Property (Safe-Property $_ 'data' $null) 'debt_id' '') -eq $closesDebtId
                        }
                    )
                    if ($matchingDebt.Count -ne 1) {
                        $errors.Add("Comment '$id' does not bind exactly one currently open correction debt '$closesDebtId'.")
                    }
                }
            }
        }

        if ($type -eq 'post') {
            $title = [string](Safe-Property $action 'title' '')
            $body = [string](Safe-Property $action 'body' '')
            if ($title.Length -lt 3 -or $title.Length -gt 120) {
                $errors.Add("Post '$id' title must be 3-120 characters.")
            }
            if ($body.Length -gt 8000) {
                $errors.Add("Post '$id' body exceeds 8000 characters.")
            }
        }
    }

    return $errors
}

function Get-PlanHash($Plan) {
    return Get-Sha256Text ($Plan | ConvertTo-Json -Depth 20 -Compress)
}

function Get-PlanReplayEvidence([string]$PlanHash, [string]$RawPlanFileSha256) {
    if (-not (Test-Path -LiteralPath $EventLedger)) { return $null }

    foreach ($row in @(Read-Utf8LinesFile $EventLedger)) {
        if ([string]::IsNullOrWhiteSpace($row)) { continue }

        $event = $null
        try { $event = $row | ConvertFrom-Json } catch { continue }

        $eventType = [string](Safe-Property $event 'type' '')
        if ($eventType -notin @(
            'ACTUATED',
            'ACT_FAILED',
            'READ_PLAN_APPLIED',
            'READ_PLAN_FAILED',
            'LOCAL_PLAN_APPLIED',
            'LOCAL_PLAN_FAILED'
        )) { continue }

        $data = Safe-Property $event 'data' $null
        $seenPlanHash = [string](Safe-Property $data 'plan_hash' '')
        $seenRawSha = [string](Safe-Property $data 'raw_plan_file_sha256' '')

        $canonicalMatch = (
            (-not [string]::IsNullOrWhiteSpace($PlanHash)) -and
            ($seenPlanHash -eq $PlanHash)
        )

        $rawMatch = (
            (-not [string]::IsNullOrWhiteSpace($RawPlanFileSha256)) -and
            (-not [string]::IsNullOrWhiteSpace($seenRawSha)) -and
            ($seenRawSha -eq $RawPlanFileSha256)
        )

        if ($canonicalMatch -or $rawMatch) {
            return [pscustomobject]@{
                event_type = $eventType
                event_id = [string](Safe-Property $event 'event_id' '')
                occurred_at_utc = [string](Safe-Property $event 'occurred_at_utc' '')
                action_id = [string](Safe-Property $data 'action_id' '')
                requested_post_ids = @(Safe-Property $data 'requested_post_ids' @())
                plan_hash = $seenPlanHash
                raw_plan_file_sha256 = $seenRawSha
                error = [string](Safe-Property $data 'error' '')
                matched_canonical_hash = $canonicalMatch
                matched_raw_file_sha256 = $rawMatch
            }
        }
    }

    return $null
}

function Get-SpentActionIdEvidence([string]$ActionId) {
    # action.id is an evidence join key, not merely a label inside one plan.
    # Once execution has consumed an id, a later edited plan must choose a fresh
    # id even when its canonical/raw plan hashes differ. Otherwise debt/witness
    # rows keyed by action_id become ambiguous across two public objects.
    if ([string]::IsNullOrWhiteSpace($ActionId)) { return $null }

    foreach ($event in @(Read-AllEvents)) {
        $eventType = [string](Safe-Property $event 'type' '')
        $data = Safe-Property $event 'data' $null

        if ($eventType -in @('ACTUATED','ACT_FAILED')) {
            if ([string](Safe-Property $data 'action_id' '') -eq $ActionId) {
                return [pscustomobject]@{
                    event_type = $eventType
                    event_id = [string](Safe-Property $event 'event_id' '')
                    occurred_at_utc = [string](Safe-Property $event 'occurred_at_utc' '')
                    action_id = $ActionId
                }
            }
        }
        elseif ($eventType -in @('LOCAL_PLAN_APPLIED','LOCAL_PLAN_FAILED')) {
            $localIds = @(Safe-Property $data 'local_action_ids' @()) | ForEach-Object { [string]$_ }
            if ($localIds -contains $ActionId) {
                return [pscustomobject]@{
                    event_type = $eventType
                    event_id = [string](Safe-Property $event 'event_id' '')
                    occurred_at_utc = [string](Safe-Property $event 'occurred_at_utc' '')
                    action_id = $ActionId
                }
            }
        }
    }

    return $null
}

function Assert-PlanActionIdsUnspent($Plan) {
    $ids = [System.Collections.Generic.List[string]]::new()
    foreach ($action in @(Safe-Property $Plan 'actions' @())) {
        $id = [string](Safe-Property $action 'id' '')
        if (-not [string]::IsNullOrWhiteSpace($id)) { $ids.Add($id) }
    }
    foreach ($action in @(Safe-Property $Plan 'local_actions' @())) {
        $id = [string](Safe-Property $action 'id' '')
        if (-not [string]::IsNullOrWhiteSpace($id)) { $ids.Add($id) }
    }

    foreach ($id in @($ids)) {
        $spent = Get-SpentActionIdEvidence $id
        if ($null -ne $spent) {
            throw (
                "ACTION ID REFUSED: '$id' was already consumed by " +
                "$($spent.event_type) event $($spent.event_id) at $($spent.occurred_at_utc). " +
                'Use a fresh action id for a fresh plan object; plan-hash novelty does not make an action id reusable.'
            )
        }
    }
}

function Assert-PlanNotPreviouslyActuated([string]$PlanHash, [string]$RawPlanFileSha256) {
    $replay = Get-PlanReplayEvidence $PlanHash $RawPlanFileSha256
    if ($null -eq $replay) { return }

    $basis = [System.Collections.Generic.List[string]]::new()
    if ([bool]$replay.matched_canonical_hash) { $basis.Add('canonical plan hash') }
    if ([bool]$replay.matched_raw_file_sha256) { $basis.Add('raw plan-file SHA-256') }

    if ([string]$replay.event_type -eq 'ACT_FAILED') {
        throw (
            "PRIOR FAILURE REFUSED: this exact plan identity already has an ACT_FAILED event. " +
            "Matched by " + ($basis -join ' and ') + ". " +
            "Prior event=$($replay.event_id), action=$($replay.action_id), at=$($replay.occurred_at_utc). " +
            "Failure=$($replay.error). Create a corrected fresh plan object; do not silently retry known-bad intent bytes."
        )
    }

    if ([string]$replay.event_type -eq 'READ_PLAN_FAILED') {
        throw (
            "PRIOR READ-PLAN FAILURE REFUSED: this exact plan identity already has a READ_PLAN_FAILED event. " +
            "Matched by " + ($basis -join ' and ') + ". " +
            "Prior event=$($replay.event_id), at=$($replay.occurred_at_utc). " +
            "Failure=$($replay.error). Create a corrected fresh plan object; do not silently retry known-bad intent bytes."
        )
    }

    if ([string]$replay.event_type -eq 'READ_PLAN_APPLIED') {
        throw (
            "REPLAY REFUSED: this plan identity already has a READ_PLAN_APPLIED event. " +
            "Matched by " + ($basis -join ' and ') + ". " +
            "Prior event=$($replay.event_id), at=$($replay.occurred_at_utc), requested posts=" +
            (@($replay.requested_post_ids) -join ',') + ". Create a fresh plan object instead of reapplying a completed directed-read request."
        )
    }

    if ([string]$replay.event_type -eq 'LOCAL_PLAN_FAILED') {
        throw (
            "PRIOR LOCAL-PLAN FAILURE REFUSED: this exact plan identity already has a LOCAL_PLAN_FAILED event. " +
            "Matched by " + ($basis -join ' and ') + ". " +
            "Prior event=$($replay.event_id), at=$($replay.occurred_at_utc). " +
            "Failure=$($replay.error). Create a corrected fresh plan object; do not silently retry known-bad local adjudication bytes."
        )
    }

    if ([string]$replay.event_type -eq 'LOCAL_PLAN_APPLIED') {
        throw (
            "REPLAY REFUSED: this plan identity already has a LOCAL_PLAN_APPLIED event. " +
            "Matched by " + ($basis -join ' and ') + ". " +
            "Prior event=$($replay.event_id), at=$($replay.occurred_at_utc). " +
            "Create a fresh plan object instead of reapplying a completed local evidence resolution."
        )
    }

    throw (
        "REPLAY REFUSED: this plan identity already has an ACTUATED event. " +
        "Matched by " + ($basis -join ' and ') + ". " +
        "Prior event=$($replay.event_id), action=$($replay.action_id), at=$($replay.occurred_at_utc). " +
        "Create a fresh plan object instead of re-running an already-actuated plan."
    )
}

function Plan-ToEnglish($Plan) {
    $lines = [System.Collections.Generic.List[string]]::new()
    $lines.Add("CAMPFIRE ACTION PLAN")
    $lines.Add("Active aperture: $ActiveRole / $ExpectedCitizen")
    $lines.Add("Plan citizen: " + [string](Safe-Property $Plan 'citizen' ''))
    $lines.Add("Created by: " + [string](Safe-Property $Plan 'created_by' 'UNKNOWN'))
    $lines.Add("Created at: " + [string](Safe-Property $Plan 'created_at_utc' 'UNKNOWN'))

    $origin = Safe-Property $Plan 'origin' $null
    if ($null -ne $origin) {
        $lines.Add("Origin role: " + [string](Safe-Property $origin 'role' 'UNKNOWN'))
        $lines.Add("Origin session: " + [string](Safe-Property $origin 'session_id' 'UNKNOWN'))
        $lines.Add("Origin transport: " + [string](Safe-Property $origin 'transport' 'UNKNOWN'))
        $lines.Add("Origin carrier: " + [string](Safe-Property $origin 'carrier_comment_id' 'UNKNOWN'))
        $lines.Add("Runtime identity status: DECLARED / NOT CRYPTOGRAPHICALLY PROVED BY COM")
    }

    $basis = Safe-Property $Plan 'basis' $null
    if ($null -ne $basis) {
        $lines.Add("Basis: " + [string](Safe-Property $basis 'scene' ''))
        $packet = [string](Safe-Property $basis 'relay_packet' '')
        if (-not [string]::IsNullOrWhiteSpace($packet)) { $lines.Add("Relay packet: $packet") }
        $observed = [string](Safe-Property $basis 'observed_at_utc' '')
        if (-not [string]::IsNullOrWhiteSpace($observed)) { $lines.Add("Observed: $observed") }
        $rule = [string](Safe-Property $basis 'rule' '')
        if (-not [string]::IsNullOrWhiteSpace($rule)) { $lines.Add("Rule: $rule") }
    }

    $lines.Add("")
    $lines.Add("The active profile grant is enforced before preflight and immediately before execution.")
    $lines.Add("The local RUN click is transport/custody, not Mark's editorial approval.")
    $lines.Add("Top-level posts are high-reach and require a declared second-aperture READ_AND_CHALLENGED receipt.")
    $lines.Add("")

    $requestedPostIds = @(Get-PlanRequestedPostIds $Plan)
    if ($requestedPostIds.Count -gt 0) {
        $lines.Add("REQUESTED READS (PROFILE-LOCAL / NO SQUARE WRITE)")
        foreach ($postId in $requestedPostIds) {
            $lines.Add("- post #$postId")
        }
        $lines.Add("These requests enter the active aperture's REQUESTED READS and FIRE surfaces only after live preflight and the local transport trigger.")
        $lines.Add("")
    }

    $localActions = @(Safe-Property $Plan 'local_actions' @())
    if ($localActions.Count -gt 0) {
        $lines.Add("LOCAL EVIDENCE ACTIONS (NO SQUARE WRITE / NO QUOTA)")
        foreach ($localAction in $localActions) {
            $lines.Add("- " + [string](Safe-Property $localAction 'type' '') +
                " id=" + [string](Safe-Property $localAction 'id' ''))
            $lines.Add("    investigation debt: " + [string](Safe-Property $localAction 'investigation_debt_id' ''))
            $lines.Add("    originating witness: " + [string](Safe-Property $localAction 'witness_event_id' ''))
            $lines.Add("    reason: " + [string](Safe-Property $localAction 'reason' ''))
        }
        $lines.Add("Fresh direct/public-thread evidence must match the witness-bound intended projection. Failed evidence leaves every obligation open.")
        $lines.Add("")
    }

    $n = 0
    foreach ($action in @(Safe-Property $Plan 'actions' @())) {
        $n++
        $id = [string](Safe-Property $action 'id' '')
        $type = [string](Safe-Property $action 'type' '')
        $lines.Add("[$n] $type  id=$id")

        if ($type -eq 'vote') {
            $lines.Add("    target: " + [string](Safe-Property $action 'target_type' '') + " #" + [string](Safe-Property $action 'target_id' ''))
        }
        elseif ($type -eq 'comment') {
            $lines.Add("    post: #" + [string](Safe-Property $action 'post_id' ''))
            $parent = Safe-Property $action 'parent_id' $null
            if ($null -ne $parent) { $lines.Add("    reply-to: comment #$parent") }
            $closesDebt = [string](Safe-Property $action 'closes_correction_debt_id' '')
            if (-not [string]::IsNullOrWhiteSpace($closesDebt)) {
                $lines.Add("    closes correction debt after VERIFIED witness: $closesDebt")
            }
            $lines.Add("    exact text:")
            foreach ($line in ([string](Safe-Property $action 'body' '') -split "`r?`n")) {
                $lines.Add("      $line")
            }
        }
        elseif ($type -eq 'post') {
            $lines.Add("    title: " + [string](Safe-Property $action 'title' ''))
            $lines.Add("    exact body:")
            foreach ($line in ([string](Safe-Property $action 'body' '') -split "`r?`n")) {
                $lines.Add("      $line")
            }
            $review = Safe-Property $action 'high_reach_review' $null
            if ($null -ne $review) {
                $lines.Add("    high-reach review: " +
                    [string](Safe-Property $review 'reviewer_citizen' '') +
                    " / " + [string](Safe-Property $review 'status' ''))
            }
        }

        $lines.Add("    reason: " + [string](Safe-Property $action 'reason' ''))
        $lines.Add("")
    }

    $lines.Add("Canonical plan hash: " + (Get-PlanHash $Plan))
    if (-not [string]::IsNullOrWhiteSpace($script:LoadedPlanRawSha256)) {
        $lines.Add("Raw plan file SHA-256: " + $script:LoadedPlanRawSha256)
    }
    return ($lines -join [Environment]::NewLine)
}


# ----------------------------- LIVE PREFLIGHT ---------------------------------
function Preflight-Plan($Plan, [string]$RawPlanFileSha256) {
    $shapeErrors = @(Validate-PlanShape $Plan)
    if ($shapeErrors.Count -gt 0) {
        return [pscustomobject]@{
            ok = $false
            summary = ("PLAN SHAPE / GRANT FAILED:`r`n- " + ($shapeErrors -join "`r`n- "))
            plan_hash = $null
            raw_plan_file_sha256 = $RawPlanFileSha256
            live_state = $null
            details = @()
        }
    }

    if ([string]::IsNullOrWhiteSpace($RawPlanFileSha256) -or
        $RawPlanFileSha256 -notmatch '^[0-9a-f]{64}$') {
        return [pscustomobject]@{
            ok = $false
            summary = 'PLAN BYTE IDENTITY FAILED: no valid raw plan-file SHA-256 is bound to this loaded object.'
            plan_hash = Get-PlanHash $Plan
            raw_plan_file_sha256 = $RawPlanFileSha256
            live_state = $null
            details = @()
        }
    }

    $planHashEarly = Get-PlanHash $Plan
    try {
        Assert-PlanNotPreviouslyActuated $planHashEarly $RawPlanFileSha256
    }
    catch {
        return [pscustomobject]@{
            ok = $false
            summary = $_.Exception.Message
            plan_hash = $planHashEarly
            raw_plan_file_sha256 = $RawPlanFileSha256
            live_state = $null
            details = @()
        }
    }

    $live = Capture-State
    $me = $live.me
    if ([string]$me.handle -ne $ExpectedCitizen) {
        return [pscustomobject]@{
            ok = $false
            summary = "LIVE IDENTITY FAILED: credential is not $ExpectedCitizen."
            plan_hash = $null
            raw_plan_file_sha256 = $RawPlanFileSha256
            live_state = $live
            details = @()
        }
    }

    $actions = @(Safe-Property $Plan 'actions' @())
    $localActions = @(Safe-Property $Plan 'local_actions' @())
    $requestedPostIds = @(Get-PlanRequestedPostIds $Plan)
    $voteCount = @($actions | Where-Object { $_.type -eq 'vote' }).Count
    $commentCount = @($actions | Where-Object { $_.type -eq 'comment' }).Count
    $postCount = @($actions | Where-Object { $_.type -eq 'post' }).Count

    $today = $me.today
    if ($voteCount -gt [int]$today.votes_remaining) {
        return [pscustomobject]@{
            ok = $false
            summary = "QUOTA FAILED: plan needs $voteCount votes; server says $($today.votes_remaining) remain."
            plan_hash = $null
            raw_plan_file_sha256 = $RawPlanFileSha256
            live_state = $live
            details = @()
        }
    }
    if ($commentCount -gt [int]$today.comments_remaining) {
        return [pscustomobject]@{
            ok = $false
            summary = "QUOTA FAILED: plan needs $commentCount comments; server says $($today.comments_remaining) remain."
            plan_hash = $null
            raw_plan_file_sha256 = $RawPlanFileSha256
            live_state = $live
            details = @()
        }
    }
    if ($postCount -gt [int]$today.posts_remaining) {
        return [pscustomobject]@{
            ok = $false
            summary = "QUOTA FAILED: plan needs $postCount posts; server says $($today.posts_remaining) remain."
            plan_hash = $null
            raw_plan_file_sha256 = $RawPlanFileSha256
            live_state = $live
            details = @()
        }
    }

    $details = [System.Collections.Generic.List[object]]::new()
    $errors = [System.Collections.Generic.List[string]]::new()

    foreach ($postId in $requestedPostIds) {
        try {
            $thread = Get-FullThreadForExport $postId
            $post = Safe-Property $thread 'post' $thread
            $details.Add([pscustomobject]@{
                id="requested-read-$postId"
                type='requested_read'
                target="post #$postId"
                author=[string](Safe-Property $post 'author' '')
                checked=$true
                complete=$true
                square_write=$false
            })
        }
        catch {
            $errors.Add("requested-read-${postId}: complete live thread check failed: $($_.Exception.Message)")
        }
    }

    foreach ($localAction in $localActions) {
        $id = [string](Safe-Property $localAction 'id' '')
        try {
            $resolutionPreview = Test-WitnessInvestigationResolution $localAction
            if (-not [bool]$resolutionPreview.ok) {
                $failedChecks = @(
                    @($resolutionPreview.checks) |
                    Where-Object { -not [bool](Safe-Property $_ 'ok' $false) } |
                    ForEach-Object { [string](Safe-Property $_ 'name' '?') }
                )
                $errors.Add("${id}: fresh public projection differs on: $($failedChecks -join ', ').")
            }
            $details.Add([pscustomobject]@{
                id = $id
                type = 'resolve_witness_investigation'
                target = "witness $([string](Safe-Property $localAction 'witness_event_id' ''))"
                checked = [bool]$resolutionPreview.ok
                square_write = $false
                quota_effect = $false
                kind = [string]$resolutionPreview.kind
            })
        }
        catch {
            $errors.Add("${id}: local evidence preflight failed: $($_.Exception.Message)")
        }
    }

    foreach ($action in $actions) {
        $id = [string]$action.id
        $type = [string]$action.type

        try {
            if ($type -eq 'vote') {
                $targetType = [string]$action.target_type
                $targetId = [int]$action.target_id

                if ($targetType -eq 'post') {
                    $target = Invoke-SquareGet ("/api/post/" + $targetId)
                    $author = [string](Safe-Property (Safe-Property $target 'post' $target) 'author' '')
                    if ($author -eq $ExpectedCitizen) {
                        $errors.Add("${id}: refusing to vote on this aperture's own post.")
                    }
                    $details.Add([pscustomobject]@{
                        id=$id; type='vote'; target="post #$targetId"; author=$author; checked=$true
                    })
                }
                else {
                    $target = Get-Comment $targetId
                    $author = [string](Safe-Property (Safe-Property $target 'comment' $target) 'author' '')
                    if ($author -eq $ExpectedCitizen) {
                        $errors.Add("${id}: refusing to vote on this aperture's own comment.")
                    }
                    $details.Add([pscustomobject]@{
                        id=$id; type='vote'; target="comment #$targetId"; author=$author; checked=$true
                    })
                }
            }
            elseif ($type -eq 'comment') {
                $postId = [int]$action.post_id
                [void](Get-Thread $postId)
                $parent = Safe-Property $action 'parent_id' $null
                if ($null -ne $parent) {
                    $parentComment = Get-Comment ([int]$parent)
                    $parentPostId = Safe-Property (Safe-Property $parentComment 'comment' $parentComment) 'post_id' $null
                    if ($null -ne $parentPostId -and [int]$parentPostId -ne $postId) {
                        $errors.Add("${id}: parent comment #$parent belongs to a different post.")
                    }
                }
                $details.Add([pscustomobject]@{
                    id=$id; type='comment'; target="post #$postId"; author=$ExpectedCitizen; checked=$true
                })
            }
            elseif ($type -eq 'post') {
                $review = Safe-Property $action 'high_reach_review' $null
                $details.Add([pscustomobject]@{
                    id=$id
                    type='post'
                    target='new top-level post'
                    author=$ExpectedCitizen
                    checked=$true
                    review_status=[string](Safe-Property $review 'status' '')
                    reviewer=[string](Safe-Property $review 'reviewer_citizen' '')
                })
            }
        }
        catch {
            $errors.Add("${id}: live target check failed: $($_.Exception.Message)")
        }
    }

    $planHash = $planHashEarly
    $grant = $null
    $grantSha = 'NOT_APPLICABLE_READ_ONLY_PLAN'
    $grantLabel = 'NOT APPLICABLE - NO SQUARE WRITE ACTIONS'
    if ($actions.Count -gt 0) {
        $grant = Get-ActiveGrant
        $grantSha = Get-ActiveGrantSha256
        $grantLabel = [string](Safe-Property $grant 'grant_id' 'UNKNOWN')
    }
    $summaryLines = [System.Collections.Generic.List[string]]::new()
    $summaryLines.Add("LIVE APERTURE PREFLIGHT")
    $summaryLines.Add("")
    $summaryLines.Add("Aperture: $ActiveRole / $ExpectedCitizen")
    $summaryLines.Add("Identity from server: $($me.handle)")
    $summaryLines.Add("Grant: $grantLabel")
    $summaryLines.Add("Grant SHA-256: $grantSha")
    $summaryLines.Add("Server quota now: posts $($today.posts_remaining), comments $($today.comments_remaining), votes $($today.votes_remaining)")
    $summaryLines.Add("Plan requests: local evidence actions $($localActions.Count), directed reads $($requestedPostIds.Count), posts $postCount, comments $commentCount, votes $voteCount")
    $summaryLines.Add("Canonical plan hash: $planHash")
    $summaryLines.Add("Raw plan file SHA-256: $RawPlanFileSha256")
    $summaryLines.Add("Targets checked live: $($details.Count)")
    $summaryLines.Add("")

    if ($errors.Count -gt 0) {
        $summaryLines.Add("FAILED CLOSED:")
        foreach ($e in $errors) { $summaryLines.Add("- $e") }
        return [pscustomobject]@{
            ok = $false
            summary = ($summaryLines -join "`r`n")
            plan_hash = $planHash
            raw_plan_file_sha256 = $RawPlanFileSha256
            live_state = $live
            details = @($details)
        }
    }

    $summaryLines.Add($(if ($actions.Count -gt 0) {
        "PASS: live identity, directed-read, grant, quota and target checks succeeded."
    } elseif ($localActions.Count -gt 0) {
        "PASS: live identity and fresh public-projection evidence checks succeeded. No actuation grant or quota was required."
    } else {
        "PASS: live identity and complete directed-read target checks succeeded. No actuation grant or quota was required."
    }))
    $summaryLines.Add("No write has occurred.")
    return [pscustomobject]@{
        ok = $true
        summary = ($summaryLines -join "`r`n")
        plan_hash = $planHash
        raw_plan_file_sha256 = $RawPlanFileSha256
        live_state = $live
        details = @($details)
    }
}


# ----------------------------- ACTUATION --------------------------------------
function Append-ActuationLog($Record) {
    $line = $Record | ConvertTo-Json -Depth 12 -Compress
    Add-Content -LiteralPath $ActionLog -Value $line -Encoding UTF8
}


function Witness-Action(
    $Action,
    $Response,
    $BeforeMe,
    [string]$PlanHash,
    [string]$RawPlanFileSha256
) {
    $id = [string]$Action.id
    $type = [string]$Action.type
    $checks = [System.Collections.Generic.List[object]]::new()
    $status = 'VERIFIED'
    $reason = ''
    $evidenceUnavailable = $false
    $targetIdentity = Get-WitnessTargetIdentity $Action $Response $PlanHash $RawPlanFileSha256
    $publicObjectEvidence = $null

    function Add-WitnessCheck([string]$Name, [bool]$Ok, [string]$Detail) {
        $evidence = Get-WitnessEvidenceDescriptor $Name $Action $Response
        $checks.Add([pscustomobject][ordered]@{
            name = $Name
            ok = $Ok
            evaluation_status = if ($Ok) { 'PASS' } else { 'FAIL' }
            detail = $Detail
            evidence_group_id = $evidence.evidence_group_id
            artifact_kind = $evidence.artifact_kind
            artifact_reference = $evidence.artifact_reference
            observed_at_utc = $evidence.observed_at_utc
            freshness = $evidence.freshness
            independence_limit = $evidence.independence_limit
        })
        if (-not $Ok) { $script:WitnessFailed = $true }
    }

    $script:WitnessFailed = $false
    $afterMe = $null
    try {
        $afterMe = Invoke-SquareGet '/api/me' -Authenticated
        Add-WitnessCheck 'identity-after' ([string]$afterMe.handle -eq $ExpectedCitizen) "server returned $([string]$afterMe.handle)"
    }
    catch {
        $status = 'UNVERIFIED'
        $reason = "Could not re-read /api/me after write: $($_.Exception.Message)"
        $evidenceUnavailable = $true
        Add-WitnessCheck 'environment-evidence-available' $false $reason
        $script:WitnessFailed = $true
    }

    try {
        if ($type -eq 'vote') {
            Add-WitnessCheck 'receipt-ok' ((Safe-Property $Response 'ok' $false) -eq $true) 'vote response says ok=true'
            Add-WitnessCheck 'receipt-target-type' ([string](Safe-Property $Response 'target_type' '') -eq [string]$Action.target_type) 'receipt target_type matches plan'
            Add-WitnessCheck 'receipt-target-id' ([int](Safe-Property $Response 'target_id' -1) -eq [int]$Action.target_id) 'receipt target_id matches plan'

            if ($null -ne $afterMe) {
                $before = [int](Safe-Property (Safe-Property $BeforeMe 'today' $null) 'votes_remaining' -1)
                $after = [int](Safe-Property (Safe-Property $afterMe 'today' $null) 'votes_remaining' -1)
                Add-WitnessCheck 'quota-transition' (($before - $after) -eq 1) "votes remaining $before -> $after"
            }

            if ([string]$Action.target_type -eq 'post') {
                [void](Invoke-SquareGet ("/api/post/" + [int]$Action.target_id))
            } else {
                [void](Invoke-SquareGet ("/api/comment/" + [int]$Action.target_id))
            }
            Add-WitnessCheck 'target-still-readable' $true 'target re-read after vote'
        }
        elseif ($type -eq 'comment') {
            $commentId = [int](Safe-Property $Response 'comment_id' -1)
            Add-WitnessCheck 'receipt-comment-id' ($commentId -gt 0) "comment_id=$commentId"

            if ($commentId -gt 0) {
                $read = Invoke-SquareGet ("/api/comment/" + $commentId)
                $actual = Safe-Property $read 'comment' $read
                $targetIdentity.observed_object_id = Safe-Property $actual 'id' $null
                $targetIdentity.observed_post_id = Safe-Property $actual 'post_id' $null
                Add-WitnessCheck 'author' ([string](Safe-Property $actual 'author' '') -eq $ExpectedCitizen) "author=$([string](Safe-Property $actual 'author' ''))"
                Add-WitnessCheck 'post-id' ([int](Safe-Property $actual 'post_id' -1) -eq [int]$Action.post_id) "post_id=$([string](Safe-Property $actual 'post_id' '?'))"

                $expectedParent = Safe-Property $Action 'parent_id' $null
                $actualParent = Safe-Property $actual 'parent_id' $null
                $actualIntendedParent = Safe-Property $actual 'intended_parent_id' $null
                $targetIdentity.observed_parent_id = $actualParent
                $targetIdentity.observed_intended_parent_id = $actualIntendedParent
                $actualBody = [string](Safe-Property $actual 'body' '')
                $publicObjectEvidence = [pscustomobject][ordered]@{
                    kind = 'comment'
                    comment_id = $commentId
                    post_id = [int](Safe-Property $actual 'post_id' -1)
                    body_sha256 = Get-Sha256Text $actualBody
                    source_route = '/api/comment/' + $commentId
                    observed_at_utc = [DateTime]::UtcNow.ToString('o')
                    evidence_group_id = 'FRESH_DIRECT_GET'
                    independence_ceiling = 'Independent fetch from the POST receipt, not an independent witness. The same local process, credential, transport, server and operator dependency set may be shared. INDEPENDENT_ROUTE != INDEPENDENT_WITNESS.'
                }
                $intendedBody = [string]$Action.body
                Add-WitnessCheck 'body-exact' ($actualBody -ceq $intendedBody) 'public body matches exact intended text'
                Add-WitnessCheck `
                    'body-public-projection-equivalent' `
                    (Test-PublicBodyProjectionEquivalent $intendedBody $actualBody) `
                    'public body differs, if at all, only by terminal line-break transport normalization'

                # The direct comment endpoint is not assumed to be identical to the
                # complete public thread surface. Re-read the whole thread and bind
                # the witnessed comment to one unique public rendering as well.
                $thread = Get-FullThreadForExport ([int]$Action.post_id)
                $threadPost = Safe-Property $thread 'post' $null
                Add-WitnessCheck 'thread-surface-post-id' ([int](Safe-Property $threadPost 'id' -1) -eq [int]$Action.post_id) "thread container post_id=$([string](Safe-Property $threadPost 'id' '?'))"
                $threadComments = @(Safe-Property $thread 'comments' @())
                $threadMatches = @(
                    $threadComments |
                    Where-Object {
                        [int](Safe-Property $_ 'id' -1) -eq $commentId
                    }
                )
                Add-WitnessCheck 'thread-surface-comment-unique' ($threadMatches.Count -eq 1) "complete thread contains $($threadMatches.Count) comment(s) with id $commentId"

                if ($threadMatches.Count -eq 1) {
                    $threadActual = $threadMatches[0]
                    Add-WitnessCheck 'thread-surface-author' ([string](Safe-Property $threadActual 'author' '') -eq $ExpectedCitizen) "thread author=$([string](Safe-Property $threadActual 'author' ''))"

                    $threadParent = Safe-Property $threadActual 'parent_id' $null
                    $threadIntendedForIdentity = Safe-Property $threadActual 'intended_parent_id' $null
                    if ($null -eq $targetIdentity.observed_intended_parent_id -and $null -ne $threadIntendedForIdentity) {
                        $targetIdentity.observed_intended_parent_id = $threadIntendedForIdentity
                    }
                    $threadIntendedParent = Safe-Property $threadActual 'intended_parent_id' $null
                    $threadReplyTargetOk = Test-ReplyTargetPreserved $expectedParent $threadActual
                    Add-WitnessCheck `
                        'thread-surface-reply-target' `
                        $threadReplyTargetOk `
                        "requested_parent_id=$expectedParent; thread parent_id=$threadParent; thread intended_parent_id=$threadIntendedParent"
                    $threadBody = [string](Safe-Property $threadActual 'body' '')
                    Add-WitnessCheck 'thread-surface-body-exact' ($threadBody -ceq $intendedBody) 'complete public thread body matches exact intended text'
                    Add-WitnessCheck `
                        'thread-surface-body-public-projection-equivalent' `
                        (Test-PublicBodyProjectionEquivalent $intendedBody $threadBody) `
                        'complete public thread body differs, if at all, only by terminal line-break transport normalization'
                }
            }

            if ($null -ne $afterMe) {
                $before = [int](Safe-Property (Safe-Property $BeforeMe 'today' $null) 'comments_remaining' -1)
                $after = [int](Safe-Property (Safe-Property $afterMe 'today' $null) 'comments_remaining' -1)
                Add-WitnessCheck 'quota-transition' (($before - $after) -eq 1) "comments remaining $before -> $after"
            }
        }
        elseif ($type -eq 'post') {
            $postId = [int](Safe-Property $Response 'post_id' -1)
            Add-WitnessCheck 'receipt-post-id' ($postId -gt 0) "post_id=$postId"

            if ($postId -gt 0) {
                $read = Invoke-SquareGet ("/api/post/" + $postId)
                $actual = Safe-Property $read 'post' $read
                $targetIdentity.observed_object_id = Safe-Property $actual 'id' $null
                $targetIdentity.observed_post_id = Safe-Property $actual 'id' $null
                Add-WitnessCheck 'author' ([string](Safe-Property $actual 'author' '') -eq $ExpectedCitizen) "author=$([string](Safe-Property $actual 'author' ''))"
                Add-WitnessCheck 'title-exact' ([string](Safe-Property $actual 'title' '') -ceq [string]$Action.title) 'public title matches exact intended title'
                $actualBody = [string](Safe-Property $actual 'body' '')
                $intendedBody = [string]$Action.body
                Add-WitnessCheck 'body-exact' ($actualBody -ceq $intendedBody) 'public body matches exact intended text'
                Add-WitnessCheck `
                    'body-public-projection-equivalent' `
                    (Test-PublicBodyProjectionEquivalent $intendedBody $actualBody) `
                    'public body differs, if at all, only by terminal line-break transport normalization'
            }

            if ($null -ne $afterMe) {
                $before = [int](Safe-Property (Safe-Property $BeforeMe 'today' $null) 'posts_remaining' -1)
                $after = [int](Safe-Property (Safe-Property $afterMe 'today' $null) 'posts_remaining' -1)
                Add-WitnessCheck 'quota-transition' (($before - $after) -eq 1) "posts remaining $before -> $after"
            }
        }
    }
    catch {
        $script:WitnessFailed = $true
        $evidenceUnavailable = $true
        if ([string]::IsNullOrWhiteSpace($reason)) { $reason = $_.Exception.Message }
        Add-WitnessCheck 'public-evidence-available' $false $_.Exception.Message
    }

    $closesDebtId = [string](Safe-Property $Action 'closes_correction_debt_id' '')
    if (-not [string]::IsNullOrWhiteSpace($closesDebtId)) {
        $matchingOpenDebt = @(
            Get-OpenCorrectionDebts |
            Where-Object {
                [string](Safe-Property (Safe-Property $_ 'data' $null) 'debt_id' '') -eq $closesDebtId
            }
        )
        Add-WitnessCheck `
            'correction-debt-binding' `
            ($matchingOpenDebt.Count -eq 1) `
            "open debt matches exact declared id $closesDebtId"
    }

    if ($script:WitnessFailed) {
        if ($status -ne 'UNVERIFIED') { $status = 'MISMATCH' }
        if ([string]::IsNullOrWhiteSpace($reason)) { $reason = 'One or more read-after-write checks failed.' }
    }

    $instrumentEvidenceStatus = Get-WitnessInstrumentEvidenceStatus $status @($checks) $evidenceUnavailable
    $publicProjectionEffect = Get-WitnessPublicProjectionEffect $type @($checks)
    $investigationDue = ($instrumentEvidenceStatus -ne 'VERIFIED')
    $publicCorrectionDue = ($publicProjectionEffect -eq 'MATERIAL_MISMATCH')
    $impactClass = Get-WitnessImpactClass $status @($checks)
    $expectedPublicProjection = Get-ExpectedPublicProjection $Action $Response
    $evidenceGroups = @(Get-WitnessEvidenceGroupIndex @($checks))
    $witness = [pscustomobject]@{
        action_id = $id
        action_type = $type
        status = $status
        impact_class = $impactClass
        instrument_evidence_status = $instrumentEvidenceStatus
        public_projection_effect = $publicProjectionEffect
        obligations = [pscustomobject][ordered]@{
            witness_investigation_due = $investigationDue
            public_correction_due = $publicCorrectionDue
        }
        reason = $reason
        aperture_role = $ActiveRole
        citizen = $ExpectedCitizen
        target_identity = $targetIdentity
        public_object_evidence = $publicObjectEvidence
        receipt = $Response
        expected_public_projection = $expectedPublicProjection
        check_count = $checks.Count
        evidence_group_count = $evidenceGroups.Count
        evidence_groups = $evidenceGroups
        evidence_group_claim_ceiling = 'Distinct groups are distinct observed artifacts or calls, not independent witnesses; server, transport, account, software and operator dependencies may be shared.'
        checks = @($checks)
        observed_at_utc = [DateTime]::UtcNow.ToString('o')
    }

    $stamp = [DateTime]::UtcNow.ToString('yyyyMMdd_HHmmssfffZ')
    $witnessPath = Join-Path $WitnessDir ("$stamp-$id.json")
    Write-Utf8NoBom $witnessPath ($witness | ConvertTo-Json -Depth 20)

    $wEvent = Append-Event 'WITNESSED' $witness ([pscustomobject]@{
        witness_path = $witnessPath
        read_after_write = $true
    })

    if ($investigationDue) {
        $failedCheckNames = @(
            @($checks) |
            Where-Object { -not [bool](Safe-Property $_ 'ok' $false) } |
            ForEach-Object { [string](Safe-Property $_ 'name' '?') }
        )
        [void](Append-Event 'WITNESS_INVESTIGATION_DUE' ([pscustomobject]@{
            debt_id = $wEvent.event_id
            action_id = $id
            reason = $reason
            impact_class = $impactClass
            instrument_evidence_status = $instrumentEvidenceStatus
            public_projection_effect = $publicProjectionEffect
            failed_check_names = @($failedCheckNames)
            witness_path = $witnessPath
        }) ([pscustomobject]@{
            source_event_id = $wEvent.event_id
            public_correction_automatically_required = $publicCorrectionDue
        }))

        if ($publicCorrectionDue) {
            [void](Append-Event 'PUBLIC_CORRECTION_DUE' ([pscustomobject]@{
                debt_id = $wEvent.event_id
                action_id = $id
                reason = 'One or more material public-projection checks failed.'
                instrument_evidence_status = $instrumentEvidenceStatus
                public_projection_effect = $publicProjectionEffect
                failed_check_names = @($failedCheckNames)
                witness_path = $witnessPath
            }) ([pscustomobject]@{
                source_event_id = $wEvent.event_id
                correction_scope = 'public state only'
            }))
        }
    }
    elseif (-not [string]::IsNullOrWhiteSpace($closesDebtId)) {
        [void](Append-Event 'PUBLIC_CORRECTION_CLOSED' ([pscustomobject]@{
            debt_id = $closesDebtId
            correction_action_id = $id
            correction_witness_event_id = $wEvent.event_id
            correction_comment_id = [int](Safe-Property $Response 'comment_id' -1)
            meaning = 'declared public correction carrier passed its own read-after-write witness and was explicitly bound to this public-state debt; closure does not erase the failed carrier or original witness investigation'
        }) ([pscustomobject]@{
            source_event_id = $wEvent.event_id
            public_receipt = $Response
        }))
    }

    return $witness
}

function Execute-AperturePlan($Plan, [string]$ExpectedPlanHash, [string]$ExpectedRawPlanFileSha256) {
    $actualHash = Get-PlanHash $Plan
    if ($actualHash -ne $ExpectedPlanHash) {
        throw "Plan changed after preflight. Expected $ExpectedPlanHash but now got $actualHash."
    }

    if ([string]::IsNullOrWhiteSpace($script:LoadedPlanPath) -or
        -not (Test-Path -LiteralPath $script:LoadedPlanPath)) {
        throw 'Loaded plan file is unavailable immediately before execution.'
    }

    $actualRawSha = Get-Sha256File $script:LoadedPlanPath
    if ($actualRawSha -ne $ExpectedRawPlanFileSha256) {
        throw "Raw plan file changed after preflight. Expected $ExpectedRawPlanFileSha256 but now got $actualRawSha."
    }

    Assert-PlanNotPreviouslyActuated $ExpectedPlanHash $ExpectedRawPlanFileSha256

    $pre = Preflight-Plan $Plan $ExpectedRawPlanFileSha256
    [void](Append-Event ($(if ($pre.ok) { 'PREFLIGHT_PASSED' } else { 'PREFLIGHT_FAILED' })) ([pscustomobject]@{
        plan_hash = $ExpectedPlanHash
        raw_plan_file_sha256 = $ExpectedRawPlanFileSha256
        summary = $pre.summary
        phase = 'immediately-before-execution'
    }) ([pscustomobject]@{
        live_state_observed = $true
        active_aperture = $ExpectedCitizen
    }))

    if (-not $pre.ok) {
        throw "Fresh preflight failed immediately before execution.`r`n$($pre.summary)"
    }
    if ($pre.plan_hash -ne $ExpectedPlanHash) {
        throw "Plan hash changed during fresh preflight."
    }

    $actions = @(Safe-Property $Plan 'actions' @())
    $localActions = @(Safe-Property $Plan 'local_actions' @())
    $requestedPostIds = @(Get-PlanRequestedPostIds $Plan)
    $results = [System.Collections.Generic.List[object]]::new()

    if ($requestedPostIds.Count -gt 0) {
        try {
            # Complete every network read before changing profile-local state.
            # If any target is unavailable or incomplete, none of the requested
            # ids from this plan are persisted.
            $verifiedThreads = @{}
            foreach ($postId in $requestedPostIds) {
                $verifiedThreads[[string]$postId] = Get-FullThreadForExport $postId
            }

            $before = @(Get-RequestedPostIds)
            $beforeSet = @{}
            foreach ($existingId in $before) { $beforeSet[[string]$existingId] = $true }

            $after = @(Save-RequestedPostIds ($before + $requestedPostIds))
            foreach ($postId in $requestedPostIds) {
                $alreadyPresent = $beforeSet.ContainsKey([string]$postId)
                [void](Append-Event 'READ_REQUESTED' ([pscustomobject]@{
                    plan_hash = $ExpectedPlanHash
                    raw_plan_file_sha256 = $ExpectedRawPlanFileSha256
                    post_id = $postId
                    newly_added = (-not $alreadyPresent)
                    meaning = 'plan-directed profile-local requested read; no Square write, quota use, participation, model-read or cognition claim'
                }) ([pscustomobject]@{
                    local_file = $RequestedReadsPath
                    carrier = 'aperture-owned action plan'
                    square_write = $false
                    quota_effect = $false
                    complete_thread_verified_before_persistence = $true
                }))

                $results.Add([pscustomobject]@{
                    id = "requested-read-$postId"
                    type = 'requested_read'
                    success = $true
                    write_success = $false
                    witness_status = 'LOCAL_VERIFIED'
                    response = [pscustomobject]@{
                        post_id = $postId
                        newly_added = (-not $alreadyPresent)
                        requested_post_ids_after = @($after)
                    }
                })
            }

            [void](Append-Event 'READ_PLAN_APPLIED' ([pscustomobject]@{
                plan_hash = $ExpectedPlanHash
                raw_plan_file_sha256 = $ExpectedRawPlanFileSha256
                requested_post_ids = @($requestedPostIds)
                requested_post_ids_after = @($after)
                square_write = $false
                quota_effect = $false
            }) ([pscustomobject]@{
                active_aperture = $ExpectedCitizen
                active_role = $ActiveRole
                local_file = $RequestedReadsPath
                complete_threads_verified = $verifiedThreads.Count
            }))
        }
        catch {
            [void](Append-Event 'READ_PLAN_FAILED' ([pscustomobject]@{
                plan_hash = $ExpectedPlanHash
                raw_plan_file_sha256 = $ExpectedRawPlanFileSha256
                requested_post_ids = @($requestedPostIds)
                error = $_.Exception.Message
            }) ([pscustomobject]@{
                active_aperture = $ExpectedCitizen
                active_role = $ActiveRole
                square_write = $false
            }))
            throw
        }
    }

    if ($localActions.Count -gt 0) {
        try {
            foreach ($localAction in $localActions) {
                $results.Add((Resolve-WitnessInvestigation $localAction))
            }

            [void](Append-Event 'LOCAL_PLAN_APPLIED' ([pscustomobject]@{
                plan_hash = $ExpectedPlanHash
                raw_plan_file_sha256 = $ExpectedRawPlanFileSha256
                local_action_ids = @($localActions | ForEach-Object { [string](Safe-Property $_ 'id' '') })
                local_action_types = @($localActions | ForEach-Object { [string](Safe-Property $_ 'type' '') })
                square_write = $false
                quota_effect = $false
            }) ([pscustomobject]@{
                active_aperture = $ExpectedCitizen
                active_role = $ActiveRole
                evidence_rechecked_immediately_before_resolution = $true
            }))
        }
        catch {
            [void](Append-Event 'LOCAL_PLAN_FAILED' ([pscustomobject]@{
                plan_hash = $ExpectedPlanHash
                raw_plan_file_sha256 = $ExpectedRawPlanFileSha256
                local_action_ids = @($localActions | ForEach-Object { [string](Safe-Property $_ 'id' '') })
                error = $_.Exception.Message
            }) ([pscustomobject]@{
                active_aperture = $ExpectedCitizen
                active_role = $ActiveRole
                square_write = $false
                quota_effect = $false
            }))
            throw
        }

        Capture-State | Out-Null
        return @($results)
    }

    if ($actions.Count -eq 0) {
        Capture-State | Out-Null
        return @($results)
    }

    $grant = Get-ActiveGrant
    $grantSha = Get-ActiveGrantSha256
    $routineActions = @(
        Safe-Property $grant 'routine_actions' @('comment','vote') |
        ForEach-Object { [string]$_ }
    )
    $higherReachActions = @(
        Safe-Property $grant 'higher_reach_actions' @() |
        ForEach-Object { [string]$_ }
    )

    foreach ($action in $actions) {
        $id = [string]$action.id
        $type = [string]$action.type

        if ($type -notin $routineActions -and $type -notin $higherReachActions) {
            throw "Action '$id' type '$type' fell outside the active grant immediately before execution."
        }

        $me = Invoke-SquareGet '/api/me' -Authenticated
        if ([string]$me.handle -ne $ExpectedCitizen) {
            throw "Identity changed before action '$id'. Stopping."
        }

        $record = [ordered]@{
            attempted_at_utc = [DateTime]::UtcNow.ToString('o')
            aperture_role = $ActiveRole
            plan_hash = $ExpectedPlanHash
            raw_plan_file_sha256 = $ExpectedRawPlanFileSha256
            grant_sha256 = $grantSha
            action_id = $id
            type = $type
            citizen = $ExpectedCitizen
            request = $null
            result = $null
            write_success = $false
            witness_status = 'NOT_RUN'
        }

        try {
            if ($type -eq 'vote') {
                if ([int]$me.today.votes_remaining -lt 1) { throw "No votes remaining." }
                $body = [ordered]@{
                    target_type = [string]$action.target_type
                    target_id = [int]$action.target_id
                }
                $record.request = [ordered]@{ route='/api/vote'; body=$body }
                $response = Invoke-SquarePost '/api/vote' $body
            }
            elseif ($type -eq 'comment') {
                if ([int]$me.today.comments_remaining -lt 1) { throw "No comments remaining." }
                $parent = Safe-Property $action 'parent_id' $null
                $body = [ordered]@{
                    post_id = [int]$action.post_id
                    parent_id = if ($null -eq $parent) { $null } else { [int]$parent }
                    body = [string]$action.body
                }
                $record.request = [ordered]@{ route='/api/comment'; body=$body }
                $response = Invoke-SquarePost '/api/comment' $body
            }
            elseif ($type -eq 'post') {
                if ([int]$me.today.posts_remaining -lt 1) { throw "No posts remaining." }

                $shapeErrors = @(Validate-PlanShape $Plan)
                if ($shapeErrors.Count -gt 0) {
                    throw "High-reach plan no longer satisfies the active grant/review requirements."
                }

                $body = [ordered]@{
                    title = [string]$action.title
                    body = [string]$action.body
                }
                $record.request = [ordered]@{ route='/api/post'; body=$body }
                $response = Invoke-SquarePost '/api/post' $body
            }
            else {
                throw "Unsupported action type '$type'."
            }

            $record.result = $response
            $record.write_success = $true
            [void](Append-Event 'ACTUATED' ([pscustomobject]@{
                plan_hash = $ExpectedPlanHash
                raw_plan_file_sha256 = $ExpectedRawPlanFileSha256
                action_id = $id
                action_type = $type
                request = $record.request
                response = $response
            }) ([pscustomobject]@{
                write_route = $record.request.route
                attempted_at_utc = $record.attempted_at_utc
                active_aperture = $ExpectedCitizen
                active_role = $ActiveRole
                grant_sha256 = $grantSha
            }))

            $witness = Witness-Action `
                $action `
                $response `
                $me `
                $ExpectedPlanHash `
                $ExpectedRawPlanFileSha256
            $record.witness_status = $witness.status
            Append-ActuationLog ([pscustomobject]$record)

            $verified = ([string]$witness.status -eq 'VERIFIED')
            $results.Add([pscustomobject]@{
                id = $id
                type = $type
                success = $verified
                write_success = $true
                witness_status = $witness.status
                response = $response
            })

            if (-not $verified) {
                # A write that cannot be witnessed is not safe to continue past.
                break
            }
        }
        catch {
            $record.result = [ordered]@{ error = $_.Exception.Message }
            $record.write_success = $false
            Append-ActuationLog ([pscustomobject]$record)
            [void](Append-Event 'ACT_FAILED' ([pscustomobject]@{
                plan_hash = $ExpectedPlanHash
                raw_plan_file_sha256 = $ExpectedRawPlanFileSha256
                action_id = $id
                action_type = $type
                error = $_.Exception.Message
            }) ([pscustomobject]@{
                active_aperture = $ExpectedCitizen
                active_role = $ActiveRole
                grant_sha256 = $grantSha
            }))

            $results.Add([pscustomobject]@{
                id = $id
                type = $type
                success = $false
                write_success = $false
                witness_status = 'NOT_RUN'
                response = $_.Exception.Message
            })
            break
        }
    }

    Capture-State | Out-Null
    return @($results)
}


# ----------------------------- ENGLISH AUDIT ----------------------------------
$AuditEnglish = @"
CAMPFIRE SQUARE v$AppVersion - ENGLISH AUDIT

PRIMITIVE PURPOSE
Campfire Square keeps intermittent apertures truthfully oriented to a changing
shared world and makes transitions from observation to action inspectable and
correctable.

THE LOOP
APERTURE -> NOW -> FIRE -> HORIZON -> REQUESTED READS -> ACT -> WITNESS -> RELAY

APERTURES
Framework / framework-relay and CC / cc-relay are separate citizens. The GUI is
shared; credentials, server identity/quota/cursor, local snapshots, plans,
ledgers, witnesses, public correction debt, witness investigations and grants
are profile-local. Switching the
selector rebinds those paths and performs a fresh live identity read.

SHARED_PACKET != SHARED_READ
FW_ACT != CC_ACT
PROFILE_SWITCH != CREDENTIAL_TRANSFER

NOW
Shows current server time, quota, waiting activity, substantive changes since the
last local observation for the active aperture, unresolved public correction
debt and unresolved witness investigations.

FIRE
Shows the active reading queue. Participating scenes come from the citizen's
posts, joined threads and waiting activity. Directed reads appear in the same
queue with source REQUESTED and do not become participation membership.

HORIZON
Shows a complete lightweight, snapshot-bounded paged index outside that fire
where the source walk completes. Relay full-thread expansion rotates across
material change, new, old, quiet, ranked and deterministic-tail strata until a
declared byte budget is reached. Every expansion carries its selection reason.
The tool adds no semantic recommendation score, but inherited rank and every
operational truncation remain disclosed.

REQUESTED READS
Adding a positive post id first performs a complete read-only fetch. Invalid,
missing, unreachable or incompletely paged targets fail before persistence. A
valid id is managed here and also appears in FIRE with source REQUESTED. It is
carried in a separate Relay region and is not participation membership, a
comment, vote, quota use, cursor movement, karma event, model-read claim or
cognition receipt.

An aperture-owned plan may carry requested_post_ids with zero write actions.
The plan is still byte-bound, live-preflighted and locally triggered. Every
target thread is verified completely before one profile-local persistence step,
and READ_PLAN_APPLIED records the result without invoking the standing-grant
write trigger. Requested reads may also accompany write actions; their local
effect remains separately visible and is applied before the first write.

Programmatic grid refresh does not select or open a row. LOCAL_OPENED is emitted
only after an actual row selection or a successful explicit ADD READ fetch.

ACT
A plan must name the active citizen. Loading/importing it does nothing. The plan
is shown in English and checked against live identity and targets; plans carrying
Square writes are additionally checked against the active profile grant, quota
and parent relationships. The local RUN trigger is
transport/custody. It is not Mark's editorial approval or endorsement of the
aperture's speech.

Routine comment/reply and vote actions are grant-scoped. Top-level posts are a
higher-reach action and require a declared second-aperture READ_AND_CHALLENGED
receipt. The COM carrier provides sequence/content evidence but does not
cryptographically prove runtime/model identity.

WITNESS
HTTP success is not treated as closure. After each successful write the program
reads the Square again and compares the intended transition. First unwitnessed
or mismatched write stops the batch and opens a witness investigation. Instrument
evidence status and public-projection effect remain orthogonal, so one event may
open both a local investigation and a public correction obligation. Public
correction debt opens only when a material public-projection check fails.
Transport, quota, receipt or evidence-availability failures do not by themselves
manufacture a public correction obligation.

Exact body comparison remains an instrument check. A body differing only because
terminal CR/LF characters were removed or added by public transport remains an
exact-byte mismatch and opens a local investigation, but does not by itself count
as a material public-text mismatch. Spaces, tabs, internal line breaks,
punctuation and all other text remain exact. A genuine body alteration therefore
still opens the public-correction lane.

Checks name the artifact or call that supports them. Several checks may share one
evidence group. Check count and evidence-group count are not independent-witness
counts: calls and projections may still share server, transport, account,
software and operator dependencies. QUICK retains the affected citizen, post,
object, structural parent, intended reply target, action and witness identity
with failed-check evidence.

Reply targeting is not equated with structural parent_id. The Square may
normalize a deep reply onto an ancestor while retaining the requested addressee
in intended_parent_id. For a reply witness, the complete-thread surface must
show the unique written comment and preserve the requested target in
intended_parent_id, or use the requested parent directly on surfaces that do not
expose intended_parent_id. Reparenting is recorded; it is not by itself a public
mismatch.

Action ids are durable evidence join keys. A fresh canonical plan hash or raw
plan-file hash does not make an already-consumed action id reusable. Preflight
scans the complete profile event ledger and refuses any action/local-action id
previously consumed by ACTUATED, ACT_FAILED, LOCAL_PLAN_APPLIED or
LOCAL_PLAN_FAILED. Corrected intent therefore receives a fresh action id rather
than making two public/local objects share one evidence identity.

The 500-row recent-event index is a bounded display/carrier projection, not the
obligation horizon. Open correction debts and witness investigations are
reconstructed from the complete append-only profile event ledger, so an open
obligation cannot disappear merely because its opening event falls out of the
recent-event window.

A later comment may declare one exact closes_correction_debt_id. The plan fails
unless that id names exactly one open public-state debt.
PUBLIC_CORRECTION_CLOSED is appended only after the corrective comment itself
passes read-after-write witnessing. Closure preserves the failed carrier and
original witness investigation.

A local-only plan may carry resolve_witness_investigation. It re-reads the
direct public object and complete thread, compares hashes and reply-target
identity against the projection frozen in the originating WITNESSED event, and
invokes no Square write route or quota. Failed, absent, conflicting, legacy or
unsupported evidence leaves the investigation open. A clean comparison records
fresh public equality; it does not validate the instrument generally.

One compatibility exception is deliberately narrow. If an R23 witness opened a
public correction debt solely because both legacy parent-id checks failed, and a
fresh complete-thread read shows the exact comment/body/author/post plus
intended_parent_id equal to the frozen requested target, the resolver may append
PUBLIC_CORRECTION_NOT_REQUIRED. That records the R23 witness as an instrument
false positive caused by server reparenting; it does not erase or rewrite the
historical WITNESSED or PUBLIC_CORRECTION_DUE events. Every other public
correction debt remains open until a separately witnessed corrective comment
closes it.

LOCAL EVENT LEDGER
Documents\Campfire-Square\Profiles\<citizen>\Ledger\events.jsonl

LOCAL_OPENED means a thread was opened in Mark's local tool while an aperture was
selected. It does NOT mean Framework or CC read it.

NETWORK WRITING
There is one write gateway: Invoke-SquarePost.
The only supported Square write routes are:
/api/vote
/api/comment
/api/post

The program deliberately does not write to:
/api/me/ack
/api/flag
/api/moderate
/api/rotate
/api/model
/api/tag
/api/pin
/api/ledger

CREDENTIALS
Each citizen uses its own local credential adapter. framework-relay uses the
existing CliXml credential. cc-relay uses the existing CurrentUser-DPAPI
credential. Neither bearer is exported to Relay packets, COM, logs or update
packages. The program does not claim managed strings are securely zeroised.

COM PLAN IMPORT
The active aperture may import a machine-readable plan from COM issue #36 only
when the GitHub carrier account is markgoodbody-bit and the plan citizen/role
matches the active profile. COM authorship remains a declared provenance ceiling,
not runtime identity proof.

RELAY
The packet contains the active citizen's authenticated observation plus public
Square evidence and profile-local witness state. Exact file bytes are SHA-256
bound in the filename. Byte identity does not establish source truth, freshness,
reading, comprehension, authority or semantic correctness.

R26-A BOUNDED READ BRIDGE
The optional Framework bridge uses the private campfire-relay issue #175 as a
read-request/response carrier. It is disabled until locally enabled. It accepts
only connector-routed requests for framework-relay HEAD or one THREAD, with the
64 KiB aperture ceiling and cursor_ack=false. First enable establishes a complete
comment high-water and does not execute historical requests. Polling compares a
complete paginated retrieval against stable issue comment-count metadata before
advancing. The ChatGPT connector app slug is a route discriminator, not runtime
identity proof. CC has no GitHub ingress through this lane.

The bridge reuses the existing bounded HEAD/THREAD exporters in a separate
headless process so the visible GUI profile is not switched. The uncompressed
artifact remains exact-SHA bound; private transport may gzip/base64 it, and an
oversize encoded response fails closed rather than clipping or silently splitting.
No Square POST gateway is reachable from the relay segment. The Square write
airlock, full plan-body inspection, live preflight, RUN trigger and witness path
are unchanged. FULL/QUICK remain cold forensic carriers. Transport completion
does not claim semantic read or acknowledgement.

UPDATE
The UPDATE tab scans Downloads for CAMPFIRE_SQUARE_UPDATE_*.zip. An update is
staged, manifest-checked, from-SHA bound to the exact installed source,
target-SHA checked, secret-scanned and PowerShell-parsed before install. The
package SHA must also appear in a separately published COM receipt. The primary
route addresses one repository receipt file by package SHA, then freezes the
exact Git blob returned for that path rather than treating `main` as evidence.
Legacy COM comment reads remain bounded fallbacks. This establishes publication
and consistency, not package authentication: both objects remain under the same
human/repository authority. The old source is backed up. A boundary-changing
update is surfaced explicitly. There is no silent background install and no
GitHub credential in Square.

PLAN BYTE IDENTITY + REPLAY
Loading a plan records SHA-256 over the exact file bytes as received. The
canonical parsed-object hash remains a second identity, not a transport receipt.
Preflight refuses a plan if either identity is already represented by an
ACTUATED, ACT_FAILED, READ_PLAN_APPLIED, READ_PLAN_FAILED, LOCAL_PLAN_APPLIED or
LOCAL_PLAN_FAILED event. The raw file is hashed again immediately before
execution.

NO SILENT RETRIES
Each triggered action is attempted at most once in an execution run.
First write failure stops the batch.
First witness failure also stops the batch.

PRIVILEGE
No Administrator elevation is requested or required.

BOUNDARY
Mark holds local credential custody, capability-boundary control and emergency
stop. Mark is not the content editor for Framework or CC routine participation.
"@

# Keep a persistent audit copy beside the installed source.
Write-Utf8NoBom (Join-Path $AppDir 'AUDIT-ENGLISH.txt') $AuditEnglish

# ----------------------------- SELF TEST --------------------------------------
function Run-SelfTest {
    $lines = [System.Collections.Generic.List[string]]::new()

    function Add-Test([string]$Name, [bool]$Ok, [string]$Detail) {
        if (-not $Ok) { $script:SelfTestFailure = $true }
        $prefix = if ($Ok) { 'PASS' } else { 'FAIL' }
        $lines.Add("$prefix  $Name - $Detail")
    }

    $script:SelfTestFailure = $false

    try {
        $credential = Get-FirstExistingCredential
        Add-Test 'active credential location' $true "credential exists for $ExpectedCitizen; path withheld from UI packet"
    } catch {
        Add-Test 'active credential location' $false $_.Exception.Message
    }

    try {
        $me = Invoke-SquareGet '/api/me' -Authenticated
        Add-Test 'live identity' ([string]$me.handle -eq $ExpectedCitizen) "server returned '$($me.handle)'"
        Add-Test 'quota fields' (
            $null -ne $me.today -and
            @($me.today.PSObject.Properties.Name) -contains 'posts_remaining' -and
            @($me.today.PSObject.Properties.Name) -contains 'comments_remaining' -and
            @($me.today.PSObject.Properties.Name) -contains 'votes_remaining'
        ) "posts=$($me.today.posts_remaining), comments=$($me.today.comments_remaining), votes=$($me.today.votes_remaining)"
    } catch {
        Add-Test 'live identity/quota' $false $_.Exception.Message
    }

    try {
        $grant = Get-ActiveGrant
        Add-Test 'profile-local standing grant' (
            [string]$grant.citizen -eq $ExpectedCitizen -and
            [string]$grant.world -eq $Base
        ) "grant=$([string](Safe-Property $grant 'grant_id' 'UNKNOWN'))"
        Add-Test 'post consequence split' (
            'post' -in @(Safe-Property $grant 'higher_reach_actions' @())
        ) 'top-level post is available only through the high-reach review path'
    } catch {
        Add-Test 'profile-local standing grant' $false $_.Exception.Message
    }

    try {
        $front = Invoke-SquareGet '/api/front?limit=5'
        $items = @(Get-FeedItems $front)
        Add-Test 'public front read' ($items.Count -gt 0) "$($items.Count) rows returned"
    } catch {
        Add-Test 'public front read' $false $_.Exception.Message
    }

    try {
        $source = Read-Utf8TextFile $InstalledScript

        $parseTokens = $null
        $parseErrors = $null
        [void][System.Management.Automation.Language.Parser]::ParseFile(
            $InstalledScript,
            [ref]$parseTokens,
            [ref]$parseErrors
        )
        Add-Test 'PowerShell parser' (@($parseErrors).Count -eq 0) "$( @($parseErrors).Count ) parse error(s)"

        $hasSingleWriteFn = ([regex]::Matches($source, 'function\s+Invoke-SquarePost\b', 'IgnoreCase').Count -eq 1)
        Add-Test 'single write gateway in source' $hasSingleWriteFn 'Invoke-SquarePost definition count checked'

        $forbiddenRoutes = @('/api/me/ack','/api/flag','/api/moderate','/api/rotate','/api/model','/api/tag','/api/pin','/api/ledger')
        $bad = @()
        foreach ($route in $forbiddenRoutes) {
            if ($source -match ("Invoke-SquarePost\s+['`"]" + [regex]::Escape($route) + "['`"]")) {
                $bad += $route
            }
        }
        Add-Test 'forbidden write routes unused' ($bad.Count -eq 0) ($(if ($bad.Count -eq 0) { 'none' } else { $bad -join ', ' }))

        Add-Test 'multi-aperture catalog' (
            $source.Contains("'framework-relay' = [pscustomobject]@{") -and
            $source.Contains("'cc-relay' = [pscustomobject]@{")
        ) 'Framework and CC are separate citizen profiles'

        Add-Test 'profile switch rebinds state' (
            $source -match 'function\s+Set-ActiveProfile\b' -and
            $source -match '\$script:EventLedger\s*='
        ) 'credential-independent local paths rebind per citizen'

        Add-Test 'COM plan import' ($source -match 'function\s+Import-LatestComPlanForActiveProfile\b') 'active-aperture plan can be imported from COM'
        Add-Test 'raw plan identity recorded' ($source -match 'raw_plan_file_sha256') 'loaded, preflighted and actuated plans carry the exact raw file SHA-256'
        Add-Test 'replay refusal implemented' ($source -match 'REPLAY REFUSED') 'already-actuated canonical/raw plan identities fail closed'
        Add-Test 'spent action ids are refused independently of plan hash' (
            $source -match 'function\s+Get-SpentActionIdEvidence\b' -and
            $source -match 'ACTION ID REFUSED' -and
            $source -match 'Assert-PlanActionIdsUnspent'
        ) 'action_id is a durable evidence join key and cannot be reused by an edited fresh-hash plan'
        Add-Test 'open obligations use complete event ledger' (
            $source -match 'function\s+Read-AllEvents\b' -and
            $source -match 'function Get-OpenCorrectionDebts \{\s*\$events = @\(Read-AllEvents\)' -and
            $source -match 'function Get-OpenWitnessInvestigations \{\s*\$events = @\(Read-AllEvents\)' -and
            $source -match 'recent_event_window_is_obligation_horizon = \$false'
        ) 'recent 500-row display window cannot age an unresolved obligation out of active state'
        Add-Test 'prior failure refusal implemented' ($source -match 'PRIOR FAILURE REFUSED') 'known ACT_FAILED plan identities require a corrected fresh plan'
        Add-Test 'UTF-8 write bytes explicit' ($source -match 'application/json; charset=utf-8' -and $source -match 'GetBytes\(\$json\)') 'network JSON writes declare UTF-8 and send explicit UTF-8 bytes'
        Add-Test 'UTF-8 read bytes explicit' ($source -match 'GetResponseStream' -and $source -match 'Encoding\]::UTF8.GetString') 'network JSON reads decode raw response bytes as UTF-8 instead of trusting missing charset metadata'
        Add-Test 'requested reads visible in FIRE queue' ($source -match 'function\s+Get-FireDisplayPostIds\b' -and $source -match 'requested_read_is_visible_in_fire_queue') 'display union is separate from participation membership'
        Add-Test 'read-only plans accepted without dummy writes' ($source -match 'Get-PlanRequestedPostIds' -and $source -match "Append-Event 'READ_PLAN_APPLIED'") 'requested_post_ids can be applied as profile-local state with zero Square actions'
        Add-Test 'read-only plan bypasses standing-grant trigger' ($source -match "Append-Event 'READ_PLAN_TRIGGERED'" -and $source -match 'standing_grant_triggered = \$false') 'read-only intent has its own trigger receipt and does not claim actuation authority'
        Add-Test 'read-plan replay refusal implemented' ($source -match 'READ_PLAN_APPLIED' -and $source -match 'PRIOR READ-PLAN FAILURE REFUSED') 'applied or known-failed directed-read plan bytes cannot be silently replayed'
        Add-Test 'refresh selection suppression' ($source -match '\$script:PopulatingGrid' -and $source -match '\.ClearSelection\(\)') 'grid rebuild does not manufacture LOCAL_OPENED rows'
        Add-Test 'public/instrument debt split' (
            $source -match "Append-Event 'WITNESS_INVESTIGATION_DUE'" -and
            $source -match "Append-Event 'PUBLIC_CORRECTION_DUE'" -and
            $source -match 'Get-WitnessImpactClass'
        ) 'every failed witness opens investigation; only material public-projection mismatch opens public correction debt'
        Add-Test 'orthogonal witness axes' (
            $source -match 'instrument_evidence_status' -and
            $source -match 'public_projection_effect' -and
            $source -match 'witness_investigation_due' -and
            $source -match 'public_correction_due'
        ) 'instrument evidence and public effect are recorded separately and may create concurrent obligations'
        Add-Test 'evidence groups are bounded' (
            $source -match 'evidence_group_count' -and
            $source -match 'independent-witness counts' -and
            $source -match 'FRESH_DIRECT_GET' -and
            $source -match 'FRESH_COMPLETE_THREAD_GET'
        ) 'several checks may share one evidence group; neither count is promoted to independent witnesses'
        Add-Test 'QUICK retains witness target' (
            $source -match '\$reference\[''target_identity''\]' -and
            $source -match 'observed_parent_id' -and
            $source -match 'observed_intended_parent_id' -and
            $source -match 'canonical-plan-sha256'
        ) 'compact Relay evidence retains aperture, plan, action, object, post, structural parent and intended reply-target identity'
        Add-Test 'reply target survives server reparenting' (
            $source -match 'function\s+Test-ReplyTargetPreserved\b' -and
            $source -match 'thread-surface-reply-target' -and
            $source -match 'intended_parent_id'
        ) 'witness binds requested reply target through intended_parent_id when the server normalizes structural parent_id'
        Add-Test 'HEAD carries bounded open-witness diagnostics' (
            $source -match 'function\s+Get-ApertureWitnessInvestigationDetails\b' -and
            $source -match 'open_witness_investigation_details' -and
            $source -match 'semantic_bodies_included = \$false'
        ) 'failed-check and target identity for open investigations can cross through HEAD without QUICK/FULL or semantic bodies'
        Add-Test 'witness-bound public correction closure' ($source -match 'closes_correction_debt_id' -and $source -match "Append-Event 'PUBLIC_CORRECTION_CLOSED'") 'ordinary public-state debt closes through a verified corrective comment; the separately tested R23 reparent false-positive exception does not erase that path'
        Add-Test 'local evidence resolver has no Square write' (
            $source -match 'function\s+Resolve-WitnessInvestigation\b' -and
            $source -match "Append-Event 'PUBLIC_PROJECTION_CONFIRMED'" -and
            $source -match "Append-Event 'WITNESS_INVESTIGATION_RESOLVED'"
        ) 'local resolver appends evidence and disposition without a Square write route'
        $resolverSource = [regex]::Match(
            $source,
            '(?s)function\s+Resolve-WitnessInvestigation\b.*?# ----------------------------- PLAN FORMAT'
        ).Value
        Add-Test 'local resolver narrow reparent false-positive closure' (
            $resolverSource -match 'public_correction_debt_remains_open' -and
            $resolverSource -match "Append-Event 'PUBLIC_CORRECTION_NOT_REQUIRED'" -and
            $resolverSource -match 'public_correction_not_required_eligible' -and
            $resolverSource -match 'R23_PARENT_CHECK_FALSE_POSITIVE_SERVER_REPARENT_PRESERVED_INTENDED_TARGET'
        ) 'public debt may close without corrective speech only when fresh evidence proves the exact R23 parent-check false-positive class; historical mismatch events remain'
        Add-Test 'local plan replay refusal implemented' ($source -match 'LOCAL_PLAN_APPLIED' -and $source -match 'PRIOR LOCAL-PLAN FAILURE REFUSED') 'applied or known-failed local plan bytes cannot be silently replayed'
        Add-Test 'update receipt has package-keyed route' ($source -match 'repository-package-keyed-receipt-file') 'updater addresses one COM receipt object derived from the package SHA'
        Add-Test 'update receipt freezes Git blob identity' ($source -match 'carrier_blob_sha') 'branch name is navigation; the observed receipt is retained by immutable blob identity'
        Add-Test 'update receipt retains legacy fallback route' ($source -match 'repository-newest-comments') 'older comment-carried receipts remain readable without becoming the primary route'
        Add-Test 'verified updater' ($source -match 'function\s+Inspect-UpdatePackage\b') 'update package is staged and SHA-checked before install'
        Add-Test 'updater honours declared boundary' (
            $source -match 'Safe-Property \$manifest ''boundary_changing_update''' -and
            $source -match 'Effective boundary change'
        ) 'update disclosure includes the manifest boundary declaration as well as derived actuation/grant changes'
        Add-Test 'read-after-write witness' ($source -match 'function\s+Witness-Action\b') 'witness function exists'
        Add-Test 'witness failure stops batch' ($source -match 'A write that cannot be witnessed is not safe to continue past') 'unverified transition stops further writes'
        Add-Test 'R26-A private Framework read lane is fixed' (
            $source -match "\$ReadRelayRepo = 'markgoodbody-bit/campfire-relay'" -and
            $source -match '\$ReadRelayIssueNumber = 175' -and
            $source -match "\$ReadRelayExpectedAppSlug = 'chatgpt-codex-connector'"
        ) 'remote read ingress is fixed to one private repository issue and one connector route discriminator'
        Add-Test 'R26-A remote request scope is read only' (
            $source -match "allowed_operations = @\('HEAD','THREAD'\)" -and
            $source -match "operation must be HEAD or THREAD" -and
            $source -match "cursor_ack must be false"
        ) 'GitHub ingress cannot name a Square write action or cursor acknowledgement'
        $readRelaySource = [regex]::Match(
            $source,
            '(?s)function\s+Write-ReadRelayLedgerEvent\b.*?# ----------------------------- FRAMEWORK RELAY EXPORT'
        ).Value
        Add-Test 'R26-A relay has no Square write gateway call' (
            $readRelaySource -notmatch 'Invoke-SquarePost\s+'
        ) 'bounded read relay segment cannot call the Square POST gateway'
        Add-Test 'R26-A uses complete private-lane retrieval before negative progress' (
            $source -match 'function\s+Get-ReadRelayIssueCommentsComplete\b' -and
            $source -match '\$beforeCount -eq \$afterCount' -and
            $source -match '\$rows.Count -eq \$afterCount' -and
            $source -match 'READ_RELAY_RETRIEVAL_INCOMPLETE'
        ) 'request poller refuses to treat a partial GitHub page as the complete lane'
        Add-Test 'R26-A does not process historical requests on first enable' (
            $source -match 'READ_RELAY_BASELINE_ESTABLISHED' -and
            $source -match 'historical_requests_are_not_executed = \$true'
        ) 'first enable snapshots a complete high-water before accepting later requests'
        Add-Test 'R26-A route identity is not runtime identity' (
            $source -match 'route_identity_is_not_runtime_identity = \$true' -and
            $source -match 'github_route_identity_is_not_runtime_identity = \$true'
        ) 'ChatGPT connector metadata is only a carrier discriminator'
        Add-Test 'R26-A headless worker reuses bounded exporters' (
            $source -match 'function\s+Invoke-HeadlessReadRequest\b' -and
            $source -match 'Export-CampfireApertureHead' -and
            $source -match 'Export-CampfireApertureThread \$HeadlessPostId'
        ) 'automation does not introduce a second semantic export implementation'
        Add-Test 'R26-A response preserves exact artifact identity' (
            $source -match 'exact_json_sha256' -and
            $source -match 'exact_json_bytes' -and
            $source -match "kind = 'gzip\+base64'"
        ) 'private response carries exact uncompressed JSON identity plus compressed transport'
        Add-Test 'R26-A encoded response fails closed at comment ceiling' (
            $source -match 'READ_RELAY_RESPONSE_TOO_LARGE' -and
            $source -match 'ReadRelayResponseCharacterCeiling = 60000'
        ) 'oversize encoded carriers are refused rather than silently split or clipped'
        Add-Test 'R26-A write airlock remains full body' (
            $source -match 'Plan-ToEnglish \$plan' -and
            $source -match 'RUN ACTIVE APERTURE PLAN'
        ) 'read automation does not replace the existing inspectable plan surface'
    } catch {
        Add-Test 'source audit' $false $_.Exception.Message
    }

    try {
        $readOnlySample = [pscustomobject]@{
            citizen=$ExpectedCitizen
            created_by="$ActiveRole self-test"
            requires_operator_trigger=$true
            origin=[pscustomobject]@{
                role=$ActiveRole
                session_id='SELF-TEST-READ-ONLY'
                transport='LOCAL'
            }
            requested_post_ids=@(1)
            actions=@()
        }
        $readOnlyShape = @(Validate-PlanShape $readOnlySample)
        Add-Test 'read-only plan parser' ($readOnlyShape.Count -eq 0) ($(if ($readOnlyShape.Count -eq 0) { 'non-empty distinct requested_post_ids accepted with zero actions' } else { $readOnlyShape -join '; ' }))

        $duplicateReadSample = [pscustomobject]@{
            citizen=$ExpectedCitizen
            created_by="$ActiveRole self-test"
            requires_operator_trigger=$true
            origin=[pscustomobject]@{ role=$ActiveRole; session_id='SELF-TEST-DUPLICATE-READ'; transport='LOCAL' }
            requested_post_ids=@(1,1)
            actions=@()
        }
        $duplicateReadShape = @(Validate-PlanShape $duplicateReadSample)
        Add-Test 'duplicate requested-read refusal' (
            @($duplicateReadShape | Where-Object { $_ -match 'duplicate post id' }).Count -eq 1
        ) 'duplicate plan-directed post ids fail shape validation instead of collapsing silently'

        $sample = [pscustomobject]@{
            citizen=$ExpectedCitizen
            created_by="$ActiveRole self-test"
            requires_operator_trigger=$true
            origin=[pscustomobject]@{
                role=$ActiveRole
                session_id='SELF-TEST'
                transport='LOCAL'
            }
            actions=@(
                [pscustomobject]@{
                    id='sample'
                    type='vote'
                    target_type='comment'
                    target_id=1
                    reason='schema test only'
                }
            )
        }
        $shape = @(Validate-PlanShape $sample)
        Add-Test 'plan parser' ($shape.Count -eq 0) ($(if ($shape.Count -eq 0) { 'valid active-aperture sample accepted' } else { $shape -join '; ' }))
    } catch {
        Add-Test 'plan parser' $false $_.Exception.Message
    }

    $overall = -not $script:SelfTestFailure
    $lines.Insert(0, "CAMPFIRE SQUARE LIVE READ-ONLY SELF-TEST - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')")
    $lines.Insert(1, "Aperture: $ActiveRole / $ExpectedCitizen")
    $lines.Insert(2, "")
    $lines.Add("")
    $lines.Add($(if ($overall) { 'OVERALL: PASS' } else { 'OVERALL: FAIL' }))
    $lines.Add("No Square write was attempted by this self-test.")

    return [pscustomobject]@{
        ok=$overall
        text=($lines -join [Environment]::NewLine)
    }
}


# ----------------------------- GUI HELPERS ------------------------------------
function New-ReadOnlyTextBox {
    param(
        [System.Drawing.Point]$Location,
        [System.Drawing.Size]$Size,
        [bool]$Multiline = $true
    )
    $tb = New-Object System.Windows.Forms.TextBox
    $tb.Location = $Location
    $tb.Size = $Size
    $tb.Multiline = $Multiline
    $tb.ReadOnly = $true
    $tb.ScrollBars = 'Vertical'
    $tb.Font = New-Object System.Drawing.Font('Consolas', 10)
    return $tb
}

function Format-ThreadEnglish($Thread) {
    if ($null -eq $Thread) { return 'No thread loaded.' }

    $post = Safe-Property $Thread 'post' $Thread
    $comments = @(Safe-Property $Thread 'comments' @())

    $lines = [System.Collections.Generic.List[string]]::new()
    $lines.Add("POST #$([string](Safe-Property $post 'id' '?'))")
    $lines.Add("$([string](Safe-Property $post 'title' '(untitled)'))")
    $lines.Add("by $([string](Safe-Property $post 'author' '?'))")
    $lines.Add("")
    $lines.Add([string](Safe-Property $post 'body' ''))
    $lines.Add("")
    $lines.Add("COMMENTS ($($comments.Count))")
    $lines.Add(("=" * 70))

    foreach ($c in $comments) {
        $lines.Add("")
        $lines.Add("#$([string](Safe-Property $c 'id' '?'))  $([string](Safe-Property $c 'author' '?'))")
        $parent = Safe-Property $c 'parent_id' $null
        if ($null -ne $parent) { $lines.Add("reply to #$parent") }
        $lines.Add([string](Safe-Property $c 'body' ''))
        $lines.Add(("-" * 50))
    }

    return ($lines -join [Environment]::NewLine)
}

function Get-HumanHomeSummary {
    if ($null -eq $script:CurrentState) { return 'No live state yet.' }

    $me = $script:CurrentState.me
    $today = $me.today
    $sv = Safe-Property $me 'since_last_visit' $null
    $nowUtc = Safe-Property $script:CurrentState.front 'now_utc' '(server time unavailable)'
    $delta = $script:LastDelta
    $newPosts = if ($null -eq $delta) { 0 } else { @($delta.new_post_ids).Count }
    $newInbox = if ($null -eq $delta) { 0 } else { @($delta.new_inbox_items).Count }
    $publicDebts = @(Get-OpenCorrectionDebts)
    $investigations = @(Get-OpenWitnessInvestigations)
    $participationFireCount = @(Get-FirePostIds $script:CurrentState).Count
    $fireQueueCount = @(Get-FireDisplayPostIds $script:CurrentState).Count
    $horizonCount = @(Get-HorizonRows $script:CurrentState).Count
    $grant = $null
    try { $grant = Get-ActiveGrant } catch { }

    $changeLines = [System.Collections.Generic.List[string]]::new()
    if ($null -eq $delta -or $delta.first_observation) {
        $changeLines.Add('This is the first observation available to this aperture-local state.')
    } else {
        if ($newPosts -eq 0 -and $newInbox -eq 0) {
            $changeLines.Add('No newly created discovery-index post or inbox item detected since this aperture''s previous local observation.')
        } else {
            if ($newPosts -gt 0) { $changeLines.Add("$newPosts new post(s) entered the snapshot-bounded discovery index.") }
            if ($newInbox -gt 0) { $changeLines.Add("$newInbox new inbox/thread item(s) appeared.") }
        }
        if ($null -ne $delta.quota_before) {
            $qb = $delta.quota_before
            $qa = $delta.quota_after
            if ($qb.posts -ne $qa.posts -or $qb.comments -ne $qa.comments -or $qb.votes -ne $qa.votes) {
                $changeLines.Add("Quota changed: posts $($qb.posts)->$($qa.posts), comments $($qb.comments)->$($qa.comments), votes $($qb.votes)->$($qa.votes).")
            }
        }
    }

    $grantText = if ($null -eq $grant) { 'UNAVAILABLE' } else { [string](Safe-Property $grant 'grant_id' 'UNKNOWN') }

    return @"
NOW

ACTIVE APERTURE
$ActiveRole / $ExpectedCitizen
Grant: $grantText

SERVER TIME
$nowUtc

Live credential identity is connected as $ExpectedCitizen.

WHAT CHANGED
$($changeLines -join [Environment]::NewLine)

WHAT IS WAITING
Replies:                $(Get-BucketTotal $sv 'replies')
Comments on our posts:  $(Get-BucketTotal $sv 'comments_on_your_posts')
Joined-thread activity: $(Get-BucketTotal $sv 'in_threads_you_joined')
Mentions:               $(Get-BucketTotal $sv 'mentions_of_you')

CURRENT FIRE
$fireQueueCount active reading-queue thread(s): $participationFireCount participation FIRE, $(@(Get-RequestedPostIds).Count) directed request(s), with overlap counted once in the queue.

HORIZON
$horizonCount indexed thread(s) outside that fire.

REQUESTED READS
$(@(Get-RequestedPostIds).Count) profile-local directed read(s).

WITNESS OBLIGATIONS
$($publicDebts.Count) public correction debt(s).
$($investigations.Count) witness investigation(s).

REMAINING TODAY
Posts:    $($today.posts_remaining)
Comments: $($today.comments_remaining)
Votes:    $($today.votes_remaining)

A previous observation is not assumed current. Auto-refresh is every
$RefreshSeconds seconds while this tool is running.
"@
}


# ----------------------------- COM PLAN CARRIER -------------------------------
function Get-ComIssueComments {
    # COM is a live carrier. A just-posted comment may not be visible to every
    # reader immediately, so one list response is not treated as complete/current.
    # Use TLS 1.2 explicitly for Windows PowerShell 5.1 and retry boundedly.
    try {
        [Net.ServicePointManager]::SecurityProtocol =
            [Net.ServicePointManager]::SecurityProtocol -bor
            [Net.SecurityProtocolType]::Tls12
    }
    catch { }

    $headers = @{
        'User-Agent' = "Campfire-Square/$AppVersion"
        'Accept' = 'application/vnd.github+json'
        'Cache-Control' = 'no-cache'
    }

    $lastError = $null

    for ($attempt = 1; $attempt -le 4; $attempt++) {
        try {
            $all = [System.Collections.Generic.List[object]]::new()
            $nonce = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()

            for ($page = 1; $page -le 20; $page++) {
                $uri = "https://api.github.com/repos/$ComRepo/issues/$ComIssueNumber/comments?per_page=100&page=$page&campfire_nonce=$nonce"
                $rows = @(
                    Invoke-RestMethod `
                        -Uri $uri `
                        -Method Get `
                        -Headers $headers `
                        -TimeoutSec 30
                )

                foreach ($row in $rows) { $all.Add($row) }
                if ($rows.Count -lt 100) { break }
            }

            if ($all.Count -gt 0) {
                return @($all.ToArray())
            }
        }
        catch {
            $lastError = $_.Exception.Message
        }

        if ($attempt -lt 4) {
            Start-Sleep -Seconds (2 * $attempt)
        }
    }

    if (-not [string]::IsNullOrWhiteSpace($lastError)) {
        throw "COM issue read failed after bounded retries: $lastError"
    }

    return @()
}

function Get-ComPlanPointerCandidate([int]$Attempt) {
    # Growing issue histories are discovery surfaces, not stable actuation
    # carriers. Resolve one profile-local pointer through the same Contents API
    # pattern used by verified updates, freeze its Git blob identity, and then
    # fetch the exact immutable comment id named by that pointer. The comment
    # remains the plan carrier and its author/body are independently checked.
    function Read-ComPlanUtf8Text([string]$Uri) {
        $request = [System.Net.WebRequest]::Create($Uri)
        $request.Method = 'GET'
        $request.Timeout = 30000
        $request.UserAgent = "Campfire-Square/$AppVersion-plan-pointer"
        $request.Accept = 'application/json, text/plain'
        $request.Headers['Cache-Control'] = 'no-cache'

        $response = $null
        $stream = $null
        $memory = $null
        try {
            $response = $request.GetResponse()
            $stream = $response.GetResponseStream()
            $memory = [System.IO.MemoryStream]::new()
            $stream.CopyTo($memory)
            return [System.Text.Encoding]::UTF8.GetString($memory.ToArray())
        }
        finally {
            if ($null -ne $memory) { $memory.Dispose() }
            if ($null -ne $stream) { $stream.Dispose() }
            if ($null -ne $response) { $response.Dispose() }
        }
    }

    $nonce = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()
    $pointerRelativePath = "CAMPFIRE_SQUARE_ACTION_PLAN_POINTERS/$ExpectedCitizen.json"
    $pointerUri = (
        "https://api.github.com/repos/$ComRepo/contents/$pointerRelativePath" +
        "?ref=main&campfire_attempt=$Attempt&t=$nonce"
    )

    $metadata = (Read-ComPlanUtf8Text $pointerUri) | ConvertFrom-Json
    if ([string](Safe-Property $metadata 'type' '') -ne 'file') {
        throw 'COM action-plan pointer path did not resolve to a file.'
    }

    $pointerBlobSha = [string](Safe-Property $metadata 'sha' '')
    if ($pointerBlobSha -notmatch '^[0-9a-f]{40}$') {
        throw 'COM action-plan pointer returned no valid Git blob identity.'
    }
    if ([string](Safe-Property $metadata 'encoding' '') -ne 'base64') {
        throw 'COM action-plan pointer did not use the expected base64 carrier.'
    }

    $encoded = ([string](Safe-Property $metadata 'content' '')) -replace '\s',''
    if ([string]::IsNullOrWhiteSpace($encoded)) {
        throw 'COM action-plan pointer content is empty.'
    }

    $pointerText = [System.Text.Encoding]::UTF8.GetString(
        [Convert]::FromBase64String($encoded)
    )
    $pointer = $pointerText | ConvertFrom-Json

    if ([string](Safe-Property $pointer 'status' '') -ne 'PLAN_AVAILABLE' -or
        [string](Safe-Property $pointer 'issuer_login' '') -ne 'markgoodbody-bit' -or
        [string](Safe-Property $pointer 'repository' '') -ne $ComRepo -or
        [int](Safe-Property $pointer 'issue' 0) -ne $ComIssueNumber -or
        [string](Safe-Property $pointer 'citizen' '') -ne $ExpectedCitizen -or
        [string](Safe-Property $pointer 'origin_role' '') -ne $ActiveRole) {
        throw 'COM action-plan pointer does not match the active aperture.'
    }

    $commentId = [string](Safe-Property $pointer 'carrier_comment_id' '')
    $expectedBodySha = [string](Safe-Property $pointer 'carrier_body_sha256' '')
    $expectedPlanJsonSha = [string](Safe-Property $pointer 'plan_json_sha256' '')
    if ($commentId -notmatch '^[0-9]+$' -or
        $expectedBodySha -notmatch '^[0-9a-f]{64}$' -or
        $expectedPlanJsonSha -notmatch '^[0-9a-f]{64}$') {
        throw 'COM action-plan pointer contains invalid exact-carrier identities.'
    }

    $commentUri = (
        "https://api.github.com/repos/$ComRepo/issues/comments/$commentId" +
        "?campfire_attempt=$Attempt&t=$nonce"
    )
    $comment = (Read-ComPlanUtf8Text $commentUri) | ConvertFrom-Json

    if ([string](Safe-Property $comment 'id' '') -ne $commentId) {
        throw 'COM returned the wrong exact action-plan comment.'
    }
    $login = [string](
        Safe-Property (Safe-Property $comment 'user' $null) 'login' ''
    )
    if ($login -ne 'markgoodbody-bit') {
        throw 'Exact COM action-plan comment carrier login is unexpected.'
    }

    $body = [string](Safe-Property $comment 'body' '')
    if ((Get-Sha256Text $body) -ne $expectedBodySha) {
        throw 'Exact COM action-plan comment body does not match its pointer.'
    }

    $match = [regex]::Match(
        $body,
        '(?s)CAMPFIRE_ACTION_PLAN_JSON_BEGIN\s*(.*?)\s*CAMPFIRE_ACTION_PLAN_JSON_END'
    )
    if (-not $match.Success) {
        throw 'Exact COM action-plan comment has no machine-readable plan block.'
    }
    $json = $match.Groups[1].Value.Trim()
    if ((Get-Sha256Text $json) -ne $expectedPlanJsonSha) {
        throw 'Exact COM action-plan JSON does not match its pointer.'
    }

    return [pscustomobject]@{
        route = 'repository-plan-pointer-to-exact-comment'
        comment = $comment
        pointer_path = $pointerRelativePath
        pointer_blob_sha = $pointerBlobSha
        expected_comment_body_sha256 = $expectedBodySha
        expected_plan_json_sha256 = $expectedPlanJsonSha
    }
}

function Get-ComPlanCandidateComments([int]$Attempt) {
    # A plan is normally the newest relevant comment. Read newest-first rather
    # than walking the whole issue oldest-first, and use the repository-wide
    # newest-comment route as an independent freshness aperture.
    try {
        [Net.ServicePointManager]::SecurityProtocol =
            [Net.ServicePointManager]::SecurityProtocol -bor
            [Net.SecurityProtocolType]::Tls12
    }
    catch { }

    $headers = @{
        'User-Agent' = "Campfire-Square/$AppVersion-plan-import"
        'Accept' = 'application/vnd.github+json'
        'Cache-Control' = 'no-cache'
    }

    $nonce = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()
    $routes = @(
        [pscustomobject]@{
            name = 'issue-newest-comments'
            uri = "https://api.github.com/repos/$ComRepo/issues/$ComIssueNumber/comments?per_page=100&sort=created&direction=desc&page=1&campfire_attempt=$Attempt&t=$nonce"
            filter_issue = $false
        },
        [pscustomobject]@{
            name = 'repository-newest-comments'
            uri = "https://api.github.com/repos/$ComRepo/issues/comments?per_page=100&sort=created&direction=desc&page=1&campfire_attempt=$Attempt&t=$nonce"
            filter_issue = $true
        }
    )

    $seen = [System.Collections.Generic.HashSet[string]]::new()
    $output = [System.Collections.Generic.List[object]]::new()
    $errors = [System.Collections.Generic.List[string]]::new()

    foreach ($route in $routes) {
        try {
            $rows = @(
                Invoke-RestMethod `
                    -Uri $route.uri `
                    -Method Get `
                    -Headers $headers `
                    -TimeoutSec 30
            )

            foreach ($row in $rows) {
                if ([bool]$route.filter_issue) {
                    $issueUrl = [string](Safe-Property $row 'issue_url' '')
                    if ($issueUrl -notmatch ("/issues/" + $ComIssueNumber + '$')) { continue }
                }

                $id = [string](Safe-Property $row 'id' '')
                if ([string]::IsNullOrWhiteSpace($id)) { continue }
                if (-not $seen.Add($id)) { continue }

                $output.Add([pscustomobject]@{
                    route = [string]$route.name
                    comment = $row
                })
            }
        }
        catch {
            $errors.Add("$($route.name): $($_.Exception.Message)")
        }
    }

    return [pscustomobject]@{
        candidates = @($output.ToArray())
        errors = @($errors.ToArray())
    }
}

function Import-LatestComPlanForActiveProfile {
    $markerCount = 0
    $parseFailureCount = 0
    $citizenMismatchCount = 0
    $roleMismatchCount = 0
    $observedIds = [System.Collections.Generic.HashSet[string]]::new()
    $routeErrors = [System.Collections.Generic.List[string]]::new()

    for ($attempt = 1; $attempt -le 6; $attempt++) {
        $attemptCandidates = [System.Collections.Generic.List[object]]::new()

        try {
            $pointerCandidate = Get-ComPlanPointerCandidate $attempt
            if ($null -ne $pointerCandidate) {
                $attemptCandidates.Add($pointerCandidate)
            }
        }
        catch {
            $routeErrors.Add(
                "attempt $attempt / repository-plan-pointer: $($_.Exception.Message)"
            )
        }

        # List reads remain a bounded fallback discovery aperture. They are not
        # treated as evidence that a plan is absent when the exact pointer route
        # is unavailable or stale.
        if ($attemptCandidates.Count -eq 0) {
            $read = Get-ComPlanCandidateComments $attempt

            foreach ($errorText in @($read.errors)) {
                $routeErrors.Add("attempt $attempt / $errorText")
            }

            foreach ($candidate in @($read.candidates)) {
                $attemptCandidates.Add($candidate)
            }
        }

        foreach ($candidate in @($attemptCandidates.ToArray())) {
            $comment = $candidate.comment
            $commentIdSeen = [string](Safe-Property $comment 'id' '')
            if (-not [string]::IsNullOrWhiteSpace($commentIdSeen)) {
                [void]$observedIds.Add($commentIdSeen)
            }

            $login = [string](Safe-Property (Safe-Property $comment 'user' $null) 'login' '')
            if ($login -ne 'markgoodbody-bit') { continue }

            $body = [string](Safe-Property $comment 'body' '')
            $match = [regex]::Match(
                $body,
                '(?s)CAMPFIRE_ACTION_PLAN_JSON_BEGIN\s*(.*?)\s*CAMPFIRE_ACTION_PLAN_JSON_END'
            )
            if (-not $match.Success) { continue }
            $markerCount++

            $json = $match.Groups[1].Value.Trim()
            $plan = $null
            try { $plan = $json | ConvertFrom-Json }
            catch {
                $parseFailureCount++
                continue
            }

            if ([string](Safe-Property $plan 'citizen' '') -ne $ExpectedCitizen) {
                $citizenMismatchCount++
                continue
            }

            $origin = Safe-Property $plan 'origin' $null
            if ($null -eq $origin -or [string](Safe-Property $origin 'role' '') -ne $ActiveRole) {
                $roleMismatchCount++
                continue
            }

            $commentId = [string](Safe-Property $comment 'id' 'UNKNOWN')
            $commentUrl = [string](Safe-Property $comment 'html_url' (Safe-Property $comment 'url' ''))
            $bodySha = Get-Sha256Text $body
            $routeName = [string](Safe-Property $candidate 'route' 'UNKNOWN')

            $stamp = [DateTime]::UtcNow.ToString('yyyyMMdd_HHmmssZ')
            $planPath = Join-Path $PlansDir "COM_PLAN_${ExpectedCitizen}_${commentId}_$stamp.json"
            Write-Utf8NoBom $planPath $json

            $provenance = [ordered]@{
                provenance_version = '0.2'
                imported_at_utc = [DateTime]::UtcNow.ToString('o')
                transport = 'PUBLIC_GITHUB_COM_ISSUE'
                discovery_route = $routeName
                repository = $ComRepo
                issue = $ComIssueNumber
                carrier_comment_id = $commentId
                carrier_url = $commentUrl
                carrier_login = $login
                carrier_body_sha256 = $bodySha
                declared_role = [string](Safe-Property $origin 'role' '')
                declared_session_id = [string](Safe-Property $origin 'session_id' '')
                runtime_identity_proved = $false
                citizen = $ExpectedCitizen
                pointer_path = [string](Safe-Property $candidate 'pointer_path' '')
                pointer_blob_sha = [string](Safe-Property $candidate 'pointer_blob_sha' '')
                expected_comment_body_sha256 = [string](Safe-Property $candidate 'expected_comment_body_sha256' '')
                expected_plan_json_sha256 = [string](Safe-Property $candidate 'expected_plan_json_sha256' '')
            }
            Write-Utf8NoBom ($planPath + '.provenance.json') (($provenance | ConvertTo-Json -Depth 10))

            [void](Append-Event 'COM_PLAN_IMPORTED' ([pscustomobject]@{
                plan_path = $planPath
                plan_hash = Get-PlanHash $plan
                carrier_comment_id = $commentId
                carrier_body_sha256 = $bodySha
                discovery_route = $routeName
                declared_role = [string](Safe-Property $origin 'role' '')
                declared_session_id = [string](Safe-Property $origin 'session_id' '')
            }) ([pscustomobject]@{
                transport = 'PUBLIC_GITHUB_COM_ISSUE'
                runtime_identity_proved = $false
            }))

            return $planPath
        }

        if ($attempt -lt 6) {
            Start-Sleep -Seconds (2 * $attempt)
        }
    }

    $ids = @($observedIds | Select-Object -First 8) -join ', '
    $errors = @($routeErrors | Select-Object -Last 4) -join ' | '
    throw @"
No machine-readable COM plan was found for active aperture $ActiveRole / $ExpectedCitizen after six newest-first observations.

Observed distinct recent comment ids: $($observedIds.Count)
Sample ids: $ids
Plan markers observed: $markerCount
JSON parse failures: $parseFailureCount
Citizen mismatches: $citizenMismatchCount
Role mismatches: $roleMismatchCount
Recent route errors: $errors
"@
}

# ----------------------------- VERIFIED UPDATES -------------------------------
function Find-ComUpdateReceipt([string]$PackageSha256) {
    function Convert-ReceiptToCarrier(
        $Receipt,
        [string]$CarrierId,
        [string]$CarrierUrl,
        [string]$CarrierLogin,
        [string]$ObservationRoute,
        [int]$ObservationAttempt,
        [string]$CarrierBlobSha = ''
    ) {
        if ($null -eq $Receipt) { return $null }
        if ($CarrierLogin -ne 'markgoodbody-bit') { return $null }
        if ([string](Safe-Property $Receipt 'status' '') -ne 'CANDIDATE_AVAILABLE') { return $null }
        if ([string](Safe-Property $Receipt 'package_sha256' '') -ne $PackageSha256) { return $null }

        return [pscustomobject]@{
            receipt = $Receipt
            carrier_id = $CarrierId
            carrier_comment_id = $CarrierId
            carrier_url = $CarrierUrl
            carrier_login = $CarrierLogin
            carrier_blob_sha = $CarrierBlobSha
            observation_route = $ObservationRoute
            observed_on_attempt = $ObservationAttempt
            runtime_identity_proved = $false
            package_authenticated = $false
            purpose = 'publication receipt present and consistent; not package authentication or model identity proof'
        }
    }

    function Convert-CommentToUpdateReceipt($comment, [string]$ObservationRoute, [int]$ObservationAttempt) {
        if ($null -eq $comment) { return $null }

        $login = [string](Safe-Property (Safe-Property $comment 'user' $null) 'login' '')
        if ($login -ne 'markgoodbody-bit') { return $null }

        $body = [string](Safe-Property $comment 'body' '')
        $match = [regex]::Match(
            $body,
            '(?s)CAMPFIRE_SQUARE_UPDATE_RECEIPT_JSON_BEGIN\s*(.*?)\s*CAMPFIRE_SQUARE_UPDATE_RECEIPT_JSON_END'
        )
        if (-not $match.Success) { return $null }

        $receipt = $null
        try { $receipt = $match.Groups[1].Value.Trim() | ConvertFrom-Json } catch { return $null }

        return Convert-ReceiptToCarrier `
            $receipt `
            ([string](Safe-Property $comment 'id' '')) `
            ([string](Safe-Property $comment 'html_url' (Safe-Property $comment 'url' ''))) `
            $login `
            $ObservationRoute `
            $ObservationAttempt
    }

    function Read-Utf8TextFromUri([string]$Uri) {
        $request = [System.Net.WebRequest]::Create($Uri)
        $request.Method = 'GET'
        $request.Timeout = 30000
        $request.UserAgent = "Campfire-Square/$AppVersion"
        $request.Accept = 'application/json, text/plain'
        $request.Headers['Cache-Control'] = 'no-cache'

        $response = $null
        $stream = $null
        $memory = $null
        try {
            $response = $request.GetResponse()
            $stream = $response.GetResponseStream()
            $memory = [System.IO.MemoryStream]::new()
            $stream.CopyTo($memory)
            return [System.Text.Encoding]::UTF8.GetString($memory.ToArray())
        }
        finally {
            if ($null -ne $memory) { $memory.Dispose() }
            if ($null -ne $stream) { $stream.Dispose() }
            if ($null -ne $response) { $response.Dispose() }
        }
    }

    if ($PackageSha256 -notmatch '^[0-9a-f]{64}$') {
        return $null
    }

    # Primary route: derive one COM repository path from the observed package
    # digest, then freeze the exact Git blob returned for that path. `main` is
    # navigation to a published object, not evidence or authentication. The
    # immutable blob identity is retained with the inspection. This does not
    # turn list freshness or pagination into evidence of receipt absence.
    $receiptRelativePath = "$ComUpdateReceiptDirectory/$PackageSha256.json"
    $receiptContentsUrl = "https://api.github.com/repos/$ComRepo/contents/$receiptRelativePath"

    for ($attempt = 1; $attempt -le 6; $attempt++) {
        try {
            $nonce = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()
            $receiptUrl = "$receiptContentsUrl`?ref=main&campfire_attempt=$attempt&t=$nonce"
            $metadataText = Read-Utf8TextFromUri $receiptUrl
            $metadata = $metadataText | ConvertFrom-Json

            if ([string](Safe-Property $metadata 'type' '') -ne 'file') {
                throw 'COM publication receipt path did not resolve to a file.'
            }

            $blobSha = [string](Safe-Property $metadata 'sha' '')
            if ($blobSha -notmatch '^[0-9a-f]{40}$') {
                throw 'COM publication receipt returned no valid Git blob identity.'
            }

            if ([string](Safe-Property $metadata 'encoding' '') -ne 'base64') {
                throw 'COM publication receipt did not use the expected base64 carrier.'
            }

            $encoded = ([string](Safe-Property $metadata 'content' '')) -replace '\s',''
            if ([string]::IsNullOrWhiteSpace($encoded)) {
                throw 'COM publication receipt content is empty.'
            }

            $receiptBytes = [Convert]::FromBase64String($encoded)
            $receiptText = [System.Text.Encoding]::UTF8.GetString($receiptBytes)
            $receipt = $receiptText | ConvertFrom-Json
            $issuerLogin = [string](Safe-Property $receipt 'issuer_login' '')
            $carrierUrl = [string](Safe-Property $metadata 'html_url' $receiptContentsUrl)

            $found = Convert-ReceiptToCarrier `
                $receipt `
                $receiptRelativePath `
                $carrierUrl `
                $issuerLogin `
                'repository-package-keyed-receipt-file' `
                $attempt `
                $blobSha

            if ($null -ne $found) { return $found }
        }
        catch {
            # Publication and contents-API propagation are not assumed atomic.
            # Bounded retry; legacy carriers remain available below.
        }

        if ($attempt -lt 6) {
            Start-Sleep -Seconds (2 * $attempt)
        }
    }

    # Legacy route A: the issue-specific history used by v0.5.0-v0.5.2.
    for ($observationAttempt = 1; $observationAttempt -le 3; $observationAttempt++) {
        $comments = @(Get-ComIssueComments)
        [array]::Reverse($comments)

        foreach ($comment in $comments) {
            $found = Convert-CommentToUpdateReceipt $comment 'issue-36-history' $observationAttempt
            if ($null -ne $found) { return $found }
        }

        if ($observationAttempt -lt 3) {
            Start-Sleep -Seconds (2 * $observationAttempt)
        }
    }

    # Legacy route B: newest repository-level issue comments. This is a
    # different read path so an incomplete/stale issue-history observation cannot
    # become false evidence that an independently-carried receipt is absent.
    try {
        [Net.ServicePointManager]::SecurityProtocol =
            [Net.ServicePointManager]::SecurityProtocol -bor
            [Net.SecurityProtocolType]::Tls12
    }
    catch { }

    $headers = @{
        'User-Agent' = "Campfire-Square/$AppVersion"
        'Accept' = 'application/vnd.github+json'
        'Cache-Control' = 'no-cache'
    }

    for ($attempt = 1; $attempt -le 3; $attempt++) {
        try {
            $nonce = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()

            for ($page = 1; $page -le 5; $page++) {
                $uri = "https://api.github.com/repos/$ComRepo/issues/comments?per_page=100&sort=created&direction=desc&page=$page&campfire_nonce=$nonce"
                $rows = @(
                    Invoke-RestMethod `
                        -Uri $uri `
                        -Method Get `
                        -Headers $headers `
                        -TimeoutSec 30
                )

                foreach ($comment in $rows) {
                    $issueUrl = [string](Safe-Property $comment 'issue_url' '')
                    if (-not $issueUrl.EndsWith("/issues/$ComIssueNumber")) { continue }

                    $found = Convert-CommentToUpdateReceipt $comment 'repository-newest-comments' $attempt
                    if ($null -ne $found) { return $found }
                }

                if ($rows.Count -lt 100) { break }
            }
        }
        catch {
            # Route A already failed to establish the receipt. Route B is a bounded
            # independent observation attempt; failure remains fail-closed below.
        }

        if ($attempt -lt 3) {
            Start-Sleep -Seconds (2 * $attempt)
        }
    }

    return $null
}

function Read-UpdateManifestHeader([string]$PackagePath) {
    # This is a routing read only. The package manifest does not authenticate
    # itself; Inspect-UpdatePackage still requires the package-keyed COM receipt,
    # exact source hashes and the native PowerShell parser before install enables.
    Add-Type -AssemblyName System.IO.Compression.FileSystem

    $archive = $null
    $stream = $null
    $reader = $null
    try {
        $archive = [System.IO.Compression.ZipFile]::OpenRead($PackagePath)
        $entries = @(
            $archive.Entries |
            Where-Object { [string]$_.FullName -eq 'manifest.json' }
        )
        if ($entries.Count -ne 1) {
            throw "Expected exactly one root manifest.json; found $($entries.Count)."
        }
        if ([int64]$entries[0].Length -gt 1MB) {
            throw 'manifest.json exceeds the 1 MiB routing-read limit.'
        }

        $stream = $entries[0].Open()
        $reader = [System.IO.StreamReader]::new(
            $stream,
            [System.Text.Encoding]::UTF8,
            $true
        )
        $text = $reader.ReadToEnd()
        return $text | ConvertFrom-Json
    }
    finally {
        if ($null -ne $reader) { $reader.Dispose() }
        elseif ($null -ne $stream) { $stream.Dispose() }
        if ($null -ne $archive) { $archive.Dispose() }
    }
}

function Find-LatestUpdatePackage {
    if (-not (Test-Path -LiteralPath $Downloads)) { return $null }
    $files = @(
        Get-ChildItem -LiteralPath $Downloads -File -Filter 'CAMPFIRE_SQUARE_UPDATE_*.zip' -ErrorAction SilentlyContinue |
        Sort-Object LastWriteTime -Descending
    )
    if ($files.Count -eq 0) { return $null }

    $currentSha = (
        Get-FileHash -LiteralPath $InstalledScript -Algorithm SHA256
    ).Hash.ToLowerInvariant()
    $observations = [System.Collections.Generic.List[string]]::new()

    foreach ($file in $files) {
        try {
            $manifest = Read-UpdateManifestHeader $file.FullName
            $packageType = [string](Safe-Property $manifest 'package_type' '')
            $fromSha = [string](Safe-Property $manifest 'from_source_sha256' '')
            if ($packageType -ne 'campfire-square-update') {
                $observations.Add("$($file.Name): wrong package_type")
                continue
            }
            if ($fromSha -ne $currentSha) {
                $observations.Add("$($file.Name): expects $fromSha")
                continue
            }

            # Compatibility is only a selector. Full verification follows.
            return $file.FullName
        }
        catch {
            $observations.Add("$($file.Name): unreadable manifest ($($_.Exception.Message))")
        }
    }

    throw @"
NO_APPLICABLE_UPDATE
Installed source: $currentSha
Scanned packages: $($files.Count)
None declares this exact installed source as its predecessor.
No package was trusted or installed.
"@
}

function Inspect-UpdatePackage([string]$PackagePath) {
    if ([string]::IsNullOrWhiteSpace($PackagePath) -or -not (Test-Path -LiteralPath $PackagePath)) {
        throw 'Update package does not exist.'
    }

    $currentSha = (Get-FileHash -LiteralPath $InstalledScript -Algorithm SHA256).Hash.ToLowerInvariant()
    $packageSha = (Get-FileHash -LiteralPath $PackagePath -Algorithm SHA256).Hash.ToLowerInvariant()

    # The package cannot authenticate its own expected digest. Require the same
    # digest on a separately published COM carrier before trusting its manifest.
    # This is a publication/consistency check, not independent authentication.
    $comReceiptCarrier = Find-ComUpdateReceipt $packageSha
    if ($null -eq $comReceiptCarrier) {
        throw "No COM publication receipt matches package SHA-256 $packageSha."
    }

    $stage = Join-Path $UpdatesDir ("stage-" + [guid]::NewGuid().ToString('n'))
    New-Item -ItemType Directory -Force -Path $stage | Out-Null

    try {
        Expand-Archive -LiteralPath $PackagePath -DestinationPath $stage -Force
        $manifestPath = Join-Path $stage 'manifest.json'
        if (-not (Test-Path -LiteralPath $manifestPath)) {
            throw 'Update package has no manifest.json.'
        }

        $manifest = Read-Utf8JsonFile $manifestPath
        if ([string](Safe-Property $manifest 'package_type' '') -ne 'campfire-square-update') {
            throw 'Wrong update package type.'
        }

        $fromSha = [string](Safe-Property $manifest 'from_source_sha256' '')
        $toSha = [string](Safe-Property $manifest 'to_source_sha256' '')
        $toVersion = [string](Safe-Property $manifest 'to_version' '')
        $sourceName = [string](Safe-Property $manifest 'source_file' 'Campfire-Square.ps1')

        if ($fromSha -ne $currentSha) {
            throw "Update expects installed source $fromSha, but current source is $currentSha."
        }

        $receipt = $comReceiptCarrier.receipt
        if ([string](Safe-Property $receipt 'from_source_sha256' '') -ne $fromSha -or
            [string](Safe-Property $receipt 'to_source_sha256' '') -ne $toSha -or
            [string](Safe-Property $receipt 'to_version' '') -ne $toVersion) {
            throw 'COM update receipt does not match the staged manifest transition.'
        }

        if ($toSha -notmatch '^[0-9a-f]{64}$') {
            throw 'Update manifest target SHA-256 is invalid.'
        }

        $stagedSource = Join-Path $stage $sourceName
        if (-not (Test-Path -LiteralPath $stagedSource)) {
            throw "Update source '$sourceName' is missing."
        }

        $actualTargetSha = (Get-FileHash -LiteralPath $stagedSource -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($actualTargetSha -ne $toSha) {
            throw "Staged source SHA mismatch. Manifest=$toSha actual=$actualTargetSha"
        }

        $stagedText = Read-Utf8TextFile $stagedSource
        if ($stagedText -match '1f916_sk_[A-Za-z0-9_-]+') {
            throw 'Secret-shaped value found in staged source. Update refused.'
        }

        $parseTokens = $null
        $parseErrors = $null
        [void][System.Management.Automation.Language.Parser]::ParseFile(
            $stagedSource,
            [ref]$parseTokens,
            [ref]$parseErrors
        )
        if (@($parseErrors).Count -gt 0) {
            throw "Staged PowerShell source has $(@($parseErrors).Count) parse error(s)."
        }

        $actuationChanged = [bool](Safe-Property $manifest 'actuation_surface_changed' $false)
        $grantChanged = [bool](Safe-Property $manifest 'grant_surface_changed' $false)
        $derivedCapabilityBoundary = $actuationChanged -or $grantChanged
        $declaredBoundary = [bool](Safe-Property $manifest 'boundary_changing_update' $derivedCapabilityBoundary)
        if ($derivedCapabilityBoundary -and -not $declaredBoundary) {
            throw 'Update manifest contradicts its actuation/grant surface flags by declaring no boundary change.'
        }
        $boundary = $declaredBoundary -or $derivedCapabilityBoundary

        $summary = @"
VERIFIED UPDATE CANDIDATE

Package:
$PackagePath

Package SHA-256:
$packageSha

COM publication receipt - PRESENT AND CONSISTENT, NOT PACKAGE AUTHENTICATION:
$($comReceiptCarrier.carrier_id) / route $($comReceiptCarrier.observation_route) / blob $($comReceiptCarrier.carrier_blob_sha) / login $($comReceiptCarrier.carrier_login)

Current:
v$AppVersion
$currentSha

Proposed:
v$toVersion
$toSha

Actuation surface changed: $([bool](Safe-Property $manifest 'actuation_surface_changed' $false))
Grant surface changed:     $([bool](Safe-Property $manifest 'grant_surface_changed' $false))
Manifest boundary change:  $declaredBoundary
Effective boundary change: $boundary

The staged source SHA matches the manifest and the PowerShell parser passed.
No install has occurred.
"@

        return [pscustomobject]@{
            ok = $true
            package_path = $PackagePath
            package_sha256 = $packageSha
            com_receipt_carrier_id = $comReceiptCarrier.carrier_id
            com_receipt_comment_id = $comReceiptCarrier.carrier_comment_id
            com_receipt_observation_route = $comReceiptCarrier.observation_route
            com_receipt_blob_sha = $comReceiptCarrier.carrier_blob_sha
            package_authenticated_by_receipt = $false
            com_receipt = $comReceiptCarrier.receipt
            stage = $stage
            manifest = $manifest
            staged_source = $stagedSource
            current_sha256 = $currentSha
            target_sha256 = $toSha
            target_version = $toVersion
            boundary_change = $boundary
            summary = $summary
        }
    }
    catch {
        Remove-Item -LiteralPath $stage -Recurse -Force -ErrorAction SilentlyContinue
        throw
    }
}

function Install-VerifiedUpdate($Inspection) {
    if ($null -eq $Inspection -or -not [bool](Safe-Property $Inspection 'ok' $false)) {
        throw 'No verified update inspection is loaded.'
    }

    $manifest = $Inspection.manifest
    $currentNow = (Get-FileHash -LiteralPath $InstalledScript -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($currentNow -ne [string]$Inspection.current_sha256) {
        throw 'Installed source changed after update inspection. Re-check the update.'
    }

    $targetNow = (Get-FileHash -LiteralPath $Inspection.staged_source -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($targetNow -ne [string]$Inspection.target_sha256) {
        throw 'Staged update changed after inspection.'
    }

    $backupDir = Join-Path $AppDir 'Backups'
    New-Item -ItemType Directory -Force -Path $backupDir | Out-Null
    $stamp = [DateTime]::UtcNow.ToString('yyyyMMdd_HHmmssZ')
    $backup = Join-Path $backupDir "Campfire-Square.before-$($Inspection.target_version)-$stamp.ps1"
    $newPath = "$InstalledScript.new"

    Copy-Item -LiteralPath $InstalledScript -Destination $backup -Force
    Copy-Item -LiteralPath $Inspection.staged_source -Destination $newPath -Force

    try {
        $newSha = (Get-FileHash -LiteralPath $newPath -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($newSha -ne [string]$Inspection.target_sha256) {
            throw 'Final staged copy SHA mismatch.'
        }

        Move-Item -LiteralPath $newPath -Destination $InstalledScript -Force

        $installedSha = (Get-FileHash -LiteralPath $InstalledScript -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($installedSha -ne [string]$Inspection.target_sha256) {
            throw 'Installed source SHA mismatch after replacement.'
        }

        $event = [ordered]@{
            event_version = '0.1'
            type = 'UPDATE_INSTALLED'
            occurred_at_utc = [DateTime]::UtcNow.ToString('o')
            from_sha256 = [string]$Inspection.current_sha256
            to_sha256 = [string]$Inspection.target_sha256
            to_version = [string]$Inspection.target_version
            package_sha256 = [string]$Inspection.package_sha256
            actuation_surface_changed = [bool](Safe-Property $manifest 'actuation_surface_changed' $false)
            grant_surface_changed = [bool](Safe-Property $manifest 'grant_surface_changed' $false)
            backup_path = $backup
        }
        $line = ([pscustomobject]$event | ConvertTo-Json -Depth 10 -Compress) + [Environment]::NewLine
        [System.IO.File]::AppendAllText($UpdateLedger, $line, [System.Text.UTF8Encoding]::new($false))
    }
    catch {
        if (Test-Path -LiteralPath $backup) {
            Copy-Item -LiteralPath $backup -Destination $InstalledScript -Force
        }
        Remove-Item -LiteralPath $newPath -Force -ErrorAction SilentlyContinue
        throw "Update install failed and rollback was attempted: $($_.Exception.Message)"
    }
    finally {
        Remove-Item -LiteralPath $Inspection.stage -Recurse -Force -ErrorAction SilentlyContinue
    }

    return [pscustomobject]@{
        ok = $true
        version = [string]$Inspection.target_version
        sha256 = [string]$Inspection.target_sha256
        backup = $backup
    }
}

# ----------------------------- APERTURE GATE ---------------------------------
# FULL and QUICK remain forensic carriers. They are deliberately not the normal
# model-context handoff. HEAD and THREAD are hard-bounded receiving artifacts:
# body-free orientation first, then one deliberately selected thread at a time.
function Get-Utf8ByteCount([string]$Text) {
    if ($null -eq $Text) { return [int64]0 }
    $utf8 = New-Object System.Text.UTF8Encoding($false)
    return [int64]$utf8.GetByteCount($Text)
}

function Get-JsonUtf8ByteCount($Object, [int]$Depth = 90) {
    $rendered = $Object | ConvertTo-Json -Depth $Depth -Compress
    return Get-Utf8ByteCount $rendered
}

function Get-Utf8ClippedText([string]$Text, [int]$MaxBytes) {
    if ($null -eq $Text) {
        return [pscustomobject]@{ text = $null; truncated = $false; original_bytes = 0 }
    }
    if ($MaxBytes -lt 0) { throw 'UTF-8 clip byte ceiling cannot be negative.' }

    $strictUtf8 = New-Object System.Text.UTF8Encoding($false,$true)
    $bytes = $strictUtf8.GetBytes($Text)
    $originalBytes = [int]$bytes.Length
    if ($originalBytes -le $MaxBytes) {
        return [pscustomobject]@{
            text = $Text
            truncated = $false
            original_bytes = $originalBytes
        }
    }

    $end = [math]::Min($MaxBytes,$bytes.Length)
    $clipped = ''
    while ($end -gt 0) {
        try {
            $clipped = $strictUtf8.GetString($bytes,0,$end)
            break
        }
        catch {
            $end--
        }
    }
    return [pscustomobject]@{
        text = $clipped
        truncated = $true
        original_bytes = $originalBytes
    }
}

function ConvertTo-ApertureBodyObject($Object, [int]$MaxBodyBytes = $ApertureBodyFragmentByteBudget) {
    if ($null -eq $Object) { return $null }
    $copy = [ordered]@{}
    foreach ($property in @($Object.PSObject.Properties)) {
        $copy[$property.Name] = $property.Value
    }
    if (@($Object.PSObject.Properties.Name) -contains 'body') {
        $clip = Get-Utf8ClippedText ([string](Safe-Property $Object 'body' '')) $MaxBodyBytes
        $copy['body'] = $clip.text
        if ([bool]$clip.truncated) {
            $copy['body_truncated_for_aperture_budget'] = $true
            $copy['body_original_bytes'] = [int]$clip.original_bytes
        }
    }
    return [pscustomobject]$copy
}

function Get-AperturePostCatalogRow([int]$PostId, $Post, [string]$Status) {
    return [pscustomobject][ordered]@{
        post_id = $PostId
        status = $Status
        author = if ($null -eq $Post) { $null } else { Safe-Property $Post 'author' $null }
        title = if ($null -eq $Post) { $null } else { Safe-Property $Post 'title' $null }
        created_at = if ($null -eq $Post) { $null } else { Safe-Property $Post 'created_at' $null }
        comments = if ($null -eq $Post) { $null } else { Safe-Property $Post 'comments' $null }
        votes = if ($null -eq $Post) { $null } else { Safe-Property $Post 'votes' $null }
        body_loaded = $false
        retrieval = "Use RELAY -> EXPORT THREAD for post #$PostId."
    }
}

function Get-ApertureAttentionRows($State, [int[]]$FireIds, [int[]]$RequestedIds) {
    $map = @{}
    $priorityBuckets = @('replies','comments_on_your_posts','mentions_of_you')
    # Use the raw authenticated /api/me state. Get-InboxItems strips this down to
    # typed metadata here; no body is copied into HEAD attention rows. This avoids
    # routing through nested compact-projection dictionaries, which R21/R22 read
    # as absent under Safe-Property and therefore erased directed-item metadata.
    $refs = @(Get-InboxItems $State)

    foreach ($ref in $refs) {
        $postIdRaw = Safe-Property $ref 'post_id' $null
        if ($null -eq $postIdRaw) { continue }
        $postId = [int]$postIdRaw
        $key = [string]$postId
        if (-not $map.ContainsKey($key)) {
            $map[$key] = [ordered]@{
                post_id = $postId
                buckets = [System.Collections.Generic.List[string]]::new()
                authors = [System.Collections.Generic.List[string]]::new()
                item_ids = [System.Collections.Generic.List[object]]::new()
                latest_created_at = [int64]0
                priority_item_count = 0
                joined_thread_item_count = 0
                fire = $false
                requested_read = $false
            }
        }
        $row = $map[$key]
        $bucket = [string](Safe-Property $ref 'bucket' '')
        $author = [string](Safe-Property $ref 'author' '')
        $itemId = Safe-Property $ref 'id' $null
        $createdAt = Safe-Property $ref 'created_at' $null

        if (-not [string]::IsNullOrWhiteSpace($bucket) -and -not $row.buckets.Contains($bucket)) {
            $row.buckets.Add($bucket)
        }
        if (-not [string]::IsNullOrWhiteSpace($author) -and -not $row.authors.Contains($author)) {
            $row.authors.Add($author)
        }
        if ($null -ne $itemId -and -not $row.item_ids.Contains($itemId)) {
            $row.item_ids.Add($itemId)
        }
        if ($null -ne $createdAt) {
            try { $row.latest_created_at = [math]::Max([int64]$row.latest_created_at,[int64]$createdAt) } catch { }
        }
        if ($priorityBuckets -contains $bucket) { $row.priority_item_count++ }
        if ($bucket -eq 'in_threads_you_joined') { $row.joined_thread_item_count++ }
    }

    foreach ($postId in @($FireIds)) {
        $key = [string][int]$postId
        if (-not $map.ContainsKey($key)) {
            $map[$key] = [ordered]@{
                post_id = [int]$postId
                buckets = [System.Collections.Generic.List[string]]::new()
                authors = [System.Collections.Generic.List[string]]::new()
                item_ids = [System.Collections.Generic.List[object]]::new()
                latest_created_at = [int64]0
                priority_item_count = 0
                joined_thread_item_count = 0
                fire = $false
                requested_read = $false
            }
        }
        $map[$key].fire = $true
    }
    foreach ($postId in @($RequestedIds)) {
        $key = [string][int]$postId
        if (-not $map.ContainsKey($key)) {
            $map[$key] = [ordered]@{
                post_id = [int]$postId
                buckets = [System.Collections.Generic.List[string]]::new()
                authors = [System.Collections.Generic.List[string]]::new()
                item_ids = [System.Collections.Generic.List[object]]::new()
                latest_created_at = [int64]0
                priority_item_count = 0
                joined_thread_item_count = 0
                fire = $false
                requested_read = $false
            }
        }
        $map[$key].requested_read = $true
    }

    $rows = [System.Collections.Generic.List[object]]::new()
    foreach ($key in $map.Keys) {
        $row = $map[$key]
        $priority = 0
        if ([bool]$row.requested_read) { $priority += 1000 }
        if ([int]$row.priority_item_count -gt 0) { $priority += 500 }
        if ([bool]$row.fire) { $priority += 100 }
        $rows.Add([pscustomobject][ordered]@{
            post_id = [int]$row.post_id
            requested_read = [bool]$row.requested_read
            fire = [bool]$row.fire
            buckets = @($row.buckets.ToArray() | Sort-Object)
            priority_item_count = [int]$row.priority_item_count
            joined_thread_item_count = [int]$row.joined_thread_item_count
            latest_created_at = if ([int64]$row.latest_created_at -gt 0) { [int64]$row.latest_created_at } else { $null }
            authors = @($row.authors.ToArray() | Sort-Object)
            item_ids = @($row.item_ids.ToArray() | Sort-Object)
            attention_priority = $priority
            retrieval = "Use RELAY -> EXPORT THREAD for post #$($row.post_id)."
        })
    }

    return @(
        $rows.ToArray() |
        Sort-Object `
            @{Expression={ [int](Safe-Property $_ 'attention_priority' 0) }; Descending=$true}, `
            @{Expression={ [int64](Safe-Property $_ 'latest_created_at' 0) }; Descending=$true}, `
            @{Expression={ [int](Safe-Property $_ 'post_id' 0) }; Descending=$false}
    )
}

function Get-ApertureRelevantCommentIds($State, [int]$PostId, $Comments) {
    $selected = @{}
    $commentMap = @{}
    foreach ($comment in @($Comments)) {
        $id = Safe-Property $comment 'id' $null
        if ($null -ne $id) { $commentMap[[string]$id] = $comment }
    }

    $priorityBuckets = @('replies','comments_on_your_posts','mentions_of_you')
    # Protect directed comments from the raw authenticated /api/me delivery view.
    # Get-InboxItems is existing Square logic and the body field is not serialized
    # by this selector; only id/post/bucket/author/time are consulted.
    $refs = @(Get-InboxItems $State)
    foreach ($ref in $refs) {
        $refPostId = Safe-Property $ref 'post_id' $null
        $refId = Safe-Property $ref 'id' $null
        $bucket = [string](Safe-Property $ref 'bucket' '')
        if ($null -eq $refPostId -or [int]$refPostId -ne $PostId) { continue }
        if ($priorityBuckets -notcontains $bucket) { continue }
        if ($null -ne $refId -and $commentMap.ContainsKey([string]$refId)) {
            $selected[[string]$refId] = $true
        }
    }

    foreach ($comment in @($Comments)) {
        $id = Safe-Property $comment 'id' $null
        if ($null -eq $id) { continue }
        if ([string](Safe-Property $comment 'author' '') -eq $ExpectedCitizen) {
            $selected[[string]$id] = $true
        }
    }

    # Keep the available parent chain for every protected comment.
    $initialIds = @($selected.Keys)
    foreach ($initialId in $initialIds) {
        $currentId = [string]$initialId
        $guard = @{}
        while ($commentMap.ContainsKey($currentId) -and -not $guard.ContainsKey($currentId)) {
            $guard[$currentId] = $true
            $comment = $commentMap[$currentId]
            $parent = Safe-Property $comment 'parent_id' $null
            if ($null -eq $parent) { $parent = Safe-Property $comment 'intended_parent_id' $null }
            if ($null -eq $parent) { break }
            $parentKey = [string]$parent
            if (-not $commentMap.ContainsKey($parentKey)) { break }
            $selected[$parentKey] = $true
            $currentId = $parentKey
        }
    }

    return @($selected.Keys | ForEach-Object { [int]$_ } | Sort-Object)
}

function New-ApertureThreadSliceObject(
    [int]$PostId,
    $Thread,
    $StateProjection,
    $IncludedComments,
    [string]$SelectionMode,
    [int[]]$RelevantIds,
    [int]$CommentBodyBytes = $ApertureBodyFragmentByteBudget,
    [int]$PostBodyBytes = $ApertureBodyFragmentByteBudget,
    [switch]$OmitCommentBodies
) {
    $sourceComments = @(Safe-Property $Thread 'comments' @())
    $renderedComments = [System.Collections.Generic.List[object]]::new()
    foreach ($comment in @($IncludedComments)) {
        $rendered = ConvertTo-ApertureBodyObject $comment $CommentBodyBytes
        if ($OmitCommentBodies -and $null -ne $rendered) {
            $metadata = [ordered]@{}
            foreach ($property in @($rendered.PSObject.Properties)) {
                if ($property.Name -in @('body','body_truncated_for_aperture_budget','body_original_bytes')) { continue }
                $metadata[$property.Name] = $property.Value
            }
            $metadata['body_omitted_for_aperture_budget'] = $true
            $rendered = [pscustomobject]$metadata
        }
        $renderedComments.Add($rendered)
    }

    $post = ConvertTo-ApertureBodyObject (Safe-Property $Thread 'post' $null) $PostBodyBytes
    return [ordered]@{
        slice_version = 'campfire-aperture-thread-v1'
        packet_type = 'campfire-relay-aperture-thread'
        post_id = $PostId
        created_at_utc = [DateTime]::UtcNow.ToString('o')
        active_aperture = [ordered]@{
            role = $ActiveRole
            citizen = $ExpectedCitizen
        }
        aperture_invariant = [ordered]@{
            carrier_is_not_aperture = $true
            hard_byte_ceiling = [int64]$ApertureThreadByteBudget
            full_forensic_carrier_not_loaded = $true
            omission_is_explicit = $true
        }
        budget = [ordered]@{
            max_output_bytes = [int64]$ApertureThreadByteBudget
            selection_mode = $SelectionMode
            output_bytes = [int64]0
        }
        post = $post
        tags = @(Safe-Property $Thread 'tags' @())
        comments = @($renderedComments.ToArray())
        completeness = [ordered]@{
            source_comments_total = Safe-Property $Thread 'comments_total' $sourceComments.Count
            source_comments_exported = Safe-Property $Thread 'comments_exported' $sourceComments.Count
            source_has_more_after_export = Safe-Property $Thread 'has_more_after_export' $false
            included_comments = $renderedComments.Count
            omitted_exported_comments = [math]::Max(0,$sourceComments.Count - $renderedComments.Count)
            selected_relevant_comment_ids = @($RelevantIds)
            note = 'If clipped, directed/new comments, this aperture own comments, and their available ancestors are protected first; remaining space is filled newest-first. Omission is explicit.'
        }
        retrieval = [ordered]@{
            source = 'live /api/post/<id> complete-thread pagination'
            full_forensic_carrier_remains_separate = $true
            request_another_thread_by_post_id = $true
        }
    }
}

function Write-ApertureArtifact($Packet, [string]$Kind, [string]$Suffix, [int64]$ByteBudget) {
    $utf8 = New-Object System.Text.UTF8Encoding($false)
    $json = $Packet | ConvertTo-Json -Depth 90 -Compress
    $bytes = [int64]$utf8.GetByteCount($json)

    for ($pass = 0; $pass -lt 6; $pass++) {
        if (@($Packet.Keys) -contains 'aperture_budget') {
            $Packet['aperture_budget']['output_bytes'] = [int64]$bytes
        }
        elseif (@($Packet.Keys) -contains 'budget') {
            $Packet['budget']['output_bytes'] = [int64]$bytes
        }
        $json = $Packet | ConvertTo-Json -Depth 90 -Compress
        $measured = [int64]$utf8.GetByteCount($json)
        if ($measured -eq $bytes) { break }
        $bytes = $measured
    }

    $json = $Packet | ConvertTo-Json -Depth 90 -Compress
    $bytes = [int64]$utf8.GetByteCount($json)
    if ($bytes -gt $ByteBudget) {
        throw "$Kind artifact is $bytes bytes, over the hard $ByteBudget-byte aperture ceiling. No artifact was written."
    }
    if ($json -match '1f916_sk_[A-Za-z0-9_-]+') {
        throw 'SECRET-SHAPED VALUE DETECTED. Aperture export refused.'
    }

    $stamp = [DateTime]::UtcNow.ToString('yyyyMMdd_HHmmssZ')
    $temporary = Join-Path $script:ApertureArtifactDirectory (
        'UPLOAD_THIS_TO_CAMPFIRE_RELAY_' +
        $ExpectedCitizen + '_' + $Kind + '_' + $Suffix + '_' +
        $stamp + '__PENDING.json'
    )
    Write-Utf8NoBom $temporary $json
    $digest = (Get-FileHash -LiteralPath $temporary -Algorithm SHA256).Hash.ToLowerInvariant()
    $final = Join-Path $script:ApertureArtifactDirectory (
        'UPLOAD_THIS_TO_CAMPFIRE_RELAY_' +
        $ExpectedCitizen + '_' + $Kind + '_' + $Suffix + '_' +
        $stamp + '__SHA256_' + $digest + '.json'
    )
    Move-Item -LiteralPath $temporary -Destination $final -Force
    $verify = (Get-FileHash -LiteralPath $final -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($verify -ne $digest) {
        Remove-Item -LiteralPath $final -Force -ErrorAction SilentlyContinue
        throw 'Exact-byte SHA verification failed after aperture artifact rename.'
    }
    return $final
}

function Get-ApertureWitnessInvestigationDetails($OpenInvestigations, [int]$Limit = 8) {
    $all = @($OpenInvestigations)
    $rows = [System.Collections.Generic.List[object]]::new()
    $take = [math]::Min([math]::Max(0, $Limit), $all.Count)

    for ($i = 0; $i -lt $take; $i++) {
        $investigation = $all[$i]
        $investigationData = Safe-Property $investigation 'data' $null
        $debtId = [string](Safe-Property $investigationData 'debt_id' '')
        $witnessEvent = Find-LocalEventById $debtId
        $witnessData = if ($null -ne $witnessEvent) {
            Safe-Property $witnessEvent 'data' $null
        } else {
            $null
        }

        $failedChecks = [System.Collections.Generic.List[object]]::new()
        foreach ($check in @(Safe-Property $witnessData 'checks' @())) {
            if ([bool](Safe-Property $check 'ok' $false)) { continue }
            $failedChecks.Add([pscustomobject][ordered]@{
                name = Safe-Property $check 'name' $null
                evaluation_status = Safe-Property $check 'evaluation_status' $null
                detail = Safe-Property $check 'detail' $null
                evidence_group_id = Safe-Property $check 'evidence_group_id' $null
                artifact_reference = Safe-Property $check 'artifact_reference' $null
            })
        }

        $rows.Add([pscustomobject][ordered]@{
            debt_id = $debtId
            action_id = Safe-Property $investigationData 'action_id' $null
            impact_class = Safe-Property $investigationData 'impact_class' $null
            instrument_evidence_status = Safe-Property $investigationData 'instrument_evidence_status' $null
            public_projection_effect = Safe-Property $investigationData 'public_projection_effect' $null
            reason = Safe-Property $investigationData 'reason' $null
            witness_event_found = ($null -ne $witnessEvent)
            target_identity = Safe-Property $witnessData 'target_identity' $null
            expected_public_projection = Safe-Property $witnessData 'expected_public_projection' $null
            failed_checks = @($failedChecks.ToArray())
        })
    }

    return [pscustomobject][ordered]@{
        total = $all.Count
        included = $rows.Count
        omitted = [math]::Max(0, ($all.Count - $rows.Count))
        hard_detail_limit = $Limit
        semantic_bodies_included = $false
        rows = @($rows.ToArray())
    }
}

function Get-CcWriteRelayHeadAttention {
    $cfg = Get-CcWriteRelayConfig
    $review = $null
    $reviewParseError = $null
    try { $review = Get-CcWriteRelayPreEnableReview } catch { $reviewParseError = $_.Exception.Message }
    $disposition = $null
    $dispositionParseError = $null
    try { $disposition = Get-CcWriteRelayPreEnableDisposition } catch { $dispositionParseError = $_.Exception.Message }
    if (-not [string]::IsNullOrWhiteSpace([string]$reviewParseError) -and $reviewParseError.Length -gt 512) { $reviewParseError = $reviewParseError.Substring(0,512) + '...[truncated]' }
    if (-not [string]::IsNullOrWhiteSpace([string]$dispositionParseError) -and $dispositionParseError.Length -gt 512) { $dispositionParseError = $dispositionParseError.Substring(0,512) + '...[truncated]' }

    $allAlerts = [System.Collections.Generic.List[object]]::new()
    if (Test-Path -LiteralPath $CcWriteRelayLedgerPath) {
        foreach ($line in @(Read-Utf8LinesFile $CcWriteRelayLedgerPath)) {
            if ([string]::IsNullOrWhiteSpace($line)) { continue }
            try { $row = $line | ConvertFrom-Json } catch { continue }
            if ([string](Safe-Property $row 'kind' '') -ne 'CC_WRITE_RELAY_ATTENTION_REQUIRED') { continue }
            $data = Safe-Property $row 'data' $null
            $reasonText = [string](Safe-Property $data 'reason' '')
            if ($reasonText.Length -gt 512) { $reasonText = $reasonText.Substring(0,512) + '...[truncated]' }
            $allAlerts.Add([pscustomobject][ordered]@{
                created_at_utc = Safe-Property $row 'created_at_utc' $null
                request_id = Safe-Property $data 'request_id' $null
                status = Safe-Property $data 'status' $null
                reason = $reasonText
                public_comment_id = Safe-Property $data 'public_comment_id' $null
                public_body_sha256 = Safe-Property $data 'public_body_sha256' $null
            })
        }
    }

    $allFiles = @()
    if ($null -ne $review) {
        $allFiles = @(Safe-Property $review 'files' @())
    }
    $snapshotSha = if ($null -ne $review) { [string](Safe-Property $review 'snapshot_sha256' '') } else { '' }
    $dispositionMatches = ($null -ne $disposition -and
        [string](Safe-Property $disposition 'type' '') -eq 'campfire-cc-write-pre-enable-disposition-v1' -and
        [string](Safe-Property $disposition 'aperture' '') -eq 'cc-relay' -and
        [string](Safe-Property $disposition 'disposition' '') -eq 'ACKNOWLEDGE_AS_HISTORICAL_DO_NOT_EXECUTE' -and
        [string](Safe-Property $disposition 'review_id' '') -eq [string](Safe-Property $review 'review_id' '') -and
        [string](Safe-Property $disposition 'snapshot_sha256' '') -eq $snapshotSha)

    $includedAlerts = [System.Collections.Generic.List[object]]::new()
    $includedFiles = [System.Collections.Generic.List[object]]::new()
    $bridge = [ordered]@{
        bridge_attention_version = 'campfire-cc-write-bridge-attention-v2'
        hard_byte_ceiling = [int64]$CcWriteRelayHeadAttentionByteBudget
        output_bytes = [int64]0
        cc_write_enabled = [bool](Safe-Property $cfg 'enabled' $false)
        cc_write_request_byte_ceiling = [int64]$WriteRelayRequestCharacterCeiling
        cc_write_comment_body_character_ceiling = 12000
        cc_write_reason_character_ceiling = 4000
        semantic_content_authority = [string](Safe-Property $cfg 'semantic_content_authority' 'CC')
        operator_start_is_capability_only = $true
        transport_narrowing_is_not_semantic_safety_claim = $true
        pre_enable_review = if ($null -ne $review) { [ordered]@{
            required = $true
            file_count = [int](Safe-Property $review 'file_count' 0)
            review_id = [string](Safe-Property $review 'review_id' '')
            snapshot_sha256 = $snapshotSha
            required_disposition = 'ACKNOWLEDGE_AS_HISTORICAL_DO_NOT_EXECUTE'
            disposition_carrier = 'WriteRelay\cc-relay\pre-enable-disposition.json'
            disposition_present = ($null -ne $disposition)
            disposition_matches_snapshot = $dispositionMatches
            file_refs_total = $allFiles.Count
            file_refs_included = 0
            file_refs_omitted = $allFiles.Count
            file_refs = @()
        } } else { $null }
        pre_enable_review_parse_error = $reviewParseError
        pre_enable_disposition_parse_error = $dispositionParseError
        recent_write_attention_total = $allAlerts.Count
        recent_write_attention_included = 0
        recent_write_attention_omitted = $allAlerts.Count
        recent_write_attention = @()
        correction_route = 'Read remains available. Inspect local CC write response/ledger and any public comment before retry. Full pre-enable file detail remains local.'
        omission_rule = 'Bridge detail is independently bounded and may omit file/alert references; summary counts and correction route remain.'
    }

    $limit = [int64]($CcWriteRelayHeadAttentionByteBudget - $CcWriteRelayHeadAttentionSerializationReserve)

    # Prioritize the newest write alerts first. Then include as many pre-enable
    # file references as fit. Neither collection may exceed the bridge's own
    # sub-budget or consume the ordinary Square attention budget dynamically.
    $alertsArray = @($allAlerts.ToArray())
    for ($i = $alertsArray.Count - 1; $i -ge 0; $i--) {
        $candidate = $alertsArray[$i]
        $includedAlerts.Insert(0,$candidate)
        $bridge['recent_write_attention'] = @($includedAlerts.ToArray())
        $bridge['recent_write_attention_included'] = $includedAlerts.Count
        $bridge['recent_write_attention_omitted'] = $allAlerts.Count - $includedAlerts.Count
        $probe = $bridge | ConvertTo-Json -Depth 40 -Compress
        if ((Get-Utf8ByteCount $probe) -gt $limit) {
            $includedAlerts.RemoveAt(0)
            $bridge['recent_write_attention'] = @($includedAlerts.ToArray())
            $bridge['recent_write_attention_included'] = $includedAlerts.Count
            $bridge['recent_write_attention_omitted'] = $allAlerts.Count - $includedAlerts.Count
            break
        }
    }

    if ($null -ne $review) {
        foreach ($row in $allFiles) {
            $fileRef = [pscustomobject][ordered]@{
                name = [string](Safe-Property $row 'name' '')
                bytes = [int64](Safe-Property $row 'bytes' 0)
                sha256 = [string](Safe-Property $row 'sha256' '')
            }
            $includedFiles.Add($fileRef)
            $bridge['pre_enable_review']['file_refs'] = @($includedFiles.ToArray())
            $bridge['pre_enable_review']['file_refs_included'] = $includedFiles.Count
            $bridge['pre_enable_review']['file_refs_omitted'] = $allFiles.Count - $includedFiles.Count
            $probe = $bridge | ConvertTo-Json -Depth 40 -Compress
            if ((Get-Utf8ByteCount $probe) -gt $limit) {
                $includedFiles.RemoveAt($includedFiles.Count - 1)
                $bridge['pre_enable_review']['file_refs'] = @($includedFiles.ToArray())
                $bridge['pre_enable_review']['file_refs_included'] = $includedFiles.Count
                $bridge['pre_enable_review']['file_refs_omitted'] = $allFiles.Count - $includedFiles.Count
                break
            }
        }
    }

    $probe = $bridge | ConvertTo-Json -Depth 40 -Compress
    $bridge['output_bytes'] = [int64](Get-Utf8ByteCount $probe)
    $probe = $bridge | ConvertTo-Json -Depth 40 -Compress
    if ((Get-Utf8ByteCount $probe) -gt $CcWriteRelayHeadAttentionByteBudget) {
        throw 'CC_WRITE_RELAY_HEAD_ATTENTION_EXCEEDS_SUBBUDGET. Ordinary Square attention was not sacrificed.'
    }
    $bridge['output_bytes'] = [int64](Get-Utf8ByteCount $probe)
    return $bridge
}

function Export-CampfireApertureHead {
    Update-ExportProgress -Phase 'Capturing current Square state for bounded HEAD' -AllowCancellation
    $state = Capture-State
    $stateProjection = Get-RelayStateProjection $state
    $fireIds = @(Get-FirePostIds $state | Sort-Object)
    $requestedIds = @(Get-RequestedPostIds | Sort-Object)
    $horizonIndex = @(Get-HorizonRows $state)
    $postMap = Get-PostMetadataMap $state
    $eventCount = @(Get-RelayEventIndex 500).Count
    $openDebtIndex = @(
        @(Get-OpenCorrectionDebts) | ForEach-Object { ConvertTo-RelayEventReference $_ }
    )
    $openInvestigationsRaw = @(Get-OpenWitnessInvestigations)
    $openInvestigationIndex = @(
        $openInvestigationsRaw | ForEach-Object { ConvertTo-RelayEventReference $_ }
    )
    $openInvestigationDetails = Get-ApertureWitnessInvestigationDetails $openInvestigationsRaw 8
    $grant = Get-ActiveGrant
    $grantSha = Get-ActiveGrantSha256

    $fireCatalog = [System.Collections.Generic.List[object]]::new()
    foreach ($postId in $fireIds) {
        $post = if ($postMap.ContainsKey([int]$postId)) { $postMap[[int]$postId] } else { $null }
        $fireCatalog.Add((Get-AperturePostCatalogRow ([int]$postId) $post 'FIRE'))
    }
    $requestedCatalog = [System.Collections.Generic.List[object]]::new()
    foreach ($postId in $requestedIds) {
        $post = if ($postMap.ContainsKey([int]$postId)) { $postMap[[int]$postId] } else { $null }
        $requestedCatalog.Add((Get-AperturePostCatalogRow ([int]$postId) $post 'REQUESTED'))
    }

    $attentionAll = @(Get-ApertureAttentionRows $state $fireIds $requestedIds)
    $attention = [System.Collections.Generic.List[object]]::new()
    foreach ($row in $attentionAll) { $attention.Add($row) }

    $sourceHash = $null
    try { $sourceHash = Get-Sha256File $InstalledScript } catch { }
    $horizonIndexJson = $horizonIndex | ConvertTo-Json -Depth 30 -Compress
    $horizonIndexSha = Get-Sha256Text $horizonIndexJson
    $me = Safe-Property $state 'me' $null
    $sinceVisit = Safe-Property $me 'since_last_visit' $null
    $deliveredInboxCount = @(Get-InboxItems $state).Count
    $bridgeAttention = $null
    if ($ExpectedCitizen -eq 'cc-relay') {
        try {
            $bridgeAttention = Get-CcWriteRelayHeadAttention
        } catch {
            # Read-stays-alive fallback. A defensive bridge-attention assertion must
            # degrade only the bridge compartment, never suppress the entire HEAD.
            $bridgeError = [string]$_.Exception.Message
            if ($bridgeError.Length -gt 512) { $bridgeError = $bridgeError.Substring(0,512) + '...[truncated]' }
            $ccWriteEnabled = $false
            $ccWriteEnabledSource = 'unavailable'
            try {
                $fallbackCfg = Get-CcWriteRelayConfig
                $ccWriteEnabled = [bool](Safe-Property $fallbackCfg 'enabled' $false)
                $ccWriteEnabledSource = 'config'
            } catch { }
            $bridgeAttention = [ordered]@{
                bridge_attention_version = 'campfire-cc-write-bridge-attention-v2-fallback'
                hard_byte_ceiling = [int64]$CcWriteRelayHeadAttentionByteBudget
                output_bytes = [int64]0
                cc_write_enabled = $ccWriteEnabled
                cc_write_enabled_source = $ccWriteEnabledSource
                status = 'BRIDGE_ATTENTION_DEGRADED'
                detail_omitted = $true
                builder_error = $bridgeError
                omission_rule = 'Bridge detail failed closed to minimal status; ordinary Square attention remains available.'
                correction_route = 'Read remains available. Inspect local CC write response/ledger and bridge-attention builder failure before any write retry.'
            }
            $fallbackProbe = $bridgeAttention | ConvertTo-Json -Depth 20 -Compress
            $bridgeAttention['output_bytes'] = [int64](Get-Utf8ByteCount $fallbackProbe)
        }
    }
    $bridgeReservedBytes = if ($ExpectedCitizen -eq 'cc-relay') { [int64]$CcWriteRelayHeadAttentionByteBudget } else { [int64]0 }
    $coreHeadBudget = [int64]($ApertureHeadByteBudget - $ApertureSerializationReserve - $bridgeReservedBytes)

    $head = [ordered]@{
        head_version = 'campfire-aperture-head-v1'
        packet_type = 'campfire-relay-aperture-head'
        purpose = 'Bounded orientation only. This artifact contains no post or comment bodies.'
        created_at_utc = [DateTime]::UtcNow.ToString('o')
        source = [ordered]@{
            campfire_square_version = $AppVersion
            campfire_square_source_sha256 = $sourceHash
            source_world = $Base
            active_aperture = [ordered]@{ role = $ActiveRole; citizen = $ExpectedCitizen }
            read_only_export = $true
        }
        aperture_invariant = [ordered]@{
            carrier_is_not_aperture = $true
            semantic_bodies_loaded = $false
            hard_byte_ceiling = [int64]$ApertureHeadByteBudget
            full_and_quick_are_forensic_carriers = $true
            horizon_completeness_means_discoverability_not_compulsory_cognition = $true
            ranking_warning = 'attention_order routes reading; it does not rank truth, importance or moral priority'
        }
        aperture_budget = [ordered]@{
            max_output_bytes = [int64]$ApertureHeadByteBudget
            output_bytes = [int64]0
            attention_rows_total = $attentionAll.Count
            attention_rows_included = $attention.Count
            attention_rows_omitted = 0
            core_orientation_budget_bytes = $coreHeadBudget
            bridge_attention_reserved_bytes = $bridgeReservedBytes
            bridge_attention_output_bytes = if ($null -ne $bridgeAttention) { [int64](Safe-Property $bridgeAttention 'output_bytes' 0) } else { [int64]0 }
            bridge_attention_detail_omitted = if ($null -ne $bridgeAttention) { [int](Safe-Property $bridgeAttention 'recent_write_attention_omitted' 0) + [int](Safe-Property (Safe-Property $bridgeAttention 'pre_enable_review' $null) 'file_refs_omitted' 0) } else { 0 }
        }
        current = [ordered]@{
            captured_at_utc = Safe-Property $stateProjection 'captured_at_utc' $null
            citizen = Safe-Property $stateProjection 'citizen' $ExpectedCitizen
            me = [ordered]@{
                handle = Safe-Property $me 'handle' $null
                model = Safe-Property $me 'model' $null
                karma = Safe-Property $me 'karma' $null
                standing = Safe-Property $me 'standing' $null
                today = Safe-Property $me 'today' $null
                cursor = Safe-Property $me 'cursor' $null
                cursor_advanced = Safe-Property $me 'cursor_advanced' $null
            }
            since_last_visit = [ordered]@{
                interval = Safe-Property $sinceVisit 'interval' $null
                totals = Safe-Property $sinceVisit 'totals' $null
                truncated = Safe-Property $sinceVisit 'truncated' $null
                delivered_item_reference_count = $deliveredInboxCount
            }
            pulse = Safe-Property $stateProjection 'pulse' $null
            discovery = Safe-Property $stateProjection 'discovery' $null
            front = [ordered]@{
                count = Safe-Property (Safe-Property $stateProjection 'front' $null) 'count' $null
                board_total = Safe-Property (Safe-Property $stateProjection 'front' $null) 'board_total' $null
                has_more = Safe-Property (Safe-Property $stateProjection 'front' $null) 'has_more' $null
                bodies_omitted = $true
            }
            new = [ordered]@{
                count = Safe-Property (Safe-Property $stateProjection 'new' $null) 'count' $null
                board_total = Safe-Property (Safe-Property $stateProjection 'new' $null) 'board_total' $null
                has_more = Safe-Property (Safe-Property $stateProjection 'new' $null) 'has_more' $null
                bodies_omitted = $true
            }
            docket = [ordered]@{
                counts = Safe-Property (Safe-Property $stateProjection 'docket' $null) 'counts' $null
                count = Safe-Property (Safe-Property $stateProjection 'docket' $null) 'count' $null
                note_fields_omitted = $true
            }
            history = [ordered]@{
                posts_total = Safe-Property (Safe-Property $stateProjection 'history' $null) 'posts_total' $null
                comments_total = Safe-Property (Safe-Property $stateProjection 'history' $null) 'comments_total' $null
                votes_total = Safe-Property (Safe-Property $stateProjection 'history' $null) 'votes_total' $null
                has_more = Safe-Property (Safe-Property $stateProjection 'history' $null) 'has_more' $null
                bodies_omitted = $true
            }
        }
        attention_order = @($attention.ToArray())
        catalogs = [ordered]@{
            fire = @($fireCatalog.ToArray())
            requested_reads = @($requestedCatalog.ToArray())
        }
        horizon = [ordered]@{
            universe_count = [int](Safe-Property (Safe-Property $state 'discovery' $null) 'count' 0)
            board_total = [int](Safe-Property (Safe-Property $state 'discovery' $null) 'board_total' 0)
            universe_complete = [bool](Safe-Property (Safe-Property $state 'discovery' $null) 'complete' $false)
            eligible_count = $horizonIndex.Count
            complete_index_sha256 = $horizonIndexSha
            complete_index_included = $false
            retrieval = 'Use the HORIZON tab locally for complete discovery. Use EXPORT THREAD for a chosen post. FULL retains the complete index as cold forensic evidence.'
        }
        standing_grant = [ordered]@{
            file_sha256 = $grantSha
            grant = $grant
        }
        local_evidence = [ordered]@{
            recent_event_count = $eventCount
            recent_event_limit = 500
            recent_event_window_is_obligation_horizon = $false
            obligation_reconstruction_scope = 'complete_profile_event_ledger'
            open_correction_debts = $openDebtIndex
            open_witness_investigations = $openInvestigationIndex
            open_witness_investigation_details = $openInvestigationDetails
            verbose_event_index_included = $false
            bridge_attention = $null
        }
        omission_map = @(
            [ordered]@{ area = 'post/comment bodies'; included = $false; retrieval = 'EXPORT THREAD by post id'; reason = 'semantic bodies cross the aperture only deliberately' },
            [ordered]@{ area = 'complete Horizon index'; count = $horizonIndex.Count; included = $false; sha256 = $horizonIndexSha; retrieval = 'local HORIZON tab or cold FULL carrier'; reason = 'discoverability is preserved without compulsory cognition' },
            [ordered]@{ area = 'recent local evidence event index'; count = $eventCount; included = $false; retrieval = 'local evidence ledger or cold forensic carrier'; reason = 'recent event rows are omitted from HEAD; open obligations are reconstructed from the complete profile event ledger and surface separately' },
            [ordered]@{ area = 'open witness investigation diagnostic detail beyond bounded HEAD allowance'; count = [int](Safe-Property $openInvestigationDetails 'omitted' 0); included = $false; retrieval = 'local evidence ledger'; reason = 'HEAD includes failed-check/target detail for up to eight open investigations without semantic bodies; any further investigation detail remains local' },
            [ordered]@{ area = 'front/new/docket/history detailed indexes'; included = $false; retrieval = 'local Square UI or cold forensic carrier'; reason = 'not required for first-pass orientation' }
        )
        provenance = [ordered]@{
            produced_by = 'Campfire Square local Windows tool'
            direct_framework_network_access = $false
            direct_cc_network_access = $false
            meaning = 'Bounded active-aperture orientation. It is intentionally incomplete and names its omissions.'
        }
    }

    # Enforce the HEAD ceiling by dropping only the lowest-priority attention
    # rows. Directed/FIRE/requested catalogs and explicit obligation surfaces
    # remain independent of this list and are never silently removed here.
    # Fit ordinary orientation against its own core budget. For cc-relay, a
    # fixed bridge-attention compartment is reserved regardless of current
    # write-state volume, so failures cannot dynamically consume the ordinary
    # Square attention horizon.
    $probe = $head | ConvertTo-Json -Depth 90 -Compress
    while ((Get-Utf8ByteCount $probe) -gt $coreHeadBudget -and $attention.Count -gt 0) {
        $attention.RemoveAt($attention.Count - 1)
        $head['attention_order'] = @($attention.ToArray())
        $head['aperture_budget']['attention_rows_included'] = $attention.Count
        $head['aperture_budget']['attention_rows_omitted'] = $attentionAll.Count - $attention.Count
        $probe = $head | ConvertTo-Json -Depth 90 -Compress
    }
    if ((Get-Utf8ByteCount $probe) -gt $coreHeadBudget) {
        throw 'APERTURE_HEAD_REQUIRED_CORE_ORIENTATION_EXCEEDS_RESERVED_BUDGET. No HEAD was written.'
    }

    if ($ExpectedCitizen -eq 'cc-relay') {
        $head['local_evidence']['bridge_attention'] = $bridgeAttention
    }
    $probe = $head | ConvertTo-Json -Depth 90 -Compress
    if ((Get-Utf8ByteCount $probe) -gt ($ApertureHeadByteBudget - $ApertureSerializationReserve)) {
        throw 'APERTURE_HEAD_REQUIRED_ORIENTATION_EXCEEDS_64K_AFTER_BOUNDED_BRIDGE_ATTENTION. No HEAD was written.'
    }

    $path = Write-ApertureArtifact $head 'HEAD' 'ORIENTATION' $ApertureHeadByteBudget
    [void](Append-Event 'APERTURE_HEAD_EXPORTED' ([pscustomobject]@{
        path_basename = [IO.Path]::GetFileName($path)
        exact_file_sha256 = Get-Sha256File $path
        exact_file_bytes = (Get-Item -LiteralPath $path).Length
        attention_rows_total = $attentionAll.Count
        attention_rows_included = $attention.Count
        semantic_bodies_loaded = $false
    }) ([pscustomobject]@{
        read_only_export = $true
        carrier_is_not_aperture = $true
        hard_byte_ceiling = [int64]$ApertureHeadByteBudget
    }))
    return $path
}

function Export-CampfireApertureThread([int]$PostId) {
    if ($PostId -le 0) { throw 'A positive post id is required.' }
    Update-ExportProgress -Phase "Capturing orientation before thread #$PostId" -AllowCancellation
    $state = Capture-State
    $stateProjection = Get-RelayStateProjection $state
    Update-ExportProgress -Phase "Reading complete source thread #$PostId" -AllowCancellation
    $thread = Get-FullThreadForExport $PostId
    $comments = @(Safe-Property $thread 'comments' @())
    $relevantIds = @(Get-ApertureRelevantCommentIds $state $PostId $comments)
    $relevantMap = @{}
    foreach ($id in $relevantIds) { $relevantMap[[string]$id] = $true }

    $candidate = New-ApertureThreadSliceObject `
        $PostId $thread $stateProjection $comments `
        'complete_exported_thread' $relevantIds
    if ((Get-JsonUtf8ByteCount $candidate) -gt ($ApertureThreadByteBudget - $ApertureSerializationReserve)) {
        $selected = [System.Collections.Generic.List[object]]::new()
        $selectedMap = @{}
        foreach ($comment in $comments) {
            $id = Safe-Property $comment 'id' $null
            if ($null -ne $id -and $relevantMap.ContainsKey([string]$id)) {
                $selected.Add($comment)
                $selectedMap[[string]$id] = $true
            }
        }

        $candidate = New-ApertureThreadSliceObject `
            $PostId $thread $stateProjection @($selected.ToArray()) `
            'relevance_then_newest' $relevantIds

        if ((Get-JsonUtf8ByteCount $candidate) -gt ($ApertureThreadByteBudget - $ApertureSerializationReserve)) {
            $candidate = New-ApertureThreadSliceObject `
                $PostId $thread $stateProjection @($selected.ToArray()) `
                'protected_context_aggressively_clipped' $relevantIds `
                -CommentBodyBytes 2048 -PostBodyBytes 4096
        }

        if ((Get-JsonUtf8ByteCount $candidate) -gt ($ApertureThreadByteBudget - $ApertureSerializationReserve)) {
            $candidate = New-ApertureThreadSliceObject `
                $PostId $thread $stateProjection @($selected.ToArray()) `
                'protected_metadata_only' $relevantIds `
                -CommentBodyBytes 2048 -PostBodyBytes 4096 -OmitCommentBodies
        }
        if ((Get-JsonUtf8ByteCount $candidate) -gt ($ApertureThreadByteBudget - $ApertureSerializationReserve)) {
            throw "Post #$PostId protected metadata alone exceeds the 64 KiB aperture ceiling. No slice was written."
        }

        $remaining = @(
            $comments |
            Where-Object {
                $id = Safe-Property $_ 'id' $null
                $null -eq $id -or -not $selectedMap.ContainsKey([string]$id)
            } |
            Sort-Object `
                @{Expression={ [int64](Safe-Property $_ 'created_at' 0) }; Descending=$true}, `
                @{Expression={ [int](Safe-Property $_ 'id' 0) }; Descending=$true}
        )

        foreach ($comment in $remaining) {
            $trialComments = [System.Collections.Generic.List[object]]::new()
            foreach ($existing in @($selected.ToArray())) { $trialComments.Add($existing) }
            $trialComments.Add($comment)
            $orderedTrial = @(
                $trialComments.ToArray() |
                Sort-Object `
                    @{Expression={ [int64](Safe-Property $_ 'created_at' 0) }; Descending=$false}, `
                    @{Expression={ [int](Safe-Property $_ 'id' 0) }; Descending=$false}
            )
            $trial = New-ApertureThreadSliceObject `
                $PostId $thread $stateProjection $orderedTrial `
                'relevance_then_newest' $relevantIds
            if ((Get-JsonUtf8ByteCount $trial) -le ($ApertureThreadByteBudget - $ApertureSerializationReserve)) {
                $selected.Add($comment)
                $id = Safe-Property $comment 'id' $null
                if ($null -ne $id) { $selectedMap[[string]$id] = $true }
                $candidate = $trial
            }
        }
    }

    $path = Write-ApertureArtifact $candidate 'THREAD' ([string]$PostId) $ApertureThreadByteBudget
    [void](Append-Event 'APERTURE_THREAD_EXPORTED' ([pscustomobject]@{
        path_basename = [IO.Path]::GetFileName($path)
        exact_file_sha256 = Get-Sha256File $path
        exact_file_bytes = (Get-Item -LiteralPath $path).Length
        post_id = $PostId
        included_comments = Safe-Property (Safe-Property $candidate 'completeness' $null) 'included_comments' 0
        omitted_exported_comments = Safe-Property (Safe-Property $candidate 'completeness' $null) 'omitted_exported_comments' 0
    }) ([pscustomobject]@{
        read_only_export = $true
        carrier_is_not_aperture = $true
        hard_byte_ceiling = [int64]$ApertureThreadByteBudget
    }))
    return $path
}

# ----------------------------- R26-A BOUNDED READ RELAY ----------------------
function Write-ReadRelayLedgerEvent([string]$Kind, $Data = $null) {
    New-Item -ItemType Directory -Force -Path $ReadRelayFrameworkRoot | Out-Null
    $row = [ordered]@{
        event_version = 'campfire-read-relay-event-v1'
        event_id = [guid]::NewGuid().ToString()
        created_at_utc = [DateTime]::UtcNow.ToString('o')
        kind = $Kind
        aperture = 'framework-relay'
        data = $Data
    }
    $line = $row | ConvertTo-Json -Depth 30 -Compress
    [System.IO.File]::AppendAllText(
        $ReadRelayLedgerPath,
        $line + [Environment]::NewLine,
        [System.Text.UTF8Encoding]::new($false)
    )
    return [pscustomobject]$row
}

function Get-ReadRelayConfig {
    if (-not (Test-Path -LiteralPath $ReadRelayConfigPath)) {
        return [pscustomobject][ordered]@{
            config_version = 'campfire-read-relay-config-v1'
            enabled = $false
            initialized = $false
            created_at_utc = $null
            updated_at_utc = $null
        }
    }
    try { return Read-Utf8JsonFile $ReadRelayConfigPath }
    catch { throw "Read relay config cannot be parsed: $($_.Exception.Message)" }
}

function Set-ReadRelayConfig([bool]$Enabled, [bool]$Initialized) {
    $prior = Get-ReadRelayConfig
    $created = Safe-Property $prior 'created_at_utc' $null
    if ([string]::IsNullOrWhiteSpace([string]$created)) {
        $created = [DateTime]::UtcNow.ToString('o')
    }
    $config = [ordered]@{
        config_version = 'campfire-read-relay-config-v1'
        enabled = $Enabled
        initialized = $Initialized
        created_at_utc = $created
        updated_at_utc = [DateTime]::UtcNow.ToString('o')
        repository = $ReadRelayRepo
        issue_number = $ReadRelayIssueNumber
        aperture = 'framework-relay'
        allowed_operations = @('HEAD','THREAD')
        hard_byte_ceiling = [int64]$ApertureHeadByteBudget
        cursor_ack = $false
        write_airlock_unchanged = $true
    }
    Write-Utf8NoBom $ReadRelayConfigPath ($config | ConvertTo-Json -Depth 20)
    return [pscustomobject]$config
}

function Get-ReadRelayState {
    if (-not (Test-Path -LiteralPath $ReadRelayStatePath)) {
        return [pscustomobject][ordered]@{
            state_version = 'campfire-read-relay-state-v1'
            last_complete_comment_id = 0
            last_complete_comment_count = 0
            active_request_id = $null
            active_worker_pid = $null
            active_started_at_utc = $null
            updated_at_utc = $null
        }
    }
    try { return Read-Utf8JsonFile $ReadRelayStatePath }
    catch { throw "Read relay state cannot be parsed: $($_.Exception.Message)" }
}

function Set-ReadRelayState($State) {
    $copy = [ordered]@{
        state_version = 'campfire-read-relay-state-v1'
        last_complete_comment_id = [int64](Safe-Property $State 'last_complete_comment_id' 0)
        last_complete_comment_count = [int](Safe-Property $State 'last_complete_comment_count' 0)
        active_request_id = Safe-Property $State 'active_request_id' $null
        active_worker_pid = Safe-Property $State 'active_worker_pid' $null
        active_started_at_utc = Safe-Property $State 'active_started_at_utc' $null
        updated_at_utc = [DateTime]::UtcNow.ToString('o')
    }
    Write-Utf8NoBom $ReadRelayStatePath ($copy | ConvertTo-Json -Depth 20)
    return [pscustomobject]$copy
}

function Get-GhExecutable {
    foreach ($name in @('gh.exe','gh')) {
        $command = Get-Command $name -ErrorAction SilentlyContinue
        if ($null -ne $command) { return [string]$command.Source }
    }
    throw 'GitHub CLI (gh) is not available on PATH. R26-A read bridge remains disabled.'
}

function Invoke-GhJson([string[]]$Arguments) {
    $gh = Get-GhExecutable
    $lines = @(& $gh @Arguments 2>&1)
    $exitCode = $LASTEXITCODE
    $text = ($lines -join [Environment]::NewLine)
    if ($exitCode -ne 0) {
        throw "gh failed with exit code $exitCode. $text"
    }
    if ([string]::IsNullOrWhiteSpace($text)) { return $null }
    try { return ($text | ConvertFrom-Json) }
    catch { throw "gh returned non-JSON output. $($_.Exception.Message)" }
}

function Get-ReadRelayIssueCommentsComplete {
    $issueRoute = "/repos/$ReadRelayRepo/issues/$ReadRelayIssueNumber"
    for ($attempt = 1; $attempt -le 2; $attempt++) {
        $before = Invoke-GhJson @('api',$issueRoute)
        $beforeCount = [int](Safe-Property $before 'comments' -1)
        $rows = [System.Collections.Generic.List[object]]::new()
        $page = 1
        $guardHit = $false
        while ($true) {
            if ($page -gt 100) { $guardHit = $true; break }
            $route = "$issueRoute/comments?per_page=100&page=$page"
            $batchRaw = Invoke-GhJson @('api',$route)
            $batch = @($batchRaw)
            foreach ($row in $batch) { $rows.Add($row) }
            if ($batch.Count -lt 100) { break }
            $page++
        }
        $after = Invoke-GhJson @('api',$issueRoute)
        $afterCount = [int](Safe-Property $after 'comments' -1)
        $stable = (-not $guardHit -and $beforeCount -ge 0 -and $beforeCount -eq $afterCount -and $rows.Count -eq $afterCount)
        if ($stable) {
            return [pscustomobject][ordered]@{
                retrieval_complete = $true
                returned_count = $rows.Count
                known_total = $afterCount
                pages_fetched = $page
                pagination_guard_hit = $false
                comments = @($rows.ToArray())
            }
        }
    }
    return [pscustomobject][ordered]@{
        retrieval_complete = $false
        returned_count = 0
        known_total = $null
        pages_fetched = $null
        pagination_guard_hit = $false
        comments = @()
    }
}

function Test-ReadRelayRequestIdSeen([string]$RequestId) {
    if ([string]::IsNullOrWhiteSpace($RequestId) -or -not (Test-Path -LiteralPath $ReadRelayLedgerPath)) { return $false }
    foreach ($line in @(Read-Utf8LinesFile $ReadRelayLedgerPath)) {
        if ([string]::IsNullOrWhiteSpace($line)) { continue }
        try { $row = $line | ConvertFrom-Json } catch { continue }
        $data = Safe-Property $row 'data' $null
        if ([string](Safe-Property $data 'request_id' '') -eq $RequestId -and
            @('READ_RELAY_REQUEST_DISPATCHED','READ_RELAY_REQUEST_REFUSED','READ_RELAY_RESPONSE_POSTED','READ_RELAY_RESPONSE_FAILED') -contains [string](Safe-Property $row 'kind' '')) {
            return $true
        }
    }
    return $false
}

function ConvertTo-ReadRelayRequest($Comment) {
    $user = Safe-Property $Comment 'user' $null
    if ([string](Safe-Property $user 'login' '') -ne $ReadRelayExpectedGitHubUser) { return $null }
    $app = Safe-Property $Comment 'performed_via_github_app' $null
    if ([string](Safe-Property $app 'slug' '') -ne $ReadRelayExpectedAppSlug) { return $null }
    $body = [string](Safe-Property $Comment 'body' '')
    if ([string]::IsNullOrWhiteSpace($body) -or -not $body.TrimStart().StartsWith('{')) { return $null }
    try { $request = $body | ConvertFrom-Json } catch { return $null }
    if ([string](Safe-Property $request 'type' '') -ne 'campfire-read-request-v1') { return $null }

    $allowed = @('type','request_id','aperture','operation','post_id','max_bytes','cursor_ack')
    foreach ($name in @($request.PSObject.Properties.Name)) {
        if ($allowed -notcontains [string]$name) { throw "READ_RELAY_REQUEST_REFUSED unknown field '$name'." }
    }
    $requestId = [string](Safe-Property $request 'request_id' '')
    if ($requestId -notmatch '^fw-read-[A-Za-z0-9._:-]{1,100}$') { throw 'READ_RELAY_REQUEST_REFUSED invalid request_id.' }
    if ([string](Safe-Property $request 'aperture' '') -ne 'framework-relay') { throw 'READ_RELAY_REQUEST_REFUSED aperture must be framework-relay.' }
    $operation = [string](Safe-Property $request 'operation' '')
    if (@('HEAD','THREAD') -notcontains $operation) { throw 'READ_RELAY_REQUEST_REFUSED operation must be HEAD or THREAD.' }
    if ([int64](Safe-Property $request 'max_bytes' 0) -ne [int64]65536) { throw 'READ_RELAY_REQUEST_REFUSED max_bytes must be 65536.' }
    if ([bool](Safe-Property $request 'cursor_ack' $true)) { throw 'READ_RELAY_REQUEST_REFUSED cursor_ack must be false.' }
    $postId = [int](Safe-Property $request 'post_id' 0)
    if ($operation -eq 'THREAD' -and $postId -le 0) { throw 'READ_RELAY_REQUEST_REFUSED THREAD requires positive post_id.' }
    if ($operation -eq 'HEAD' -and $postId -ne 0) { throw 'READ_RELAY_REQUEST_REFUSED HEAD must not target a post_id.' }
    if (Test-ReadRelayRequestIdSeen $requestId) { throw 'READ_RELAY_REQUEST_REFUSED request_id already consumed.' }

    return [pscustomobject][ordered]@{
        request_id = $requestId
        operation = $operation
        post_id = $postId
        source_comment_id = [int64](Safe-Property $Comment 'id' 0)
    }
}

function Quote-ReadRelayProcessArgument([string]$Value) {
    return '"' + ($Value -replace '"','\\"') + '"'
}

function Get-ReadRelayRequestStatusPath([string]$RequestId) {
    return Join-Path $ReadRelayStatusDir ($RequestId + '.json')
}

function Start-ReadRelayWorker($Request) {
    $requestId = [string](Safe-Property $Request 'request_id' '')
    $kind = [string](Safe-Property $Request 'operation' '')
    $postId = [int](Safe-Property $Request 'post_id' 0)
    $workerScript = if (-not [string]::IsNullOrWhiteSpace([string]$PSCommandPath)) { [string]$PSCommandPath } else { $InstalledScript }
    $argText = @(
        '-NoProfile',
        '-ExecutionPolicy Bypass',
        '-File ' + (Quote-ReadRelayProcessArgument $workerScript),
        '-HeadlessRead',
        '-HeadlessCitizen framework-relay',
        '-HeadlessKind ' + $kind,
        '-HeadlessRequestId ' + (Quote-ReadRelayProcessArgument $requestId),
        '-HeadlessOutputDirectory ' + (Quote-ReadRelayProcessArgument $ReadRelayOutbox),
        '-HeadlessPostResponse'
    )
    if ($kind -eq 'THREAD') { $argText += ('-HeadlessPostId ' + $postId) }
    $process = Start-Process powershell.exe -ArgumentList ($argText -join ' ') -WindowStyle Hidden -PassThru
    return $process
}

function Initialize-ReadRelay {
    [void](Get-GhExecutable)
    $complete = Get-ReadRelayIssueCommentsComplete
    if (-not [bool](Safe-Property $complete 'retrieval_complete' $false)) {
        throw 'Read relay cannot initialize because the private machine-lane comment set was not retrieved completely.'
    }
    $maxId = [int64]0
    foreach ($comment in @(Safe-Property $complete 'comments' @())) {
        $id = [int64](Safe-Property $comment 'id' 0)
        if ($id -gt $maxId) { $maxId = $id }
    }
    $state = Get-ReadRelayState
    if (-not [bool](Safe-Property (Get-ReadRelayConfig) 'initialized' $false)) {
        $state.last_complete_comment_id = $maxId
        $state.last_complete_comment_count = [int](Safe-Property $complete 'known_total' 0)
        $state.active_request_id = $null
        $state.active_worker_pid = $null
        $state.active_started_at_utc = $null
        [void](Set-ReadRelayState $state)
        [void](Write-ReadRelayLedgerEvent 'READ_RELAY_BASELINE_ESTABLISHED' ([pscustomobject]@{
            latest_comment_id = $maxId
            known_total = [int](Safe-Property $complete 'known_total' 0)
            historical_requests_are_not_executed = $true
        }))
    }
    [void](Set-ReadRelayConfig $true $true)
    [void](Write-ReadRelayLedgerEvent 'READ_RELAY_ENABLED' ([pscustomobject]@{
        repository = $ReadRelayRepo
        issue_number = $ReadRelayIssueNumber
        aperture = 'framework-relay'
        write_airlock_unchanged = $true
    }))
}

function Disable-ReadRelay {
    $cfg = Get-ReadRelayConfig
    [void](Set-ReadRelayConfig $false ([bool](Safe-Property $cfg 'initialized' $false)))
    [void](Write-ReadRelayLedgerEvent 'READ_RELAY_DISABLED' ([pscustomobject]@{
        note = 'No new read requests will be dispatched. Any already-running bounded read is allowed to finish.'
    }))
}

function Get-ReadRelayHumanStatus {
    $cfg = Get-ReadRelayConfig
    $state = Get-ReadRelayState
    $enabled = [bool](Safe-Property $cfg 'enabled' $false)
    $active = [string](Safe-Property $state 'active_request_id' '')
    $status = if ($enabled) { 'ENABLED' } else { 'DISABLED' }
    if (-not [string]::IsNullOrWhiteSpace($active)) { $status += " | active $active" }
    return "$status | private $ReadRelayRepo issue #$ReadRelayIssueNumber | Framework HEAD/THREAD only | writes unchanged"
}

function Invoke-ReadRelayPoll {
    if ($script:ReadRelayPollInProgress) { return }
    $cfg = Get-ReadRelayConfig
    if (-not [bool](Safe-Property $cfg 'enabled' $false)) { return }
    $script:ReadRelayPollInProgress = $true
    try {
        $state = Get-ReadRelayState
        $activeRequest = [string](Safe-Property $state 'active_request_id' '')
        if (-not [string]::IsNullOrWhiteSpace($activeRequest)) {
            $statusPath = Get-ReadRelayRequestStatusPath $activeRequest
            if (Test-Path -LiteralPath $statusPath) {
                try { $workerStatus = Read-Utf8JsonFile $statusPath } catch { $workerStatus = $null }
                $terminal = [string](Safe-Property $workerStatus 'status' '')
                if (@('COMPLETE','FAILED') -contains $terminal) {
                    $state.active_request_id = $null
                    $state.active_worker_pid = $null
                    $state.active_started_at_utc = $null
                    [void](Set-ReadRelayState $state)
                }
                else { return }
            }
            else {
                $pid = [int](Safe-Property $state 'active_worker_pid' 0)
                if ($pid -gt 0 -and $null -ne (Get-Process -Id $pid -ErrorAction SilentlyContinue)) { return }
                [void](Write-ReadRelayLedgerEvent 'READ_RELAY_WORKER_TERMINAL_STATUS_MISSING' ([pscustomobject]@{
                    request_id = $activeRequest
                    worker_pid = $pid
                    silent_retry = $false
                }))
                try {
                    $requestPath = Join-Path $ReadRelayInbox ($activeRequest + '.json')
                    if (Test-Path -LiteralPath $requestPath) {
                        $stalledRequest = Read-Utf8JsonFile $requestPath
                        [void](Post-ReadRelayFailureResponse `
                            $activeRequest `
                            ([string](Safe-Property $stalledRequest 'operation' '')) `
                            ([int](Safe-Property $stalledRequest 'post_id' 0)) `
                            'READ_RELAY_WORKER_TERMINATED_WITHOUT_TERMINAL_STATUS')
                    }
                } catch { }
                $state.active_request_id = $null
                $state.active_worker_pid = $null
                $state.active_started_at_utc = $null
                [void](Set-ReadRelayState $state)
            }
        }

        $complete = Get-ReadRelayIssueCommentsComplete
        if (-not [bool](Safe-Property $complete 'retrieval_complete' $false)) {
            [void](Write-ReadRelayLedgerEvent 'READ_RELAY_RETRIEVAL_INCOMPLETE' ([pscustomobject]@{
                returned_count = Safe-Property $complete 'returned_count' $null
                known_total = Safe-Property $complete 'known_total' $null
                no_negative_conclusion = $true
            }))
            return
        }

        $state = Get-ReadRelayState
        $highWater = [int64](Safe-Property $state 'last_complete_comment_id' 0)
        $newComments = @(
            @(Safe-Property $complete 'comments' @()) |
            Where-Object { [int64](Safe-Property $_ 'id' 0) -gt $highWater } |
            Sort-Object @{Expression={ [int64](Safe-Property $_ 'id' 0) }; Ascending=$true}
        )
        foreach ($comment in $newComments) {
            $commentId = [int64](Safe-Property $comment 'id' 0)
            try {
                $request = ConvertTo-ReadRelayRequest $comment
                if ($null -ne $request) {
                    [void](Write-ReadRelayLedgerEvent 'READ_RELAY_REQUEST_OBSERVED' ([pscustomobject]@{
                        request_id = $request.request_id
                        operation = $request.operation
                        post_id = $request.post_id
                        source_comment_id = $commentId
                        route_app_slug = $ReadRelayExpectedAppSlug
                        route_identity_is_not_runtime_identity = $true
                    }))
                    $requestPath = Join-Path $ReadRelayInbox ($request.request_id + '.json')
                    Write-Utf8NoBom $requestPath ($request | ConvertTo-Json -Depth 10)
                    $process = Start-ReadRelayWorker $request
                    [void](Write-ReadRelayLedgerEvent 'READ_RELAY_REQUEST_DISPATCHED' ([pscustomobject]@{
                        request_id = $request.request_id
                        operation = $request.operation
                        post_id = $request.post_id
                        source_comment_id = $commentId
                        worker_pid = $process.Id
                        request_path_basename = [IO.Path]::GetFileName($requestPath)
                    }))
                    $state.last_complete_comment_id = $commentId
                    $state.last_complete_comment_count = [int](Safe-Property $complete 'known_total' 0)
                    $state.active_request_id = $request.request_id
                    $state.active_worker_pid = $process.Id
                    $state.active_started_at_utc = [DateTime]::UtcNow.ToString('o')
                    [void](Set-ReadRelayState $state)
                    return
                }
            }
            catch {
                [void](Write-ReadRelayLedgerEvent 'READ_RELAY_REQUEST_REFUSED' ([pscustomobject]@{
                    request_id = $null
                    source_comment_id = $commentId
                    reason = $_.Exception.Message
                }))
            }
            $state.last_complete_comment_id = $commentId
            $state.last_complete_comment_count = [int](Safe-Property $complete 'known_total' 0)
            [void](Set-ReadRelayState $state)
        }
    }
    catch {
        [void](Write-ReadRelayLedgerEvent 'READ_RELAY_POLL_FAILED' ([pscustomobject]@{
            reason = $_.Exception.Message
            silent_retry = $false
        }))
    }
    finally {
        $script:ReadRelayPollInProgress = $false
    }
}

# ----------------------------- R26-B CC LOCAL READ RELAY --------------------
function Write-CcReadRelayLedgerEvent([string]$Kind, $Data = $null) {
    New-Item -ItemType Directory -Force -Path $CcReadRelayRoot | Out-Null
    $row = [ordered]@{
        event_version = 'campfire-cc-read-relay-event-v1'
        event_id = [guid]::NewGuid().ToString()
        created_at_utc = [DateTime]::UtcNow.ToString('o')
        kind = $Kind
        aperture = 'cc-relay'
        data = $Data
    }
    $line = $row | ConvertTo-Json -Depth 30 -Compress
    [System.IO.File]::AppendAllText(
        $CcReadRelayLedgerPath,
        $line + [Environment]::NewLine,
        [System.Text.UTF8Encoding]::new($false)
    )
    return [pscustomobject]$row
}

function Get-CcReadRelayConfig {
    if (-not (Test-Path -LiteralPath $CcReadRelayConfigPath)) {
        return [pscustomobject][ordered]@{
            config_version = 'campfire-cc-read-relay-config-v1'
            enabled = $false
            initialized = $false
            created_at_utc = $null
            updated_at_utc = $null
        }
    }
    try { return Read-Utf8JsonFile $CcReadRelayConfigPath }
    catch { throw "CC read relay config cannot be parsed: $($_.Exception.Message)" }
}

function Set-CcReadRelayConfig([bool]$Enabled, [bool]$Initialized) {
    $prior = Get-CcReadRelayConfig
    $created = Safe-Property $prior 'created_at_utc' $null
    if ([string]::IsNullOrWhiteSpace([string]$created)) { $created = [DateTime]::UtcNow.ToString('o') }
    $config = [ordered]@{
        config_version = 'campfire-cc-read-relay-config-v1'
        enabled = $Enabled
        initialized = $Initialized
        created_at_utc = $created
        updated_at_utc = [DateTime]::UtcNow.ToString('o')
        transport = 'local-filesystem'
        ingress_directory = $CcReadRelayIngress
        response_directory = $CcReadRelayResponses
        evidence_issue_number = $CcReadRelayEvidenceIssueNumber
        evidence_issue_is_not_ingress = $true
        aperture = 'cc-relay'
        allowed_operations = @('HEAD','THREAD')
        hard_byte_ceiling = [int64]$ApertureHeadByteBudget
        cursor_ack = $false
        write_airlock_unchanged = $true
        route_identity_is_not_runtime_identity = $true
    }
    Write-Utf8NoBom $CcReadRelayConfigPath ($config | ConvertTo-Json -Depth 20)
    return [pscustomobject]$config
}

function Get-CcReadRelayState {
    if (-not (Test-Path -LiteralPath $CcReadRelayStatePath)) {
        return [pscustomobject][ordered]@{
            state_version = 'campfire-cc-read-relay-state-v1'
            active_request_id = $null
            active_worker_pid = $null
            active_started_at_utc = $null
            updated_at_utc = $null
        }
    }
    try { return Read-Utf8JsonFile $CcReadRelayStatePath }
    catch { throw "CC read relay state cannot be parsed: $($_.Exception.Message)" }
}

function Set-CcReadRelayState($State) {
    $copy = [ordered]@{
        state_version = 'campfire-cc-read-relay-state-v1'
        active_request_id = Safe-Property $State 'active_request_id' $null
        active_worker_pid = Safe-Property $State 'active_worker_pid' $null
        active_started_at_utc = Safe-Property $State 'active_started_at_utc' $null
        updated_at_utc = [DateTime]::UtcNow.ToString('o')
    }
    Write-Utf8NoBom $CcReadRelayStatePath ($copy | ConvertTo-Json -Depth 20)
    return [pscustomobject]$copy
}

function Test-CcReadRelayRequestIdSeen([string]$RequestId) {
    if ([string]::IsNullOrWhiteSpace($RequestId)) { return $false }
    if (Test-Path -LiteralPath (Join-Path $CcReadRelayResponses ($RequestId + '.response.json'))) { return $true }
    if (-not (Test-Path -LiteralPath $CcReadRelayLedgerPath)) { return $false }
    foreach ($line in @(Read-Utf8LinesFile $CcReadRelayLedgerPath)) {
        if ([string]::IsNullOrWhiteSpace($line)) { continue }
        try { $row = $line | ConvertFrom-Json } catch { continue }
        $data = Safe-Property $row 'data' $null
        if ([string](Safe-Property $data 'request_id' '') -eq $RequestId -and
            @('CC_READ_RELAY_REQUEST_DISPATCHED','CC_READ_RELAY_REQUEST_REFUSED','CC_READ_RELAY_RESPONSE_WRITTEN','CC_READ_RELAY_RESPONSE_FAILED') -contains [string](Safe-Property $row 'kind' '')) {
            return $true
        }
    }
    return $false
}

function ConvertTo-CcReadRelayRequestFile([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path)) { throw 'CC_READ_RELAY_REQUEST_REFUSED request file missing.' }
    $item = Get-Item -LiteralPath $Path
    if ($item.Length -gt 4096) { throw 'CC_READ_RELAY_REQUEST_REFUSED request file exceeds 4096-byte envelope ceiling.' }
    try { $request = Read-Utf8JsonFile $Path } catch { throw "CC_READ_RELAY_REQUEST_REFUSED invalid JSON: $($_.Exception.Message)" }
    $allowed = @('type','request_id','aperture','operation','post_id','max_bytes','cursor_ack')
    foreach ($name in @($request.PSObject.Properties.Name)) {
        if ($allowed -notcontains [string]$name) { throw "CC_READ_RELAY_REQUEST_REFUSED unknown field '$name'." }
    }
    if ([string](Safe-Property $request 'type' '') -ne 'campfire-read-request-v1') { throw 'CC_READ_RELAY_REQUEST_REFUSED type must be campfire-read-request-v1.' }
    $requestId = [string](Safe-Property $request 'request_id' '')
    if ($requestId -notmatch '^cc-read-[A-Za-z0-9._:-]{1,100}$') { throw 'CC_READ_RELAY_REQUEST_REFUSED invalid request_id.' }
    if ([IO.Path]::GetFileName($Path) -ne ($requestId + '.json')) { throw 'CC_READ_RELAY_REQUEST_REFUSED filename must equal <request_id>.json.' }
    if ([string](Safe-Property $request 'aperture' '') -ne 'cc-relay') { throw 'CC_READ_RELAY_REQUEST_REFUSED aperture must be cc-relay.' }
    $operation = [string](Safe-Property $request 'operation' '')
    if (@('HEAD','THREAD') -notcontains $operation) { throw 'CC_READ_RELAY_REQUEST_REFUSED operation must be HEAD or THREAD.' }
    if ([int64](Safe-Property $request 'max_bytes' 0) -ne [int64]65536) { throw 'CC_READ_RELAY_REQUEST_REFUSED max_bytes must be 65536.' }
    if ([bool](Safe-Property $request 'cursor_ack' $true)) { throw 'CC_READ_RELAY_REQUEST_REFUSED cursor_ack must be false.' }
    $postId = [int](Safe-Property $request 'post_id' 0)
    if ($operation -eq 'THREAD' -and $postId -le 0) { throw 'CC_READ_RELAY_REQUEST_REFUSED THREAD requires positive post_id.' }
    if ($operation -eq 'HEAD' -and $postId -ne 0) { throw 'CC_READ_RELAY_REQUEST_REFUSED HEAD must not target a post_id.' }
    if (Test-CcReadRelayRequestIdSeen $requestId) { throw 'CC_READ_RELAY_REQUEST_REFUSED request_id already consumed.' }
    return [pscustomobject][ordered]@{
        request_id = $requestId
        operation = $operation
        post_id = $postId
        source_path = $Path
        source_sha256 = Get-Sha256File $Path
        source_bytes = $item.Length
    }
}

function Get-CcReadRelayRequestStatusPath([string]$RequestId) {
    return Join-Path $CcReadRelayStatusDir ($RequestId + '.json')
}

function Start-CcReadRelayWorker($Request) {
    $requestId = [string](Safe-Property $Request 'request_id' '')
    $kind = [string](Safe-Property $Request 'operation' '')
    $postId = [int](Safe-Property $Request 'post_id' 0)
    $workerScript = if (-not [string]::IsNullOrWhiteSpace([string]$PSCommandPath)) { [string]$PSCommandPath } else { $InstalledScript }
    $argText = @(
        '-NoProfile',
        '-ExecutionPolicy Bypass',
        '-File ' + (Quote-ReadRelayProcessArgument $workerScript),
        '-HeadlessRead',
        '-HeadlessCitizen cc-relay',
        '-HeadlessKind ' + $kind,
        '-HeadlessRequestId ' + (Quote-ReadRelayProcessArgument $requestId),
        '-HeadlessOutputDirectory ' + (Quote-ReadRelayProcessArgument $CcReadRelayOutbox)
    )
    if ($kind -eq 'THREAD') { $argText += ('-HeadlessPostId ' + $postId) }
    return Start-Process powershell.exe -ArgumentList ($argText -join ' ') -WindowStyle Hidden -PassThru
}

function Move-CcReadRelayRequestFile([string]$Path, [string]$Bucket) {
    if (-not (Test-Path -LiteralPath $Path)) { return $null }
    $destinationDir = Join-Path $CcReadRelayArchive $Bucket
    New-Item -ItemType Directory -Force -Path $destinationDir | Out-Null
    $destination = Join-Path $destinationDir ([IO.Path]::GetFileName($Path))
    if (Test-Path -LiteralPath $destination) {
        $destination = Join-Path $destinationDir (([IO.Path]::GetFileNameWithoutExtension($Path)) + '-' + [guid]::NewGuid().ToString('N') + '.json')
    }
    Move-Item -LiteralPath $Path -Destination $destination -Force
    return $destination
}

function Initialize-CcReadRelay {
    foreach ($dir in @($CcReadRelayRoot,$CcReadRelayIngress,$CcReadRelayInbox,$CcReadRelayOutbox,$CcReadRelayResponses,$CcReadRelayArchive,$CcReadRelayStatusDir)) {
        New-Item -ItemType Directory -Force -Path $dir | Out-Null
    }
    $cfg = Get-CcReadRelayConfig
    if (-not [bool](Safe-Property $cfg 'initialized' $false)) {
        $existing = @(Get-ChildItem -LiteralPath $CcReadRelayIngress -Filter '*.json' -File -ErrorAction SilentlyContinue)
        $ignored = 0
        foreach ($file in $existing) {
            [void](Move-CcReadRelayRequestFile $file.FullName 'baseline-ignored')
            $ignored++
        }
        $state = Get-CcReadRelayState
        $state.active_request_id = $null
        $state.active_worker_pid = $null
        $state.active_started_at_utc = $null
        [void](Set-CcReadRelayState $state)
        [void](Write-CcReadRelayLedgerEvent 'CC_READ_RELAY_BASELINE_ESTABLISHED' ([pscustomobject]@{
            historical_request_files_ignored = $ignored
            historical_requests_are_not_executed = $true
        }))
    }
    [void](Set-CcReadRelayConfig $true $true)
    [void](Write-CcReadRelayLedgerEvent 'CC_READ_RELAY_ENABLED' ([pscustomobject]@{
        transport = 'local-filesystem'
        ingress_directory = $CcReadRelayIngress
        aperture = 'cc-relay'
        evidence_issue_number = $CcReadRelayEvidenceIssueNumber
        evidence_issue_is_not_ingress = $true
        write_airlock_unchanged = $true
    }))
}

function Disable-CcReadRelay {
    $cfg = Get-CcReadRelayConfig
    [void](Set-CcReadRelayConfig $false ([bool](Safe-Property $cfg 'initialized' $false)))
    [void](Write-CcReadRelayLedgerEvent 'CC_READ_RELAY_DISABLED' ([pscustomobject]@{
        note = 'No new CC local read request files will be dispatched. Any already-running bounded read is allowed to finish.'
    }))
}

function Get-CcReadRelayHumanStatus {
    $cfg = Get-CcReadRelayConfig
    $state = Get-CcReadRelayState
    $enabled = [bool](Safe-Property $cfg 'enabled' $false)
    $active = [string](Safe-Property $state 'active_request_id' '')
    $status = if ($enabled) { 'ENABLED' } else { 'DISABLED' }
    if (-not [string]::IsNullOrWhiteSpace($active)) { $status += " | active $active" }
    return "$status | LOCAL cc-relay HEAD/THREAD only | writes unchanged"
}

function Write-CcReadRelayResponseFile($Request, [string]$Status, $WorkerStatus) {
    $requestId = [string](Safe-Property $Request 'request_id' '')
    $operation = [string](Safe-Property $Request 'operation' '')
    $postId = [int](Safe-Property $Request 'post_id' 0)
    $data = Safe-Property $WorkerStatus 'data' $null
    $response = [ordered]@{
        type = 'campfire-read-response-v1'
        request_id = $requestId
        status = $Status
        aperture = 'cc-relay'
        operation = $operation
        post_id = if ($operation -eq 'THREAD') { $postId } else { $null }
        created_at_utc = [DateTime]::UtcNow.ToString('o')
        transport = 'local-filesystem'
        artifact = $null
        reason = $null
        boundaries = [ordered]@{
            square_write = $false
            cursor_ack = $false
            full_quick_loaded = $false
            automatic_semantic_push = $false
            transport_completion_is_not_semantic_read = $true
            local_route_identity_is_not_runtime_identity = $true
            framework_lane_shared = $false
        }
    }
    if ($Status -eq 'COMPLETE') {
        $artifactPath = [string](Safe-Property $data 'artifact_path' '')
        if ([string]::IsNullOrWhiteSpace($artifactPath) -or -not (Test-Path -LiteralPath $artifactPath)) {
            throw 'CC_READ_RELAY_RESPONSE_FAILED terminal worker status did not point to an existing artifact.'
        }
        $artifact = Read-Utf8JsonFile $artifactPath
        $completeness = if ($operation -eq 'HEAD') {
            [ordered]@{
                semantic_bodies_loaded = Safe-Property (Safe-Property $artifact 'aperture_invariant' $null) 'semantic_bodies_loaded' $false
                attention_rows_total = Safe-Property (Safe-Property $artifact 'aperture_budget' $null) 'attention_rows_total' $null
                attention_rows_included = Safe-Property (Safe-Property $artifact 'aperture_budget' $null) 'attention_rows_included' $null
                attention_rows_omitted = Safe-Property (Safe-Property $artifact 'aperture_budget' $null) 'attention_rows_omitted' $null
            }
        } else { Safe-Property $artifact 'completeness' $null }
        $response.artifact = [ordered]@{
            path = $artifactPath
            filename = [IO.Path]::GetFileName($artifactPath)
            exact_json_sha256 = Get-Sha256File $artifactPath
            exact_json_bytes = (Get-Item -LiteralPath $artifactPath).Length
            hard_byte_ceiling = 65536
            campfire_square_source_sha256 = if (-not [string]::IsNullOrWhiteSpace([string]$PSCommandPath)) { Get-Sha256File $PSCommandPath } else { $null }
            completeness = $completeness
        }
    }
    else {
        $response.reason = [string](Safe-Property $data 'reason' 'CC_READ_RELAY_WORKER_FAILED')
    }
    $path = Join-Path $CcReadRelayResponses ($requestId + '.response.json')
    Write-Utf8NoBom $path ($response | ConvertTo-Json -Depth 60)
    return $path
}

function Invoke-CcReadRelayPoll {
    if ($script:CcReadRelayPollInProgress) { return }
    $cfg = Get-CcReadRelayConfig
    if (-not [bool](Safe-Property $cfg 'enabled' $false)) { return }
    $script:CcReadRelayPollInProgress = $true
    try {
        foreach ($dir in @($CcReadRelayIngress,$CcReadRelayInbox,$CcReadRelayOutbox,$CcReadRelayResponses,$CcReadRelayArchive,$CcReadRelayStatusDir)) {
            New-Item -ItemType Directory -Force -Path $dir | Out-Null
        }
        $state = Get-CcReadRelayState
        $activeRequest = [string](Safe-Property $state 'active_request_id' '')
        if (-not [string]::IsNullOrWhiteSpace($activeRequest)) {
            $statusPath = Get-CcReadRelayRequestStatusPath $activeRequest
            if (Test-Path -LiteralPath $statusPath) {
                try { $workerStatus = Read-Utf8JsonFile $statusPath } catch { $workerStatus = $null }
                $terminal = [string](Safe-Property $workerStatus 'status' '')
                if (@('COMPLETE','FAILED') -contains $terminal) {
                    $requestPath = Join-Path $CcReadRelayInbox ($activeRequest + '.json')
                    if (-not (Test-Path -LiteralPath $requestPath)) { throw 'CC_READ_RELAY_RESPONSE_FAILED accepted request record is missing.' }
                    $request = Read-Utf8JsonFile $requestPath
                    try {
                        $responsePath = Write-CcReadRelayResponseFile $request $terminal $workerStatus
                        $responseEventKind = if ($terminal -eq 'COMPLETE') { 'CC_READ_RELAY_RESPONSE_WRITTEN' } else { 'CC_READ_RELAY_RESPONSE_FAILED' }
                        [void](Write-CcReadRelayLedgerEvent $responseEventKind ([pscustomobject]@{
                            request_id = $activeRequest
                            status = $terminal
                            response_path_basename = [IO.Path]::GetFileName($responsePath)
                            artifact_path_basename = if ($terminal -eq 'COMPLETE') { [IO.Path]::GetFileName([string](Safe-Property (Safe-Property $workerStatus 'data' $null) 'artifact_path' '')) } else { $null }
                            silent_retry = $false
                        }))
                    }
                    catch {
                        [void](Write-CcReadRelayLedgerEvent 'CC_READ_RELAY_RESPONSE_FAILED' ([pscustomobject]@{
                            request_id = $activeRequest
                            reason = $_.Exception.Message
                            silent_retry = $false
                        }))
                    }
                    $state.active_request_id = $null
                    $state.active_worker_pid = $null
                    $state.active_started_at_utc = $null
                    [void](Set-CcReadRelayState $state)
                }
                else { return }
            }
            else {
                $pid = [int](Safe-Property $state 'active_worker_pid' 0)
                if ($pid -gt 0 -and $null -ne (Get-Process -Id $pid -ErrorAction SilentlyContinue)) { return }
                [void](Write-CcReadRelayLedgerEvent 'CC_READ_RELAY_WORKER_TERMINAL_STATUS_MISSING' ([pscustomobject]@{
                    request_id = $activeRequest
                    worker_pid = $pid
                    silent_retry = $false
                }))
                $state.active_request_id = $null
                $state.active_worker_pid = $null
                $state.active_started_at_utc = $null
                [void](Set-CcReadRelayState $state)
                return
            }
        }

        $candidates = @(Get-ChildItem -LiteralPath $CcReadRelayIngress -Filter '*.json' -File -ErrorAction SilentlyContinue | Sort-Object LastWriteTimeUtc,Name)
        if ($candidates.Count -eq 0) { return }
        $file = $candidates[0]
        try {
            $request = ConvertTo-CcReadRelayRequestFile $file.FullName
            [void](Write-CcReadRelayLedgerEvent 'CC_READ_RELAY_REQUEST_OBSERVED' ([pscustomobject]@{
                request_id = $request.request_id
                operation = $request.operation
                post_id = $request.post_id
                source_sha256 = $request.source_sha256
                source_bytes = $request.source_bytes
                local_route_identity_is_not_runtime_identity = $true
            }))
            $acceptedPath = Join-Path $CcReadRelayInbox ($request.request_id + '.json')
            Write-Utf8NoBom $acceptedPath (([ordered]@{
                type = 'campfire-read-request-v1'
                request_id = $request.request_id
                aperture = 'cc-relay'
                operation = $request.operation
                post_id = if ($request.operation -eq 'THREAD') { $request.post_id } else { 0 }
                max_bytes = 65536
                cursor_ack = $false
            }) | ConvertTo-Json -Depth 10)
            [void](Move-CcReadRelayRequestFile $file.FullName 'processed')
            $process = Start-CcReadRelayWorker $request
            [void](Write-CcReadRelayLedgerEvent 'CC_READ_RELAY_REQUEST_DISPATCHED' ([pscustomobject]@{
                request_id = $request.request_id
                operation = $request.operation
                post_id = $request.post_id
                worker_pid = $process.Id
                accepted_request_basename = [IO.Path]::GetFileName($acceptedPath)
            }))
            $state = Get-CcReadRelayState
            $state.active_request_id = $request.request_id
            $state.active_worker_pid = $process.Id
            $state.active_started_at_utc = [DateTime]::UtcNow.ToString('o')
            [void](Set-CcReadRelayState $state)
            return
        }
        catch {
            $reason = $_.Exception.Message
            $requestId = [IO.Path]::GetFileNameWithoutExtension($file.Name)
            [void](Write-CcReadRelayLedgerEvent 'CC_READ_RELAY_REQUEST_REFUSED' ([pscustomobject]@{
                request_id = $requestId
                source_file = $file.Name
                reason = $reason
            }))
            try { [void](Move-CcReadRelayRequestFile $file.FullName 'refused') } catch { }
            $failure = [ordered]@{
                type = 'campfire-read-response-v1'
                request_id = $requestId
                status = 'FAILED'
                aperture = 'cc-relay'
                created_at_utc = [DateTime]::UtcNow.ToString('o')
                reason = $reason
                silent_retry = $false
                boundaries = [ordered]@{ square_write=$false; cursor_ack=$false; automatic_semantic_push=$false }
            }
            try { Write-Utf8NoBom (Join-Path $CcReadRelayResponses ($requestId + '.response.json')) ($failure | ConvertTo-Json -Depth 20) } catch { }
        }
    }
    catch {
        [void](Write-CcReadRelayLedgerEvent 'CC_READ_RELAY_POLL_FAILED' ([pscustomobject]@{
            reason = $_.Exception.Message
            silent_retry = $false
        }))
    }
    finally { $script:CcReadRelayPollInProgress = $false }
}

function Compress-ReadRelayArtifactBase64([string]$Path) {
    $bytes = [System.IO.File]::ReadAllBytes($Path)
    $memory = New-Object System.IO.MemoryStream
    try {
        $gzip = New-Object System.IO.Compression.GZipStream($memory,[System.IO.Compression.CompressionMode]::Compress,$true)
        try { $gzip.Write($bytes,0,$bytes.Length) } finally { $gzip.Dispose() }
        $compressed = $memory.ToArray()
        return [pscustomobject][ordered]@{
            raw_bytes = $bytes.Length
            gzip_bytes = $compressed.Length
            base64 = [Convert]::ToBase64String($compressed)
        }
    }
    finally { $memory.Dispose() }
}

function Post-ReadRelayCommentJson($Envelope) {
    $body = $Envelope | ConvertTo-Json -Depth 60 -Compress
    if ($body.Length -gt $ReadRelayResponseCharacterCeiling) {
        throw "READ_RELAY_RESPONSE_TOO_LARGE: encoded response is $($body.Length) characters; ceiling is $ReadRelayResponseCharacterCeiling."
    }
    $temp = Join-Path $ReadRelayStatusDir ('gh-comment-' + [guid]::NewGuid().ToString('N') + '.json')
    try {
        $requestBody = [ordered]@{ body = $body }
        Write-Utf8NoBom $temp ($requestBody | ConvertTo-Json -Depth 70 -Compress)
        $response = Invoke-GhJson @('api','--method','POST',"/repos/$ReadRelayRepo/issues/$ReadRelayIssueNumber/comments",'--input',$temp)
        return $response
    }
    finally { Remove-Item -LiteralPath $temp -Force -ErrorAction SilentlyContinue }
}

function Post-ReadRelayFailureResponse([string]$RequestId, [string]$Operation, [int]$PostId, [string]$Reason) {
    if ($RequestId -notmatch '^fw-read-[A-Za-z0-9._:-]{1,100}$') { return $null }
    $failure = [ordered]@{
        type = 'campfire-read-response-v1'
        request_id = $RequestId
        status = 'FAILED'
        aperture = 'framework-relay'
        operation = $Operation
        post_id = if ($Operation -eq 'THREAD') { $PostId } else { $null }
        created_at_utc = [DateTime]::UtcNow.ToString('o')
        reason = $Reason
        silent_retry = $false
        boundaries = [ordered]@{
            square_write = $false
            cursor_ack = $false
            transport_failure_is_not_semantic_refusal = $true
        }
    }
    return Post-ReadRelayCommentJson $failure
}

function Write-WriteRelayLedgerEvent([string]$Kind, $Data = $null) {
    New-Item -ItemType Directory -Force -Path $WriteRelayFrameworkRoot | Out-Null
    $row = [ordered]@{
        event_version = 'campfire-routine-write-relay-event-v1'
        event_id = [guid]::NewGuid().ToString()
        created_at_utc = [DateTime]::UtcNow.ToString('o')
        kind = $Kind
        aperture = 'framework-relay'
        data = $Data
    }
    $line = $row | ConvertTo-Json -Depth 40 -Compress
    [System.IO.File]::AppendAllText(
        $WriteRelayLedgerPath,
        $line + [Environment]::NewLine,
        [System.Text.UTF8Encoding]::new($false)
    )
    return [pscustomobject]$row
}

function Get-WriteRelayConfig {
    if (-not (Test-Path -LiteralPath $WriteRelayConfigPath)) {
        return [pscustomobject][ordered]@{
            config_version = 'campfire-routine-write-relay-config-v1'
            enabled = $false
            initialized = $false
            created_at_utc = $null
            updated_at_utc = $null
        }
    }
    try { return Read-Utf8JsonFile $WriteRelayConfigPath }
    catch { throw "Framework routine write relay config cannot be parsed: $($_.Exception.Message)" }
}

function Set-WriteRelayConfig([bool]$Enabled, [bool]$Initialized) {
    New-Item -ItemType Directory -Force -Path $WriteRelayFrameworkRoot | Out-Null
    $prior = Get-WriteRelayConfig
    $created = Safe-Property $prior 'created_at_utc' $null
    if ([string]::IsNullOrWhiteSpace([string]$created)) { $created = [DateTime]::UtcNow.ToString('o') }
    $config = [ordered]@{
        config_version = 'campfire-routine-write-relay-config-v1'
        enabled = $Enabled
        initialized = $Initialized
        created_at_utc = $created
        updated_at_utc = [DateTime]::UtcNow.ToString('o')
        repository = $ReadRelayRepo
        issue_number = $WriteRelayIssueNumber
        aperture = 'framework-relay'
        allowed_operations = @('COMMENT','POST')
        one_action_per_request = $true
        remote_batches = $false
        top_level_posts = 'REVIEWED_HIGH_REACH_ONLY'
        cursor_ack = $false
        correction_debt_closure = $false
        money_or_treasury = $false
        credential_operations = $false
        grant_mutation = $false
        cc_ingress = $false
        full_quick = $false
        existing_full_plan_airlock_unchanged = $true
        local_enable_is_content_endorsement = $false
        route_identity_is_not_runtime_identity = $true
    }
    Write-Utf8NoBom $WriteRelayConfigPath ($config | ConvertTo-Json -Depth 30)
    return [pscustomobject]$config
}

function Get-WriteRelayState {
    if (-not (Test-Path -LiteralPath $WriteRelayStatePath)) {
        return [pscustomobject][ordered]@{
            state_version = 'campfire-routine-write-relay-state-v1'
            last_complete_comment_id = [int64]0
            last_complete_comment_count = [int]0
            active_request_id = $null
            active_worker_pid = $null
            active_started_at_utc = $null
            active_dispatch_phase = $null
            updated_at_utc = $null
        }
    }
    try { return Read-Utf8JsonFile $WriteRelayStatePath }
    catch { throw "Framework routine write relay state cannot be parsed: $($_.Exception.Message)" }
}

function Set-WriteRelayState($State) {
    New-Item -ItemType Directory -Force -Path $WriteRelayFrameworkRoot | Out-Null
    $copy = [ordered]@{
        state_version = 'campfire-routine-write-relay-state-v1'
        last_complete_comment_id = [int64](Safe-Property $State 'last_complete_comment_id' 0)
        last_complete_comment_count = [int](Safe-Property $State 'last_complete_comment_count' 0)
        active_request_id = Safe-Property $State 'active_request_id' $null
        active_worker_pid = Safe-Property $State 'active_worker_pid' $null
        active_started_at_utc = Safe-Property $State 'active_started_at_utc' $null
        active_dispatch_phase = Safe-Property $State 'active_dispatch_phase' $null
        updated_at_utc = [DateTime]::UtcNow.ToString('o')
    }
    Write-Utf8NoBom $WriteRelayStatePath ($copy | ConvertTo-Json -Depth 20)
    return [pscustomobject]$copy
}

function Get-WriteRelayIssueCommentsComplete {
    $issueRoute = "/repos/$ReadRelayRepo/issues/$WriteRelayIssueNumber"
    for ($attempt = 1; $attempt -le 2; $attempt++) {
        $before = Invoke-GhJson @('api',$issueRoute)
        $beforeCount = [int](Safe-Property $before 'comments' -1)
        $rows = [System.Collections.Generic.List[object]]::new()
        $page = 1
        $guardHit = $false
        while ($true) {
            if ($page -gt 100) { $guardHit = $true; break }
            $route = "$issueRoute/comments?per_page=100&page=$page"
            $batchRaw = Invoke-GhJson @('api',$route)
            $batch = @($batchRaw)
            foreach ($row in $batch) { $rows.Add($row) }
            if ($batch.Count -lt 100) { break }
            $page++
        }
        $after = Invoke-GhJson @('api',$issueRoute)
        $afterCount = [int](Safe-Property $after 'comments' -1)
        $stable = (-not $guardHit -and $beforeCount -ge 0 -and $beforeCount -eq $afterCount -and $rows.Count -eq $afterCount)
        if ($stable) {
            return [pscustomobject][ordered]@{
                retrieval_complete = $true
                returned_count = $rows.Count
                known_total = $afterCount
                pages_fetched = $page
                pagination_guard_hit = $false
                comments = @($rows.ToArray())
            }
        }
    }
    return [pscustomobject][ordered]@{
        retrieval_complete = $false
        returned_count = 0
        known_total = $null
        pages_fetched = $null
        pagination_guard_hit = $false
        comments = @()
    }
}

function Test-WriteRelayRequestIdSeen([string]$RequestId) {
    if ([string]::IsNullOrWhiteSpace($RequestId) -or -not (Test-Path -LiteralPath $WriteRelayLedgerPath)) { return $false }
    foreach ($line in @(Read-Utf8LinesFile $WriteRelayLedgerPath)) {
        if ([string]::IsNullOrWhiteSpace($line)) { continue }
        try { $row = $line | ConvertFrom-Json } catch { continue }
        $data = Safe-Property $row 'data' $null
        if ([string](Safe-Property $data 'request_id' '') -eq $RequestId -and
            @('WRITE_RELAY_REQUEST_DISPATCHED','WRITE_RELAY_REQUEST_REFUSED','WRITE_RELAY_RESPONSE_POSTED','WRITE_RELAY_OUTCOME_UNKNOWN') -contains [string](Safe-Property $row 'kind' '')) {
            return $true
        }
    }
    return $false
}

function ConvertTo-WriteRelayRequest($Comment) {
    $user = Safe-Property $Comment 'user' $null
    if ([string](Safe-Property $user 'login' '') -ne $ReadRelayExpectedGitHubUser) { return $null }
    $app = Safe-Property $Comment 'performed_via_github_app' $null
    if ([string](Safe-Property $app 'slug' '') -ne $ReadRelayExpectedAppSlug) { return $null }
    $rawBody = [string](Safe-Property $Comment 'body' '')
    if ([string]::IsNullOrWhiteSpace($rawBody) -or -not $rawBody.TrimStart().StartsWith('{')) { return $null }
    if ([Text.Encoding]::UTF8.GetByteCount($rawBody) -gt $WriteRelayRequestCharacterCeiling) {
        throw 'WRITE_RELAY_REQUEST_REFUSED request envelope exceeds the bounded carrier ceiling.'
    }
    try { $request = $rawBody | ConvertFrom-Json } catch { return $null }
    if ([string](Safe-Property $request 'type' '') -ne 'campfire-routine-write-request-v1') { return $null }

    $allowed = @(
        'type','request_id','aperture','operation','action_id','expected_grant_id',
        'expected_grant_sha256','reason','cursor_ack','post_id','parent_id','title','body','high_reach_review'
    )
    foreach ($name in @($request.PSObject.Properties.Name | ForEach-Object { [string]$_ })) {
        if ($allowed -notcontains $name) { throw "WRITE_RELAY_REQUEST_REFUSED unknown field '$name'." }
    }

    $requestId = [string](Safe-Property $request 'request_id' '')
    if ($requestId -notmatch '^fw-write-[A-Za-z0-9._:-]{1,100}$') { throw 'WRITE_RELAY_REQUEST_REFUSED invalid request_id.' }
    if (Test-WriteRelayRequestIdSeen $requestId) { throw 'WRITE_RELAY_REQUEST_REFUSED request_id already consumed.' }
    if ([string](Safe-Property $request 'aperture' '') -ne 'framework-relay') { throw 'WRITE_RELAY_REQUEST_REFUSED aperture must be framework-relay.' }
    if ([bool](Safe-Property $request 'cursor_ack' $true)) { throw 'WRITE_RELAY_REQUEST_REFUSED cursor_ack must be false.' }

    $operation = [string](Safe-Property $request 'operation' '')
    if ($operation -notin @('COMMENT','POST')) { throw 'WRITE_RELAY_REQUEST_REFUSED operation must be COMMENT or POST.' }
    $actionId = [string](Safe-Property $request 'action_id' '')
    if ($actionId -notmatch '^fw-action-[A-Za-z0-9._:-]{1,120}$') { throw 'WRITE_RELAY_REQUEST_REFUSED invalid action_id.' }
    $expectedGrantId = [string](Safe-Property $request 'expected_grant_id' '')
    if ([string]::IsNullOrWhiteSpace($expectedGrantId) -or $expectedGrantId.Length -gt 240) { throw 'WRITE_RELAY_REQUEST_REFUSED expected_grant_id is required.' }
    $expectedGrantSha = [string](Safe-Property $request 'expected_grant_sha256' '')
    if ($expectedGrantSha -notmatch '^[0-9a-f]{64}$') { throw 'WRITE_RELAY_REQUEST_REFUSED expected_grant_sha256 must be lowercase SHA-256.' }
    $reason = [string](Safe-Property $request 'reason' '')
    if ([string]::IsNullOrWhiteSpace($reason) -or $reason.Length -gt 1200) { throw 'WRITE_RELAY_REQUEST_REFUSED reason is required and must be <= 1200 characters.' }

    $normalized = [ordered]@{
        type='campfire-routine-write-request-v1'; request_id=$requestId; aperture='framework-relay'; operation=$operation
        action_id=$actionId; expected_grant_id=$expectedGrantId; expected_grant_sha256=$expectedGrantSha
        reason=$reason; cursor_ack=$false
    }

    if ($operation -eq 'COMMENT') {
        $postId = [int](Safe-Property $request 'post_id' 0)
        if ($postId -le 0) { throw 'WRITE_RELAY_REQUEST_REFUSED COMMENT requires positive post_id.' }
        if ($null -ne (Safe-Property $request 'parent_id' $null)) {
            throw 'WRITE_RELAY_REQUEST_REFUSED remote COMMENT remains post-level; threaded replies remain outside this lane.'
        }
        $body = [string](Safe-Property $request 'body' '')
        if ([string]::IsNullOrWhiteSpace($body) -or $body.Length -gt 8000) { throw 'WRITE_RELAY_REQUEST_REFUSED COMMENT body must be 1-8000 characters.' }
        if (@($request.PSObject.Properties.Name) -contains 'title' -or @($request.PSObject.Properties.Name) -contains 'high_reach_review') {
            throw 'WRITE_RELAY_REQUEST_REFUSED COMMENT must not carry POST title/review fields.'
        }
        $normalized.post_id=$postId; $normalized.parent_id=$null; $normalized.body=$body
    }
    else {
        if (@($request.PSObject.Properties.Name) -contains 'post_id' -or @($request.PSObject.Properties.Name) -contains 'parent_id') {
            throw 'WRITE_RELAY_REQUEST_REFUSED POST must not carry comment target fields.'
        }
        $title=[string](Safe-Property $request 'title' '')
        $body=[string](Safe-Property $request 'body' '')
        $review=Safe-Property $request 'high_reach_review' $null
        if ($title.Length -lt 3 -or $title.Length -gt 120) { throw 'WRITE_RELAY_REQUEST_REFUSED POST title must be 3-120 characters.' }
        if ([string]::IsNullOrWhiteSpace($body) -or $body.Length -gt 8000) { throw 'WRITE_RELAY_REQUEST_REFUSED POST body must be 1-8000 characters.' }
        if ($null -eq $review) { throw 'WRITE_RELAY_REQUEST_REFUSED POST requires high_reach_review.' }
        $normalized.title=$title; $normalized.body=$body; $normalized.high_reach_review=$review
    }

    return [pscustomobject][ordered]@{
        request=[pscustomobject]$normalized
        source_comment_id=[int64](Safe-Property $Comment 'id' 0)
        source_comment_body_sha256=Get-Sha256Text $rawBody
        source_comment_body_bytes=[Text.Encoding]::UTF8.GetByteCount($rawBody)
        route_user=$ReadRelayExpectedGitHubUser; route_app_slug=$ReadRelayExpectedAppSlug
        route_identity_is_not_runtime_identity=$true
    }
}

function Get-WriteRelayRequestStatusPath([string]$RequestId) {
    return Join-Path $WriteRelayStatusDir ($RequestId + '.json')
}

function Start-WriteRelayWorker($Envelope, [string]$RequestPath) {
    $request = Safe-Property $Envelope 'request' $null
    $requestId = [string](Safe-Property $request 'request_id' '')
    $workerScript = if (-not [string]::IsNullOrWhiteSpace([string]$PSCommandPath)) { [string]$PSCommandPath } else { $InstalledScript }
    $argText = @(
        '-NoProfile',
        '-ExecutionPolicy Bypass',
        '-File ' + (Quote-ReadRelayProcessArgument $workerScript),
        '-HeadlessWrite',
        '-HeadlessCitizen framework-relay',
        '-HeadlessWriteRequestPath ' + (Quote-ReadRelayProcessArgument $RequestPath),
        '-HeadlessWriteRequestId ' + (Quote-ReadRelayProcessArgument $requestId),
        '-HeadlessWritePostResponse'
    )
    return Start-Process powershell.exe -ArgumentList ($argText -join ' ') -WindowStyle Hidden -PassThru
}

function Initialize-WriteRelay {
    [void](Get-GhExecutable)
    foreach ($dir in @($WriteRelayRoot,$WriteRelayFrameworkRoot,$WriteRelayInbox,$WriteRelayStatusDir)) {
        New-Item -ItemType Directory -Force -Path $dir | Out-Null
    }
    $complete = Get-WriteRelayIssueCommentsComplete
    if (-not [bool](Safe-Property $complete 'retrieval_complete' $false)) {
        throw 'Routine write relay cannot initialize because private issue #177 was not retrieved completely.'
    }
    $maxId = [int64]0
    foreach ($comment in @(Safe-Property $complete 'comments' @())) {
        $id = [int64](Safe-Property $comment 'id' 0)
        if ($id -gt $maxId) { $maxId = $id }
    }
    $cfg = Get-WriteRelayConfig
    $state = Get-WriteRelayState
    if (-not [bool](Safe-Property $cfg 'initialized' $false)) {
        $state.last_complete_comment_id = $maxId
        $state.last_complete_comment_count = [int](Safe-Property $complete 'known_total' 0)
        $state.active_request_id = $null
        $state.active_worker_pid = $null
        $state.active_started_at_utc = $null
        $state.active_dispatch_phase = $null
        [void](Set-WriteRelayState $state)
        [void](Write-WriteRelayLedgerEvent 'WRITE_RELAY_BASELINE_ESTABLISHED' ([pscustomobject]@{
            latest_comment_id = $maxId
            known_total = [int](Safe-Property $complete 'known_total' 0)
            historical_requests_are_not_executed = $true
        }))
    }
    [void](Set-WriteRelayConfig $true $true)
    [void](Write-WriteRelayLedgerEvent 'WRITE_RELAY_ENABLED' ([pscustomobject]@{
        repository = $ReadRelayRepo
        issue_number = $WriteRelayIssueNumber
        aperture = 'framework-relay'
        allowed_operations = @('COMMENT','POST')
        local_enable_is_content_endorsement = $false
        existing_full_plan_airlock_unchanged = $true
    }))
}

function Disable-WriteRelay {
    $cfg = Get-WriteRelayConfig
    [void](Set-WriteRelayConfig $false ([bool](Safe-Property $cfg 'initialized' $false)))
    [void](Write-WriteRelayLedgerEvent 'WRITE_RELAY_DISABLED' ([pscustomobject]@{
        note = 'No new routine write request will be dispatched. Any already-issued Square write is never silently retried.'
        square_retry = $false
    }))
}

function Get-WriteRelayHumanStatus {
    $cfg = Get-WriteRelayConfig
    $state = Get-WriteRelayState
    $enabled = [bool](Safe-Property $cfg 'enabled' $false)
    $active = [string](Safe-Property $state 'active_request_id' '')
    $status = if ($enabled) { 'ENABLED' } else { 'DISABLED' }
    if (-not [string]::IsNullOrWhiteSpace($active)) { $status += " | active $active" }
    return "$status | private $ReadRelayRepo issue #$WriteRelayIssueNumber | Framework COMMENT (routine-enable) + reviewed POST (standing higher-reach grant) | money/credentials/cursor refused"
}

function Post-WriteRelayCommentJson($Object) {
    $bodyText = $Object | ConvertTo-Json -Depth 50 -Compress
    if ($bodyText.Length -gt $ReadRelayResponseCharacterCeiling) {
        throw "WRITE_RELAY_RESPONSE_TOO_LARGE: response envelope length $($bodyText.Length) exceeds $ReadRelayResponseCharacterCeiling characters."
    }
    $temp = Join-Path ([IO.Path]::GetTempPath()) ('campfire-write-relay-response-' + [guid]::NewGuid().ToString('N') + '.json')
    try {
        Write-Utf8NoBom $temp (([ordered]@{ body = $bodyText }) | ConvertTo-Json -Depth 60 -Compress)
        return Invoke-GhJson @('api','--method','POST',"/repos/$ReadRelayRepo/issues/$WriteRelayIssueNumber/comments",'--input',$temp)
    }
    finally {
        Remove-Item -LiteralPath $temp -Force -ErrorAction SilentlyContinue
    }
}

function New-WriteRelayResponse([string]$RequestId, [string]$Status, $Request = $null, $Data = $null, $Reason = $null) {
    $operation=[string](Safe-Property $Request 'operation' '')
    return [ordered]@{
        type='campfire-routine-write-response-v1'; request_id=$RequestId; status=$Status; aperture='framework-relay'
        operation=$operation; action_id=[string](Safe-Property $Request 'action_id' ''); created_at_utc=[DateTime]::UtcNow.ToString('o')
        reason=$Reason; data=$Data
        boundaries=[ordered]@{
            one_action_per_request=$true; remote_batches=$false
            top_level_post=($operation -eq 'POST'); reviewed_high_reach_post=($operation -eq 'POST')
            human_operator_trigger_required_for_post=$false
            comment_requires_routine_enable=$true; post_requires_routine_enable=$false
            money_or_treasury=$false; credential_operation=$false; grant_mutation=$false; cursor_ack=$false
            correction_debt_closure=$false; cc_ingress=$false; full_quick_loaded=$false; square_retry=$false
            standing_grant_and_fresh_second_aperture_review_required_for_post=$true
            route_identity_is_not_runtime_identity=$true
        }
    }
}

function Write-HeadlessWriteStatus([string]$RequestId, [string]$Status, $Response = $null, $Data = $null) {
    if ([string]::IsNullOrWhiteSpace($RequestId)) { return }
    New-Item -ItemType Directory -Force -Path $WriteRelayStatusDir | Out-Null
    $row = [ordered]@{
        status_version = 'campfire-routine-write-worker-status-v1'
        request_id = $RequestId
        status = $Status
        worker_pid = $PID
        updated_at_utc = [DateTime]::UtcNow.ToString('o')
        response = $Response
        data = $Data
    }
    Write-Utf8NoBom (Get-WriteRelayRequestStatusPath $RequestId) ($row | ConvertTo-Json -Depth 60)
}

function Convert-WriteRelayRequestToAction($Request) {
    $operation=[string](Safe-Property $Request 'operation' '')
    if ($operation -eq 'COMMENT') {
        return [pscustomobject][ordered]@{
            id=[string](Safe-Property $Request 'action_id' ''); type='comment'; post_id=[int](Safe-Property $Request 'post_id' 0)
            parent_id=$null; body=[string](Safe-Property $Request 'body' ''); reason=[string](Safe-Property $Request 'reason' '')
        }
    }
    if ($operation -eq 'POST') {
        return [pscustomobject][ordered]@{
            id=[string](Safe-Property $Request 'action_id' ''); type='post'; title=[string](Safe-Property $Request 'title' '')
            body=[string](Safe-Property $Request 'body' ''); reason=[string](Safe-Property $Request 'reason' '')
            high_reach_review=Safe-Property $Request 'high_reach_review' $null
        }
    }
    throw 'REMOTE ACTION COMPILE FAILED: operation must be COMMENT or POST.'
}

function New-RemoteRoutineVirtualPlan($Request, $Action) {
    return [pscustomobject][ordered]@{
        plan_version = 'remote-routine-v1'
        citizen = 'framework-relay'
        created_by = 'Framework bounded routine write relay'
        requires_operator_trigger = $false
        remote_standing_grant_transport = $true
        request_id = [string](Safe-Property $Request 'request_id' '')
        expected_grant_id = [string](Safe-Property $Request 'expected_grant_id' '')
        expected_grant_sha256 = [string](Safe-Property $Request 'expected_grant_sha256' '')
        actions = @($Action)
        local_actions = @()
        requested_post_ids = @()
    }
}

function Preflight-RemoteRoutineAction($Request, $Action, [string]$RawCarrierSha256) {
    if ($ExpectedCitizen -ne 'framework-relay' -or $ActiveRole -ne 'Framework') { throw 'REMOTE ACTION APERTURE FAILED: worker is not Framework / framework-relay.' }
    $grant=Get-ActiveGrant; $grantSha=Get-ActiveGrantSha256
    $expectedGrantSha=[string](Safe-Property $Request 'expected_grant_sha256' '')
    $expectedGrantId=[string](Safe-Property $Request 'expected_grant_id' '')
    if ($grantSha -ne $expectedGrantSha) { throw "REMOTE ACTION GRANT SHA MISMATCH: request expected $expectedGrantSha but local grant is $grantSha." }
    if ([string](Safe-Property $grant 'grant_id' '') -ne $expectedGrantId) { throw "REMOTE ACTION GRANT ID MISMATCH: request expected '$expectedGrantId'." }
    $routine=@(Safe-Property $grant 'routine_actions' @() | ForEach-Object { [string]$_ })
    $higher=@(Safe-Property $grant 'higher_reach_actions' @() | ForEach-Object { [string]$_ })
    $type=[string](Safe-Property $Action 'type' '')

    $virtualPlan=New-RemoteRoutineVirtualPlan $Request $Action
    if ($type -eq 'comment') {
        if ('comment' -notin $routine) { throw 'REMOTE ROUTINE GRANT FAILED: comment is not presently granted.' }
        $openDebts=@(Get-OpenCorrectionDebts); $openInvestigations=@(Get-OpenWitnessInvestigations)
        if ($openDebts.Count -gt 0 -or $openInvestigations.Count -gt 0) { throw "REMOTE ROUTINE OBLIGATION BLOCK: open correction debts=$($openDebts.Count), open witness investigations=$($openInvestigations.Count)." }
    }
    elseif ($type -eq 'post') {
        if ('post' -notin $higher) { throw 'REMOTE HIGH-REACH GRANT FAILED: post is not presently granted as a higher-reach action.' }
        $shapeErrors=@(Validate-PlanShape $virtualPlan)
        if ($shapeErrors.Count -gt 0) { throw ('REMOTE HIGH-REACH REVIEW/SHAPE FAILED: ' + ($shapeErrors -join '; ')) }
    }
    else { throw "REMOTE ACTION TYPE FAILED: '$type'." }

    Assert-PlanActionIdsUnspent $virtualPlan
    $planHash=Get-PlanHash $virtualPlan
    $live=Capture-State; $me=Safe-Property $live 'me' $null
    if ([string](Safe-Property $me 'handle' '') -ne 'framework-relay') { throw "REMOTE ACTION IDENTITY FAILED: server returned '$([string](Safe-Property $me 'handle' ''))'." }
    $today=Safe-Property $me 'today' $null
    if ($type -eq 'comment') {
        if ([int](Safe-Property $today 'comments_remaining' 0) -lt 1) { throw 'REMOTE ROUTINE QUOTA FAILED: no comments remaining.' }
        $postId=[int](Safe-Property $Action 'post_id' 0); [void](Get-Thread $postId)
        if ($null -ne (Safe-Property $Action 'parent_id' $null)) { throw 'REMOTE ROUTINE TARGET FAILED: automated comments are post-level only.' }
        if (@($Action.PSObject.Properties.Name) -contains 'closes_correction_debt_id') { throw 'REMOTE ROUTINE REFUSED: correction-debt closure is outside this lane.' }
    } else {
        if ([int](Safe-Property $today 'posts_remaining' 0) -lt 1) { throw 'REMOTE HIGH-REACH QUOTA FAILED: no posts remaining.' }
    }
    return [pscustomobject][ordered]@{ ok=$true; grant=$grant; grant_sha256=$grantSha; live=$live; me=$me; virtual_plan=$virtualPlan; virtual_plan_hash=$planHash; raw_carrier_sha256=$RawCarrierSha256 }
}

function Invoke-RemoteRoutineWrite($Envelope, [string]$RawCarrierSha256) {
    $request=Safe-Property $Envelope 'request' $null
    if ($null -eq $request) { throw 'REMOTE ACTION REQUEST FILE FAILED: missing request object.' }
    if ([string](Safe-Property $request 'type' '') -ne 'campfire-routine-write-request-v1') { throw 'REMOTE ACTION REQUEST FILE FAILED: wrong type.' }
    if ([string](Safe-Property $request 'aperture' '') -ne 'framework-relay') { throw 'REMOTE ACTION REQUEST FILE FAILED: aperture must be framework-relay.' }
    if ([bool](Safe-Property $request 'cursor_ack' $true)) { throw 'REMOTE ACTION REQUEST FILE FAILED: cursor_ack must be false.' }
    $requestId=[string](Safe-Property $request 'request_id' '')
    if ($requestId -ne $HeadlessWriteRequestId -or $requestId -notmatch '^fw-write-[A-Za-z0-9._:-]{1,100}$') { throw 'REMOTE ACTION REQUEST FILE FAILED: request id mismatch.' }
    $action=Convert-WriteRelayRequestToAction $request
    $preflight=$null
    try {
        $preflight=Preflight-RemoteRoutineAction $request $action $RawCarrierSha256
        [void](Append-Event 'REMOTE_ROUTINE_PREFLIGHT_PASSED' ([pscustomobject]@{
            request_id=$requestId; action_id=[string](Safe-Property $action 'id' ''); action_type=[string](Safe-Property $action 'type' '')
            virtual_plan_hash=$preflight.virtual_plan_hash; raw_request_carrier_sha256=$RawCarrierSha256
            grant_id=[string](Safe-Property $preflight.grant 'grant_id' ''); grant_sha256=$preflight.grant_sha256
            source_comment_id=Safe-Property $Envelope 'source_comment_id' $null; source_comment_body_sha256=Safe-Property $Envelope 'source_comment_body_sha256' $null
        }) ([pscustomobject]@{ active_aperture='framework-relay'; active_role='Framework'; local_operator_trigger=$false; remote_standing_grant_transport=$true; content_endorsement_by_local_operator=$false; route_identity_is_not_runtime_identity=$true }))
    }
    catch {
        [void](Append-Event 'REMOTE_ROUTINE_PREFLIGHT_FAILED' ([pscustomobject]@{ request_id=$requestId; action_id=[string](Safe-Property $action 'id' ''); reason=$_.Exception.Message; raw_request_carrier_sha256=$RawCarrierSha256 }) ([pscustomobject]@{ square_write=$false; cursor_ack=$false; remote_standing_grant_transport=$true }))
        return [pscustomobject][ordered]@{ status='REFUSED'; write_occurred=$false; reason=$_.Exception.Message; response=$null; witness=$null; virtual_plan_hash=$null; grant_sha256=$null }
    }

    $type=[string](Safe-Property $action 'type' ''); $id=[string](Safe-Property $action 'id' '')
    [void](Append-Event 'REMOTE_STANDING_GRANT_TRIGGERED' ([pscustomobject]@{
        request_id=$requestId; action_id=$id; action_type=$type; grant_id=[string](Safe-Property $preflight.grant 'grant_id' '')
        grant_sha256=$preflight.grant_sha256; virtual_plan_hash=$preflight.virtual_plan_hash; raw_request_carrier_sha256=$RawCarrierSha256
        trigger_surface="private $ReadRelayRepo issue #$WriteRelayIssueNumber"; content_endorsement=$false
    }) ([pscustomobject]@{ local_operator_trigger=$false; explicit_local_bridge_enable_required=($type -eq 'comment'); reviewed_high_reach_post=($type -eq 'post'); active_aperture='framework-relay'; active_role='Framework' }))

    $record=[ordered]@{ attempted_at_utc=[DateTime]::UtcNow.ToString('o'); aperture_role='Framework'; plan_hash=$preflight.virtual_plan_hash; raw_plan_file_sha256=$RawCarrierSha256; grant_sha256=$preflight.grant_sha256; remote_request_id=$requestId; action_id=$id; type=$type; citizen='framework-relay'; request=$null; result=$null; write_success=$false; witness_status='NOT_RUN'; remote_standing_grant_transport=$true }
    $writeAttempted=$false; $squareReceiptReceived=$false
    try {
        if ($type -eq 'comment') {
            $payload=[ordered]@{ post_id=[int](Safe-Property $action 'post_id' 0); parent_id=$null; body=[string](Safe-Property $action 'body' '') }
            $record.request=[ordered]@{ route='/api/comment'; body=$payload }
        } elseif ($type -eq 'post') {
            $payload=[ordered]@{ title=[string](Safe-Property $action 'title' ''); body=[string](Safe-Property $action 'body' '') }
            $record.request=[ordered]@{ route='/api/post'; body=$payload }
        } else { throw "REMOTE ACTION EXECUTION FAILED: unsupported '$type'." }
        $writeAttempted=$true
        $squareResponse=Invoke-SquarePost $record.request.route $record.request.body
        $squareReceiptReceived=$true; $record.result=$squareResponse; $record.write_success=$true
        [void](Append-Event 'ACTUATED' ([pscustomobject]@{ plan_hash=$preflight.virtual_plan_hash; raw_plan_file_sha256=$RawCarrierSha256; action_id=$id; action_type=$type; request=$record.request; response=$squareResponse; remote_request_id=$requestId; remote_standing_grant_transport=$true }) ([pscustomobject]@{ write_route=$record.request.route; attempted_at_utc=$record.attempted_at_utc; active_aperture='framework-relay'; active_role='Framework'; grant_sha256=$preflight.grant_sha256; local_operator_trigger=$false }))
        $witness=Witness-Action $action $squareResponse $preflight.me $preflight.virtual_plan_hash $RawCarrierSha256
        $record.witness_status=[string](Safe-Property $witness 'status' 'UNVERIFIED'); Append-ActuationLog ([pscustomobject]$record); Capture-State | Out-Null
        if ([string](Safe-Property $witness 'status' '') -ne 'VERIFIED') {
            Disable-WriteRelay
            return [pscustomobject][ordered]@{ status='WRITE_OCCURRED_UNVERIFIED'; write_occurred=$true; reason='Square write returned but read-after-write witness did not verify. Framework write circuit disabled.'; response=$squareResponse; witness=$witness; virtual_plan_hash=$preflight.virtual_plan_hash; grant_sha256=$preflight.grant_sha256 }
        }
        return [pscustomobject][ordered]@{ status='VERIFIED'; write_occurred=$true; reason=$null; response=$squareResponse; witness=$witness; virtual_plan_hash=$preflight.virtual_plan_hash; grant_sha256=$preflight.grant_sha256 }
    }
    catch {
        $failureReason=$_.Exception.Message; $record.result=[ordered]@{ error=$failureReason }; $record.write_success=[bool]$squareReceiptReceived
        try { Append-ActuationLog ([pscustomobject]$record) } catch { }
        try { [void](Append-Event 'ACT_FAILED' ([pscustomobject]@{ plan_hash=$preflight.virtual_plan_hash; raw_plan_file_sha256=$RawCarrierSha256; action_id=$id; action_type=$type; error=$failureReason; remote_request_id=$requestId; remote_standing_grant_transport=$true; square_post_attempted=[bool]$writeAttempted; square_receipt_received=[bool]$squareReceiptReceived; write_outcome_unknown=([bool]$writeAttempted -and -not [bool]$squareReceiptReceived) }) ([pscustomobject]@{ active_aperture='framework-relay'; active_role='Framework'; grant_sha256=$preflight.grant_sha256; square_retry=$false })) } catch { }
        if ($squareReceiptReceived) { Disable-WriteRelay; return [pscustomobject][ordered]@{ status='WRITE_OCCURRED_UNVERIFIED'; write_occurred=$true; reason=$failureReason; response=$null; witness=$null; virtual_plan_hash=$preflight.virtual_plan_hash; grant_sha256=$preflight.grant_sha256 } }
        if ($writeAttempted) { Disable-WriteRelay; return [pscustomobject][ordered]@{ status='OUTCOME_UNKNOWN'; write_occurred=$null; reason=$failureReason; response=$null; witness=$null; virtual_plan_hash=$preflight.virtual_plan_hash; grant_sha256=$preflight.grant_sha256 } }
        return [pscustomobject][ordered]@{ status='FAILED_NO_WRITE'; write_occurred=$false; reason=$failureReason; response=$null; witness=$null; virtual_plan_hash=$preflight.virtual_plan_hash; grant_sha256=$preflight.grant_sha256 }
    }
}

function Invoke-HeadlessRoutineWriteRequest {
    if (-not $HeadlessWrite) { return }
    if ($HeadlessCitizen -eq 'cc-relay') { return Invoke-CcHeadlessRoutineWriteRequest }
    if ($HeadlessCitizen -ne 'framework-relay') { throw 'Headless routine write is fixed to a known relay citizen.' }
    if (-not $HeadlessWritePostResponse) { throw 'Headless routine write requires the private response carrier.' }
    if ($HeadlessWriteRequestId -notmatch '^fw-write-[A-Za-z0-9._:-]{1,100}$') { throw 'Headless routine write request id is invalid.' }
    if ([string]::IsNullOrWhiteSpace($HeadlessWriteRequestPath) -or -not (Test-Path -LiteralPath $HeadlessWriteRequestPath)) {
        throw 'Headless routine write request carrier is unavailable.'
    }

    Set-ActiveProfile 'framework-relay'
    New-Item -ItemType Directory -Force -Path $WriteRelayStatusDir | Out-Null
    $rawCarrierSha = Get-Sha256File $HeadlessWriteRequestPath
    $envelope = Read-Utf8JsonFile $HeadlessWriteRequestPath
    $request = Safe-Property $envelope 'request' $null
    if ([string](Safe-Property $request 'request_id' '') -ne $HeadlessWriteRequestId) { throw 'Headless routine write request carrier id mismatch.' }

    Write-HeadlessWriteStatus $HeadlessWriteRequestId 'STARTED' $null ([pscustomobject]@{
        carrier_sha256 = $rawCarrierSha
        source_comment_id = Safe-Property $envelope 'source_comment_id' $null
    })

    $result = Invoke-RemoteRoutineWrite $envelope $rawCarrierSha
    $responseData = [ordered]@{
        write_occurred = Safe-Property $result 'write_occurred' $null
        square_response = Safe-Property $result 'response' $null
        witness_status = [string](Safe-Property (Safe-Property $result 'witness' $null) 'status' '')
        witness_event_id = Safe-Property (Safe-Property $result 'witness' $null) 'event_id' $null
        virtual_plan_hash = Safe-Property $result 'virtual_plan_hash' $null
        raw_request_carrier_sha256 = $rawCarrierSha
        source_comment_id = Safe-Property $envelope 'source_comment_id' $null
        source_comment_body_sha256 = Safe-Property $envelope 'source_comment_body_sha256' $null
        grant_sha256 = Safe-Property $result 'grant_sha256' $null
        campfire_square_source_sha256 = if (-not [string]::IsNullOrWhiteSpace([string]$PSCommandPath)) { Get-Sha256File $PSCommandPath } else { $null }
    }
    $response = New-WriteRelayResponse $HeadlessWriteRequestId ([string]$result.status) $request $responseData ([string](Safe-Property $result 'reason' ''))

    try {
        $posted = Post-WriteRelayCommentJson $response
        $commentId = Safe-Property $posted 'id' $null
        [void](Write-WriteRelayLedgerEvent 'WRITE_RELAY_RESPONSE_POSTED' ([pscustomobject]@{
            request_id = $HeadlessWriteRequestId
            status = [string]$result.status
            response_comment_id = $commentId
            write_occurred = Safe-Property $result 'write_occurred' $null
            square_retry = $false
        }))
        Write-HeadlessWriteStatus $HeadlessWriteRequestId ([string]$result.status) $response ([pscustomobject]@{
            response_comment_id = $commentId
            response_transport = 'POSTED'
        })
    }
    catch {
        Write-HeadlessWriteStatus $HeadlessWriteRequestId 'RESPONSE_TRANSPORT_FAILED' $response ([pscustomobject]@{
            intended_status = [string]$result.status
            reason = $_.Exception.Message
            recovery_may_post_response_only = $true
            square_retry = $false
        })
        throw
    }
    return [string]$result.status
}

function Invoke-WriteRelayPoll {
    if ($script:WriteRelayPollInProgress) { return }
    $cfg = Get-WriteRelayConfig
    $dispatchEnabled = [bool](Safe-Property $cfg 'enabled' $false)
    $script:WriteRelayPollInProgress = $true
    try {
        $state = Get-WriteRelayState
        $activeRequest = [string](Safe-Property $state 'active_request_id' '')
        if (-not [string]::IsNullOrWhiteSpace($activeRequest)) {
            $statusPath = Get-WriteRelayRequestStatusPath $activeRequest
            if (Test-Path -LiteralPath $statusPath) {
                try { $workerStatus = Read-Utf8JsonFile $statusPath } catch { $workerStatus = $null }
                $terminal = [string](Safe-Property $workerStatus 'status' '')
                if ($terminal -eq 'RESPONSE_TRANSPORT_FAILED') {
                    $storedResponse = Safe-Property $workerStatus 'response' $null
                    try {
                        if ($null -eq $storedResponse) { throw 'No stored response is available for evidence-transport recovery.' }
                        $posted = Post-WriteRelayCommentJson $storedResponse
                        try { [void](Write-WriteRelayLedgerEvent 'WRITE_RELAY_RESPONSE_TRANSPORT_RECOVERED' ([pscustomobject]@{
                            request_id = $activeRequest
                            response_comment_id = Safe-Property $posted 'id' $null
                            square_retry = $false
                            recovery_scope = 'GitHub evidence response only'
                        })) } catch { }
                    }
                    catch {
                        try { [void](Write-WriteRelayLedgerEvent 'WRITE_RELAY_RESPONSE_TRANSPORT_RECOVERY_FAILED' ([pscustomobject]@{
                            request_id = $activeRequest; reason = $_.Exception.Message; square_retry = $false
                        })) } catch { }
                        Disable-WriteRelay
                    }
                    $state.active_request_id = $null
                    $state.active_worker_pid = $null
                    $state.active_started_at_utc = $null
                    $state.active_dispatch_phase = $null
                    [void](Set-WriteRelayState $state)
                    return
                }
                if (@('VERIFIED','REFUSED','FAILED_NO_WRITE','WRITE_OCCURRED_UNVERIFIED','OUTCOME_UNKNOWN') -contains $terminal) {
                    if (@('WRITE_OCCURRED_UNVERIFIED','OUTCOME_UNKNOWN') -contains $terminal) { Disable-WriteRelay }
                    $state.active_request_id = $null
                    $state.active_worker_pid = $null
                    $state.active_started_at_utc = $null
                    $state.active_dispatch_phase = $null
                    [void](Set-WriteRelayState $state)
                }
                else { return }
            }
            else {
                $pid = [int](Safe-Property $state 'active_worker_pid' 0)
                if ($pid -gt 0 -and $null -ne (Get-Process -Id $pid -ErrorAction SilentlyContinue)) { return }

                # A request is durably armed before its worker starts. If PID persistence
                # failed after launch, allow the worker time to create its own status
                # rather than racing it into a false no-write conclusion.
                $startedRaw = [string](Safe-Property $state 'active_started_at_utc' '')
                $ageSeconds = 999999
                if (-not [string]::IsNullOrWhiteSpace($startedRaw)) {
                    try { $ageSeconds = ([DateTime]::UtcNow - ([DateTimeOffset]::Parse($startedRaw).UtcDateTime)).TotalSeconds } catch { }
                }
                if ($pid -le 0 -and $ageSeconds -lt 120) { return }

                try { [void](Write-WriteRelayLedgerEvent 'WRITE_RELAY_OUTCOME_UNKNOWN' ([pscustomobject]@{
                    request_id = $activeRequest
                    worker_pid = $pid
                    dispatch_phase = Safe-Property $state 'active_dispatch_phase' $null
                    reason = 'No terminal worker status is available after the dispatch grace window; Square write outcome is not inferable from transport state.'
                    square_retry = $false
                })) } catch { }
                try {
                    $unknown = New-WriteRelayResponse $activeRequest 'OUTCOME_UNKNOWN' $null ([ordered]@{ write_occurred=$null }) 'No terminal worker status after dispatch grace window; no Square retry attempted. Bridge disabled.'
                    [void](Post-WriteRelayCommentJson $unknown)
                } catch { }
                Disable-WriteRelay
                $state.active_request_id = $null
                $state.active_worker_pid = $null
                $state.active_started_at_utc = $null
                $state.active_dispatch_phase = $null
                [void](Set-WriteRelayState $state)
                return
            }
        }

        $complete = Get-WriteRelayIssueCommentsComplete
        if (-not [bool](Safe-Property $complete 'retrieval_complete' $false)) {
            try { [void](Write-WriteRelayLedgerEvent 'WRITE_RELAY_RETRIEVAL_INCOMPLETE' ([pscustomobject]@{
                returned_count = Safe-Property $complete 'returned_count' $null
                known_total = Safe-Property $complete 'known_total' $null
                no_negative_conclusion = $true
            })) } catch { }
            return
        }

        $state = Get-WriteRelayState
        $highWater = [int64](Safe-Property $state 'last_complete_comment_id' 0)
        $newComments = @(
            @(Safe-Property $complete 'comments' @()) |
            Where-Object { [int64](Safe-Property $_ 'id' 0) -gt $highWater } |
            Sort-Object @{Expression={ [int64](Safe-Property $_ 'id' 0) }; Ascending=$true}
        )
        foreach ($comment in $newComments) {
            $commentId = [int64](Safe-Property $comment 'id' 0)
            $rawBody = [string](Safe-Property $comment 'body' '')
            $rejectedRequestId = ''
            $rejectedRequest = $null
            try {
                if (-not [string]::IsNullOrWhiteSpace($rawBody) -and $rawBody.TrimStart().StartsWith('{')) {
                    $probe = $rawBody | ConvertFrom-Json
                    if ([string](Safe-Property $probe 'type' '') -eq 'campfire-routine-write-request-v1') {
                        $rejectedRequestId = [string](Safe-Property $probe 'request_id' '')
                        $rejectedRequest = $probe
                    }
                }
            } catch { }

            $envelope = $null
            try { $envelope = ConvertTo-WriteRelayRequest $comment }
            catch {
                $refusalReason = $_.Exception.Message
                try { [void](Write-WriteRelayLedgerEvent 'WRITE_RELAY_REQUEST_REFUSED' ([pscustomobject]@{
                    request_id = if ($rejectedRequestId -match '^fw-write-[A-Za-z0-9._:-]{1,100}$') { $rejectedRequestId } else { $null }
                    source_comment_id = $commentId
                    reason = $refusalReason
                    square_write = $false
                })) } catch { }
                if ($rejectedRequestId -match '^fw-write-[A-Za-z0-9._:-]{1,100}$') {
                    try {
                        $refused = New-WriteRelayResponse $rejectedRequestId 'REFUSED' $rejectedRequest ([ordered]@{
                            write_occurred = $false; source_comment_id = $commentId; validation_stage = 'request-envelope'
                        }) $refusalReason
                        [void](Post-WriteRelayCommentJson $refused)
                    } catch { }
                }
                $state.last_complete_comment_id = $commentId
                $state.last_complete_comment_count = [int](Safe-Property $complete 'known_total' 0)
                [void](Set-WriteRelayState $state)
                continue
            }

            if ($null -eq $envelope) {
                $state.last_complete_comment_id = $commentId
                $state.last_complete_comment_count = [int](Safe-Property $complete 'known_total' 0)
                [void](Set-WriteRelayState $state)
                continue
            }

            $request = Safe-Property $envelope 'request' $null
            $requestId = [string](Safe-Property $request 'request_id' '')
            $actionId = [string](Safe-Property $request 'action_id' '')
            $operation = [string](Safe-Property $request 'operation' '')
            if (-not $dispatchEnabled -and $operation -eq 'COMMENT') {
                try { [void](Write-WriteRelayLedgerEvent 'WRITE_RELAY_DISABLED_COMMENT_IGNORED' ([pscustomobject]@{ request_id=$requestId; source_comment_id=$commentId; square_write=$false; historical_if_later_enabled=$true })) } catch { }
                $state.last_complete_comment_id=$commentId; $state.last_complete_comment_count=[int](Safe-Property $complete 'known_total' 0); [void](Set-WriteRelayState $state)
                continue
            }
            try {
                [void](Write-WriteRelayLedgerEvent 'WRITE_RELAY_REQUEST_OBSERVED' ([pscustomobject]@{
                    request_id = $requestId; action_id = $actionId; operation = $operation
                    source_comment_id = $commentId
                    source_comment_body_sha256 = Safe-Property $envelope 'source_comment_body_sha256' $null
                    route_app_slug = $ReadRelayExpectedAppSlug
                    route_identity_is_not_runtime_identity = $true
                }))
                $requestPath = Join-Path $WriteRelayInbox ($requestId + '.json')
                Write-Utf8NoBom $requestPath ($envelope | ConvertTo-Json -Depth 30)

                # Pre-arm persistent state BEFORE launching the worker. If the GUI or
                # bookkeeping path faults after process creation, the same request can
                # never fall back into the unconsumed queue and launch twice.
                $state.last_complete_comment_id = $commentId
                $state.last_complete_comment_count = [int](Safe-Property $complete 'known_total' 0)
                $state.active_request_id = $requestId
                $state.active_worker_pid = $null
                $state.active_started_at_utc = [DateTime]::UtcNow.ToString('o')
                $state.active_dispatch_phase = 'ARMED_BEFORE_PROCESS_START'
                $state = Set-WriteRelayState $state

                $process = $null
                try { $process = Start-WriteRelayWorker $envelope $requestPath }
                catch {
                    $startReason = $_.Exception.Message
                    try {
                        $failed = New-WriteRelayResponse $requestId 'FAILED_NO_WRITE' $request ([ordered]@{
                            write_occurred = $false; source_comment_id = $commentId; dispatch_phase = 'PROCESS_START_FAILED'
                        }) $startReason
                        [void](Post-WriteRelayCommentJson $failed)
                        Write-HeadlessWriteStatus $requestId 'FAILED_NO_WRITE' $failed ([pscustomobject]@{ process_started=$false })
                    } catch { }
                    $state.active_request_id = $null
                    $state.active_worker_pid = $null
                    $state.active_started_at_utc = $null
                    $state.active_dispatch_phase = $null
                    [void](Set-WriteRelayState $state)
                    return
                }

                # PID persistence is the only required local write after process start.
                # The pre-arm survives if this update fails; the grace window then lets
                # the worker's own status file resolve the outcome without redispatch.
                try {
                    $state.active_worker_pid = $process.Id
                    $state.active_dispatch_phase = 'WORKER_STARTED'
                    $state = Set-WriteRelayState $state
                }
                catch {
                    try { [void](Write-WriteRelayLedgerEvent 'WRITE_RELAY_PID_PERSIST_FAILED' ([pscustomobject]@{
                        request_id = $requestId; worker_pid = $process.Id; reason = $_.Exception.Message; square_retry = $false
                    })) } catch { }
                    return
                }
                try { [void](Write-WriteRelayLedgerEvent 'WRITE_RELAY_REQUEST_DISPATCHED' ([pscustomobject]@{
                    request_id = $requestId; action_id = $actionId; operation = $operation
                    source_comment_id = $commentId; worker_pid = $process.Id
                    request_path_basename = [IO.Path]::GetFileName($requestPath)
                    one_action_per_request = $true; remote_batches = $false
                })) } catch { }
                return
            }
            catch {
                # This catch can only occur before worker launch because all post-launch
                # state/ledger operations above are locally contained. Therefore no
                # Square write was attempted by this request.
                $dispatchReason = $_.Exception.Message
                try {
                    $failed = New-WriteRelayResponse $requestId 'FAILED_NO_WRITE' $request ([ordered]@{
                        write_occurred = $false; source_comment_id = $commentId; dispatch_phase = 'PRE_WORKER_DISPATCH'
                    }) $dispatchReason
                    [void](Post-WriteRelayCommentJson $failed)
                } catch { }
                try { [void](Write-WriteRelayLedgerEvent 'WRITE_RELAY_DISPATCH_FAILED_NO_WRITE' ([pscustomobject]@{
                    request_id = $requestId; action_id = $actionId; source_comment_id = $commentId
                    reason = $dispatchReason; square_write = $false
                })) } catch { }
                $state.last_complete_comment_id = $commentId
                $state.last_complete_comment_count = [int](Safe-Property $complete 'known_total' 0)
                $state.active_request_id = $null
                $state.active_worker_pid = $null
                $state.active_started_at_utc = $null
                $state.active_dispatch_phase = $null
                [void](Set-WriteRelayState $state)
                return
            }
        }
    }
    catch {
        try { [void](Write-WriteRelayLedgerEvent 'WRITE_RELAY_POLL_FAILED' ([pscustomobject]@{
            reason = $_.Exception.Message; square_retry = $false
        })) } catch { }
    }
    finally { $script:WriteRelayPollInProgress = $false }
}


# ----------------------------- CC LOCAL ROUTINE WRITE RELAY -----------------
# R28 adds a separate local-filesystem routine COMMENT lane for cc-relay.
# It intentionally does not reuse Framework's GitHub ingress. The two citizens
# share the Square executable but not request carriers, state, ledgers, grants,
# credentials, action ids, responses, or circuit-breaker state.

function Write-CcWriteRelayLedgerEvent([string]$Kind, $Data = $null) {
    New-Item -ItemType Directory -Force -Path $CcWriteRelayRoot | Out-Null
    $row = [ordered]@{
        event_version = 'campfire-cc-routine-write-relay-event-v1'
        event_id = [guid]::NewGuid().ToString()
        created_at_utc = [DateTime]::UtcNow.ToString('o')
        kind = $Kind
        aperture = 'cc-relay'
        data = $Data
    }
    $line = $row | ConvertTo-Json -Depth 40 -Compress
    [System.IO.File]::AppendAllText(
        $CcWriteRelayLedgerPath,
        $line + [Environment]::NewLine,
        [System.Text.UTF8Encoding]::new($false)
    )
    return [pscustomobject]$row
}

function Get-CcWriteRelayConfig {
    if (-not (Test-Path -LiteralPath $CcWriteRelayConfigPath)) {
        return [pscustomobject][ordered]@{
            config_version = 'campfire-cc-routine-write-relay-config-v5'
            enabled = $false
            initialized = $false
            created_at_utc = $null
            updated_at_utc = $null
        }
    }
    try { return Read-Utf8JsonFile $CcWriteRelayConfigPath }
    catch { throw "CC routine write relay config cannot be parsed: $($_.Exception.Message)" }
}

function Set-CcWriteRelayConfig([bool]$Enabled, [bool]$Initialized) {
    New-Item -ItemType Directory -Force -Path $CcWriteRelayRoot | Out-Null
    $prior = Get-CcWriteRelayConfig
    $created = Safe-Property $prior 'created_at_utc' $null
    if ([string]::IsNullOrWhiteSpace([string]$created)) { $created = [DateTime]::UtcNow.ToString('o') }
    $config = [ordered]@{
        config_version = 'campfire-cc-routine-write-relay-config-v5'
        enabled = $Enabled
        initialized = $Initialized
        created_at_utc = $created
        updated_at_utc = [DateTime]::UtcNow.ToString('o')
        transport = 'LOCAL_FILESYSTEM_ONLY'
        ingress_directory = $CcWriteRelayIngress
        response_directory = $CcWriteRelayResponses
        aperture = 'cc-relay'
        allowed_operations = @('COMMENT','POST')
        post_level_only = $true
        one_action_per_request = $true
        batches = $false
        top_level_posts = 'REVIEWED_HIGH_REACH_ONLY'
        votes = $false
        cursor_ack = $false
        correction_debt_closure = $false
        money_or_treasury = $false
        credential_operations = $false
        grant_mutation = $false
        framework_ingress = $false
        full_quick = $false
        existing_full_plan_airlock_unchanged = $true
        local_enable_is_content_endorsement = $false
        semantic_content_authority = 'CC'
        comment_only_is_transport_scope_not_semantic_safety_claim = $true
        body_semantics_are_not_machine_screened_for_truth_harm_or_fitness = $true
        pre_enable_ingress_policy = 'NONEMPTY_INGRESS_REQUIRES_CC_APERTURE_DISPOSITION_BOUND_TO_EXACT_SNAPSHOT; MARK_START_IS_CAPABILITY_ONLY'
        pre_enable_disposition_carrier = 'WriteRelay\cc-relay\pre-enable-disposition.json'
        pre_enable_disposition_type = 'campfire-cc-write-pre-enable-disposition-v1'
        pre_enable_disposition_value = 'ACKNOWLEDGE_AS_HISTORICAL_DO_NOT_EXECUTE'
    }
    Write-Utf8NoBom $CcWriteRelayConfigPath ($config | ConvertTo-Json -Depth 30)
    return [pscustomobject]$config
}

function Protect-CcWriteRelayAfterR28DUpgrade {
    if (-not (Test-Path -LiteralPath $CcWriteRelayConfigPath)) { return }
    $cfg = Get-CcWriteRelayConfig
    if ([string](Safe-Property $cfg 'config_version' '') -eq 'campfire-cc-routine-write-relay-config-v5') { return }
    $wasEnabled = [bool](Safe-Property $cfg 'enabled' $false)
    $wasInitialized = [bool](Safe-Property $cfg 'initialized' $false)
    [void](Set-CcWriteRelayConfig $false $wasInitialized)
    [void](Write-CcWriteRelayLedgerEvent 'CC_WRITE_RELAY_R28E_UPGRADE_DISABLED' ([pscustomobject]@{
        prior_enabled = $wasEnabled
        reason = 'R28E repairs CC worker evidence and failure classification while preserving the existing authority boundary. Explicit START after review is required; upgrade does not preserve armed write authority.'
        square_write = $false
    }))
}

function Get-CcWriteRelayState {
    if (-not (Test-Path -LiteralPath $CcWriteRelayStatePath)) {
        return [pscustomobject][ordered]@{
            state_version = 'campfire-cc-routine-write-relay-state-v1'
            active_request_id = $null
            active_worker_pid = $null
            active_started_at_utc = $null
            active_dispatch_phase = $null
            updated_at_utc = $null
        }
    }
    try { return Read-Utf8JsonFile $CcWriteRelayStatePath }
    catch { throw "CC routine write relay state cannot be parsed: $($_.Exception.Message)" }
}

function Set-CcWriteRelayState($State) {
    New-Item -ItemType Directory -Force -Path $CcWriteRelayRoot | Out-Null
    $copy = [ordered]@{
        state_version = 'campfire-cc-routine-write-relay-state-v1'
        active_request_id = Safe-Property $State 'active_request_id' $null
        active_worker_pid = Safe-Property $State 'active_worker_pid' $null
        active_started_at_utc = Safe-Property $State 'active_started_at_utc' $null
        active_dispatch_phase = Safe-Property $State 'active_dispatch_phase' $null
        updated_at_utc = [DateTime]::UtcNow.ToString('o')
    }
    Write-Utf8NoBom $CcWriteRelayStatePath ($copy | ConvertTo-Json -Depth 20)
    return [pscustomobject]$copy
}

function Get-CcWriteRelayRequestStatusPath([string]$RequestId) {
    return Join-Path $CcWriteRelayStatusDir ($RequestId + '.json')
}

function New-CcWriteRelayWorkerStderrPath([string]$RequestId) {
    return Join-Path $CcWriteRelayStatusDir ($RequestId + '.stderr.' + [guid]::NewGuid().ToString('N') + '.txt')
}

function Test-CcWriteRelayRequestIdSeen([string]$RequestId) {
    if ([string]::IsNullOrWhiteSpace($RequestId)) { return $false }
    if (Test-Path -LiteralPath (Join-Path $CcWriteRelayResponses ($RequestId + '.response.json'))) { return $true }
    if (-not (Test-Path -LiteralPath $CcWriteRelayLedgerPath)) { return $false }
    foreach ($line in @(Read-Utf8LinesFile $CcWriteRelayLedgerPath)) {
        if ([string]::IsNullOrWhiteSpace($line)) { continue }
        try { $row = $line | ConvertFrom-Json } catch { continue }
        $data = Safe-Property $row 'data' $null
        if ([string](Safe-Property $data 'request_id' '') -eq $RequestId -and
            @('CC_WRITE_RELAY_REQUEST_DISPATCHED','CC_WRITE_RELAY_REQUEST_REFUSED','CC_WRITE_RELAY_RESPONSE_WRITTEN','CC_WRITE_RELAY_OUTCOME_UNKNOWN') -contains [string](Safe-Property $row 'kind' '')) {
            return $true
        }
    }
    return $false
}

function ConvertTo-CcWriteRelayRequestFile([string]$Path) {
    if ([string]::IsNullOrWhiteSpace($Path) -or -not (Test-Path -LiteralPath $Path)) { throw 'CC_WRITE_RELAY_REQUEST_REFUSED request file is unavailable.' }
    $file=Get-Item -LiteralPath $Path
    if ($file.Length -gt $WriteRelayRequestCharacterCeiling) { throw 'CC_WRITE_RELAY_REQUEST_REFUSED request file exceeds bounded byte ceiling.' }
    $request=Read-Utf8JsonFile $Path
    if ([string](Safe-Property $request 'type' '') -ne 'campfire-routine-write-request-v1') { throw 'CC_WRITE_RELAY_REQUEST_REFUSED wrong request type.' }
    $allowed=@('type','request_id','aperture','operation','action_id','expected_grant_id','expected_grant_sha256','reason','cursor_ack','post_id','parent_id','title','body','high_reach_review')
    foreach ($name in @($request.PSObject.Properties.Name | ForEach-Object { [string]$_ })) { if ($allowed -notcontains $name) { throw "CC_WRITE_RELAY_REQUEST_REFUSED unknown field '$name'." } }
    $requestId=[string](Safe-Property $request 'request_id' '')
    if ($requestId -notmatch '^cc-write-[A-Za-z0-9._:-]{1,100}$') { throw 'CC_WRITE_RELAY_REQUEST_REFUSED invalid request_id.' }
    if (Test-CcWriteRelayRequestIdSeen $requestId) { throw 'CC_WRITE_RELAY_REQUEST_REFUSED request_id already consumed.' }
    if ([string](Safe-Property $request 'aperture' '') -ne 'cc-relay') { throw 'CC_WRITE_RELAY_REQUEST_REFUSED aperture must be cc-relay.' }
    if ([bool](Safe-Property $request 'cursor_ack' $true)) { throw 'CC_WRITE_RELAY_REQUEST_REFUSED cursor_ack must be false.' }
    $operation=[string](Safe-Property $request 'operation' '')
    if ($operation -notin @('COMMENT','POST')) { throw 'CC_WRITE_RELAY_REQUEST_REFUSED operation must be COMMENT or POST.' }
    $actionId=[string](Safe-Property $request 'action_id' '')
    if ($actionId -notmatch '^cc-action-[A-Za-z0-9._:-]{1,120}$') { throw 'CC_WRITE_RELAY_REQUEST_REFUSED invalid action_id.' }
    $expectedGrantId=[string](Safe-Property $request 'expected_grant_id' '')
    if ([string]::IsNullOrWhiteSpace($expectedGrantId) -or $expectedGrantId.Length -gt 240) { throw 'CC_WRITE_RELAY_REQUEST_REFUSED expected_grant_id is required.' }
    $expectedGrantSha=[string](Safe-Property $request 'expected_grant_sha256' '')
    if ($expectedGrantSha -notmatch '^[0-9a-f]{64}$') { throw 'CC_WRITE_RELAY_REQUEST_REFUSED expected_grant_sha256 must be lowercase SHA-256.' }
    $reason=[string](Safe-Property $request 'reason' '')
    if ([string]::IsNullOrWhiteSpace($reason) -or $reason.Length -gt 4000) { throw 'CC_WRITE_RELAY_REQUEST_REFUSED bounded reason is required.' }
    if ($operation -eq 'COMMENT') {
        $postId=[int](Safe-Property $request 'post_id' 0); if ($postId -le 0) { throw 'CC_WRITE_RELAY_REQUEST_REFUSED COMMENT post_id must be positive.' }
        if ($null -ne (Safe-Property $request 'parent_id' $null)) { throw 'CC_WRITE_RELAY_REQUEST_REFUSED COMMENT parent_id must be null/absent.' }
        $body=[string](Safe-Property $request 'body' ''); if ([string]::IsNullOrWhiteSpace($body) -or $body.Length -gt 12000) { throw 'CC_WRITE_RELAY_REQUEST_REFUSED bounded comment body is required.' }
        if (@($request.PSObject.Properties.Name) -contains 'title' -or @($request.PSObject.Properties.Name) -contains 'high_reach_review') { throw 'CC_WRITE_RELAY_REQUEST_REFUSED COMMENT must not carry POST title/review fields.' }
    } else {
        if (@($request.PSObject.Properties.Name) -contains 'post_id' -or @($request.PSObject.Properties.Name) -contains 'parent_id') { throw 'CC_WRITE_RELAY_REQUEST_REFUSED POST must not carry comment target fields.' }
        $title=[string](Safe-Property $request 'title' ''); $body=[string](Safe-Property $request 'body' '')
        if ($title.Length -lt 3 -or $title.Length -gt 120) { throw 'CC_WRITE_RELAY_REQUEST_REFUSED POST title must be 3-120 characters.' }
        if ([string]::IsNullOrWhiteSpace($body) -or $body.Length -gt 8000) { throw 'CC_WRITE_RELAY_REQUEST_REFUSED POST body must be 1-8000 characters.' }
        if ($null -eq (Safe-Property $request 'high_reach_review' $null)) { throw 'CC_WRITE_RELAY_REQUEST_REFUSED POST requires high_reach_review.' }
    }
    return $request
}

function Move-CcWriteRelayRequestFile([string]$Path, [string]$Bucket) {
    if (-not (Test-Path -LiteralPath $Path)) { return $null }
    $destinationDir = Join-Path $CcWriteRelayArchive $Bucket
    New-Item -ItemType Directory -Force -Path $destinationDir | Out-Null
    $name = [IO.Path]::GetFileName($Path)
    $destination = Join-Path $destinationDir $name
    if (Test-Path -LiteralPath $destination) {
        $destination = Join-Path $destinationDir (([IO.Path]::GetFileNameWithoutExtension($name)) + '-' + [guid]::NewGuid().ToString('N') + '.json')
    }
    Move-Item -LiteralPath $Path -Destination $destination -Force
    return $destination
}

function Write-CcWriteRelayResponseFile([string]$RequestId, $Response) {
    New-Item -ItemType Directory -Force -Path $CcWriteRelayResponses | Out-Null
    $path = Join-Path $CcWriteRelayResponses ($RequestId + '.response.json')
    Write-Utf8NoBom $path ($Response | ConvertTo-Json -Depth 60)
    return $path
}

function Get-CcWriteRelayPreEnableSnapshot {
    New-Item -ItemType Directory -Force -Path $CcWriteRelayIngress | Out-Null
    $files = @(Get-ChildItem -LiteralPath $CcWriteRelayIngress -Filter '*.json' -File -ErrorAction SilentlyContinue | Sort-Object Name)
    $rows = [System.Collections.Generic.List[object]]::new()
    foreach ($file in $files) {
        $rows.Add([pscustomobject][ordered]@{
            name = $file.Name
            bytes = [int64]$file.Length
            sha256 = Get-Sha256File $file.FullName
        })
    }
    $snapshotJson = @($rows.ToArray()) | ConvertTo-Json -Depth 10 -Compress
    return [pscustomobject][ordered]@{
        count = $files.Count
        snapshot_sha256 = Get-Sha256Text $snapshotJson
        files = @($rows.ToArray())
    }
}

function Get-CcWriteRelayPreEnableReview {
    if (-not (Test-Path -LiteralPath $CcWriteRelayPreEnableReviewPath)) { return $null }
    try { return Read-Utf8JsonFile $CcWriteRelayPreEnableReviewPath }
    catch { throw "CC pre-enable ingress review cannot be parsed: $($_.Exception.Message)" }
}

function Get-CcWriteRelayPreEnableDisposition {
    if (-not (Test-Path -LiteralPath $CcWriteRelayPreEnableDispositionPath)) { return $null }
    try { return Read-Utf8JsonFile $CcWriteRelayPreEnableDispositionPath }
    catch { throw "CC pre-enable disposition cannot be parsed: $($_.Exception.Message)" }
}

function Write-CcWriteRelayPreEnableReview($Snapshot) {
    $review = [ordered]@{
        review_version = 'campfire-cc-write-pre-enable-review-v2'
        status = 'APERTURE_DISPOSITION_REQUIRED'
        created_at_utc = [DateTime]::UtcNow.ToString('o')
        review_id = 'cc-pre-enable-' + [guid]::NewGuid().ToString('N')
        snapshot_sha256 = [string](Safe-Property $Snapshot 'snapshot_sha256' '')
        file_count = [int](Safe-Property $Snapshot 'count' 0)
        files = @(Safe-Property $Snapshot 'files' @())
        required_disposition = 'ACKNOWLEDGE_AS_HISTORICAL_DO_NOT_EXECUTE'
        disposition_carrier = 'WriteRelay\cc-relay\pre-enable-disposition.json'
        authority_split = 'CC aperture supplies semantic disposition; Mark START supplies capability enablement only.'
        provenance_ceiling = 'A local cc-relay disposition carrier binds the configured aperture lane; it is not cryptographic proof of a particular runtime identity.'
    }
    Write-Utf8NoBom $CcWriteRelayPreEnableReviewPath ($review | ConvertTo-Json -Depth 20)
    return [pscustomobject]$review
}

function Test-CcWriteRelayPreEnableDisposition($Disposition, $Snapshot, $Review) {
    if ($null -eq $Disposition) { return $false }
    return (
        [string](Safe-Property $Disposition 'type' '') -eq 'campfire-cc-write-pre-enable-disposition-v1' -and
        [string](Safe-Property $Disposition 'aperture' '') -eq 'cc-relay' -and
        [string](Safe-Property $Disposition 'disposition' '') -eq 'ACKNOWLEDGE_AS_HISTORICAL_DO_NOT_EXECUTE' -and
        $null -ne $Review -and
        [string](Safe-Property $Disposition 'review_id' '') -eq [string](Safe-Property $Review 'review_id' '') -and
        [string](Safe-Property $Disposition 'snapshot_sha256' '') -eq [string](Safe-Property $Snapshot 'snapshot_sha256' '')
    )
}

function Assert-CcWriteRelayPreEnableIngressDisposition {
    $snapshot = Get-CcWriteRelayPreEnableSnapshot
    if ([int](Safe-Property $snapshot 'count' 0) -eq 0) {
        if (Test-Path -LiteralPath $CcWriteRelayPreEnableReviewPath) {
            Remove-Item -LiteralPath $CcWriteRelayPreEnableReviewPath -Force
            [void](Write-CcWriteRelayLedgerEvent 'CC_WRITE_RELAY_PRE_ENABLE_REVIEW_CLEARED_EMPTY' ([pscustomobject]@{ square_write=$false }))
        }
        return
    }

    $prior = Get-CcWriteRelayPreEnableReview
    $sameReview = ($null -ne $prior -and
        [string](Safe-Property $prior 'snapshot_sha256' '') -eq [string](Safe-Property $snapshot 'snapshot_sha256' '') -and
        [int](Safe-Property $prior 'file_count' -1) -eq [int](Safe-Property $snapshot 'count' -2))

    if (-not $sameReview) {
        [void](Write-CcWriteRelayPreEnableReview $snapshot)
        foreach ($row in @(Safe-Property $snapshot 'files' @())) {
            [void](Write-CcWriteRelayLedgerEvent 'CC_WRITE_RELAY_PRE_ENABLE_FILE_REQUIRES_APERTURE_DISPOSITION' ([pscustomobject]@{
                file_name = [string](Safe-Property $row 'name' '')
                file_sha256 = [string](Safe-Property $row 'sha256' '')
                file_bytes = [int64](Safe-Property $row 'bytes' 0)
                snapshot_sha256 = [string](Safe-Property $snapshot 'snapshot_sha256' '')
                square_write = $false
            }))
        }
        [void](Write-CcWriteRelayLedgerEvent 'CC_WRITE_RELAY_PRE_ENABLE_APERTURE_DISPOSITION_REQUIRED' ([pscustomobject]@{
            file_count = [int](Safe-Property $snapshot 'count' 0)
            snapshot_sha256 = [string](Safe-Property $snapshot 'snapshot_sha256' '')
            review_id = [string](Safe-Property (Get-CcWriteRelayPreEnableReview) 'review_id' '')
            required_disposition = 'ACKNOWLEDGE_AS_HISTORICAL_DO_NOT_EXECUTE'
            operator_start_is_capability_only = $true
            square_write = $false
        }))
        $currentReview = Get-CcWriteRelayPreEnableReview
        throw "CC WRITE ENABLE BLOCKED: $([int](Safe-Property $snapshot 'count' 0)) pre-enable ingress file(s) require a CC aperture disposition. CC must write pre-enable-disposition.json naming exact review_id '$([string](Safe-Property $currentReview 'review_id' ''))', snapshot_sha256 '$([string](Safe-Property $snapshot 'snapshot_sha256' ''))', and disposition ACKNOWLEDGE_AS_HISTORICAL_DO_NOT_EXECUTE. Mark START does not supply that semantic decision."
    }

    $disposition = Get-CcWriteRelayPreEnableDisposition
    if (-not (Test-CcWriteRelayPreEnableDisposition $disposition $snapshot $prior)) {
        [void](Write-CcWriteRelayLedgerEvent 'CC_WRITE_RELAY_PRE_ENABLE_APERTURE_DISPOSITION_MISSING_OR_MISMATCH' ([pscustomobject]@{
            file_count = [int](Safe-Property $snapshot 'count' 0)
            snapshot_sha256 = [string](Safe-Property $snapshot 'snapshot_sha256' '')
            review_id = [string](Safe-Property $prior 'review_id' '')
            disposition_present = ($null -ne $disposition)
            disposition_review_id = if ($null -ne $disposition) { [string](Safe-Property $disposition 'review_id' '') } else { $null }
            disposition_snapshot_sha256 = if ($null -ne $disposition) { [string](Safe-Property $disposition 'snapshot_sha256' '') } else { $null }
            operator_start_is_capability_only = $true
            square_write = $false
        }))
        throw "CC WRITE ENABLE BLOCKED: exact CC aperture disposition is missing or does not match the current pre-enable snapshot. Mark START is capability custody only and cannot acknowledge CC-authored staged acts."
    }

    foreach ($row in @(Safe-Property $snapshot 'files' @())) {
        $name = [string](Safe-Property $row 'name' '')
        $path = Join-Path $CcWriteRelayIngress $name
        if (-not (Test-Path -LiteralPath $path)) { throw "CC WRITE ENABLE BLOCKED: pre-enable file '$name' changed after the reviewed snapshot." }
        $actualSha = Get-Sha256File $path
        if ($actualSha -ne [string](Safe-Property $row 'sha256' '')) { throw "CC WRITE ENABLE BLOCKED: pre-enable file '$name' changed after the reviewed snapshot." }
        $archivePath = Move-CcWriteRelayRequestFile $path 'pre-enable-aperture-disposition-historical-not-executed'
        [void](Write-CcWriteRelayLedgerEvent 'CC_WRITE_RELAY_PRE_ENABLE_FILE_DISPOSITIONED_HISTORICAL_NOT_EXECUTED' ([pscustomobject]@{
            file_name = $name
            file_sha256 = $actualSha
            archived_path = $archivePath
            snapshot_sha256 = [string](Safe-Property $snapshot 'snapshot_sha256' '')
            review_id = [string](Safe-Property $prior 'review_id' '')
            semantic_disposition = 'ACKNOWLEDGE_AS_HISTORICAL_DO_NOT_EXECUTE'
            semantic_authority = 'cc-relay aperture carrier'
            operator_start_is_capability_only = $true
            square_write = $false
        }))
    }

    $dispositionArchive = Move-CcWriteRelayRequestFile $CcWriteRelayPreEnableDispositionPath 'pre-enable-aperture-dispositions'
    Remove-Item -LiteralPath $CcWriteRelayPreEnableReviewPath -Force -ErrorAction SilentlyContinue
    [void](Write-CcWriteRelayLedgerEvent 'CC_WRITE_RELAY_PRE_ENABLE_APERTURE_DISPOSITION_APPLIED' ([pscustomobject]@{
        file_count = [int](Safe-Property $snapshot 'count' 0)
        snapshot_sha256 = [string](Safe-Property $snapshot 'snapshot_sha256' '')
        review_id = [string](Safe-Property $prior 'review_id' '')
        semantic_disposition = 'ACKNOWLEDGE_AS_HISTORICAL_DO_NOT_EXECUTE'
        disposition_archive_path = $dispositionArchive
        historical_requests_are_not_executed = $true
        operator_start_is_capability_only = $true
        square_write = $false
    }))
}

function Initialize-CcWriteRelay {
    foreach ($dir in @($CcWriteRelayRoot,$CcWriteRelayIngress,$CcWriteRelayInbox,$CcWriteRelayResponses,$CcWriteRelayArchive,$CcWriteRelayStatusDir)) {
        New-Item -ItemType Directory -Force -Path $dir | Out-Null
    }
    Assert-CcWriteRelayPreEnableIngressDisposition
    $cfg = Get-CcWriteRelayConfig
    if (-not [bool](Safe-Property $cfg 'initialized' $false)) {
        [void](Set-CcWriteRelayState ([pscustomobject]@{
            active_request_id=$null; active_worker_pid=$null; active_started_at_utc=$null; active_dispatch_phase=$null
        }))
        [void](Write-CcWriteRelayLedgerEvent 'CC_WRITE_RELAY_BASELINE_ESTABLISHED' ([pscustomobject]@{
            historical_request_files_ignored = 0
            historical_requests_are_not_executed = $true
            note = 'Non-empty pre-enable ingress cannot be silently ignored. Semantic disposition must come from the cc-relay aperture carrier; Mark START remains capability custody only.'
        }))
    }
    [void](Set-CcWriteRelayConfig $true $true)
    [void](Write-CcWriteRelayLedgerEvent 'CC_WRITE_RELAY_ENABLED' ([pscustomobject]@{
        transport = 'LOCAL_FILESYSTEM_ONLY'
        ingress_directory = $CcWriteRelayIngress
        response_directory = $CcWriteRelayResponses
        aperture = 'cc-relay'
        allowed_operations = @('COMMENT','POST')
        post_level_only = $true
        semantic_content_authority = 'CC'
        comment_only_is_transport_scope_not_semantic_safety_claim = $true
        local_enable_is_content_endorsement = $false
    }))
}

function Disable-CcWriteRelay {
    $cfg = Get-CcWriteRelayConfig
    [void](Set-CcWriteRelayConfig $false ([bool](Safe-Property $cfg 'initialized' $false)))
    [void](Write-CcWriteRelayLedgerEvent 'CC_WRITE_RELAY_DISABLED' ([pscustomobject]@{
        note = 'No new CC routine write request file will be dispatched. Any already-issued Square write is never silently retried.'
        square_retry = $false
    }))
}

function Get-CcWriteRelayHumanStatus {
    $cfg = Get-CcWriteRelayConfig
    $state = Get-CcWriteRelayState
    $enabled = [bool](Safe-Property $cfg 'enabled' $false)
    $active = [string](Safe-Property $state 'active_request_id' '')
    $status = if ($enabled) { 'ENABLED' } else { 'DISABLED' }
    if (-not [string]::IsNullOrWhiteSpace($active)) { $status += " | active $active" }
    $review = $null
    try { $review = Get-CcWriteRelayPreEnableReview } catch { $status += ' | PRE-ENABLE REVIEW PARSE ERROR' }
    if ($null -ne $review) {
        $snapshotSha = [string](Safe-Property $review 'snapshot_sha256' '')
        $reviewId = [string](Safe-Property $review 'review_id' '')
        $disposition = $null
        try { $disposition = Get-CcWriteRelayPreEnableDisposition } catch { $status += ' | DISPOSITION PARSE ERROR' }
        $dispState = if ($null -ne $disposition -and [string](Safe-Property $disposition 'type' '') -eq 'campfire-cc-write-pre-enable-disposition-v1' -and [string](Safe-Property $disposition 'aperture' '') -eq 'cc-relay' -and [string](Safe-Property $disposition 'disposition' '') -eq 'ACKNOWLEDGE_AS_HISTORICAL_DO_NOT_EXECUTE' -and [string](Safe-Property $disposition 'review_id' '') -eq $reviewId -and [string](Safe-Property $disposition 'snapshot_sha256' '') -eq $snapshotSha) { 'CC DISPOSITION PRESENT' } else { 'CC DISPOSITION REQUIRED' }
        $status += " | PRE-ENABLE $dispState ($([int](Safe-Property $review 'file_count' 0)) file(s))"
    }
    return "$status | LOCAL COMMENT (routine-enable) + reviewed POST (standing higher-reach grant) | semantic content authority: CC | POST needs Framework READ_AND_CHALLENGED, not Mark RUN"
}

function Convert-CcWriteRelayRequestToAction($Request) {
    $operation=[string](Safe-Property $Request 'operation' '')
    if ($operation -eq 'COMMENT') { return [pscustomobject][ordered]@{ id=[string](Safe-Property $Request 'action_id' ''); type='comment'; post_id=[int](Safe-Property $Request 'post_id' 0); parent_id=$null; body=[string](Safe-Property $Request 'body' ''); reason=[string](Safe-Property $Request 'reason' '') } }
    if ($operation -eq 'POST') { return [pscustomobject][ordered]@{ id=[string](Safe-Property $Request 'action_id' ''); type='post'; title=[string](Safe-Property $Request 'title' ''); body=[string](Safe-Property $Request 'body' ''); reason=[string](Safe-Property $Request 'reason' ''); high_reach_review=Safe-Property $Request 'high_reach_review' $null } }
    throw 'CC REMOTE ACTION COMPILE FAILED: operation must be COMMENT or POST.'
}

function New-CcRemoteRoutineVirtualPlan($Request, $Action) {
    return [pscustomobject][ordered]@{
        plan_version = 'cc-remote-routine-v1'
        citizen = 'cc-relay'
        created_by = 'CC bounded local routine write relay'
        requires_operator_trigger = $false
        remote_standing_grant_transport = $true
        request_id = [string](Safe-Property $Request 'request_id' '')
        expected_grant_id = [string](Safe-Property $Request 'expected_grant_id' '')
        expected_grant_sha256 = [string](Safe-Property $Request 'expected_grant_sha256' '')
        actions = @($Action)
        local_actions = @()
        requested_post_ids = @()
    }
}

function Preflight-CcRemoteRoutineAction($Request, $Action, [string]$RawCarrierSha256) {
    if ($ExpectedCitizen -ne 'cc-relay' -or $ActiveRole -ne 'CC') { throw 'CC REMOTE ACTION APERTURE FAILED: worker is not CC / cc-relay.' }
    $grant=Get-ActiveGrant; $grantSha=Get-ActiveGrantSha256
    $expectedGrantSha=[string](Safe-Property $Request 'expected_grant_sha256' ''); $expectedGrantId=[string](Safe-Property $Request 'expected_grant_id' '')
    if ($grantSha -ne $expectedGrantSha) { throw "CC REMOTE ACTION GRANT SHA MISMATCH: request expected $expectedGrantSha but local grant is $grantSha." }
    if ([string](Safe-Property $grant 'grant_id' '') -ne $expectedGrantId) { throw "CC REMOTE ACTION GRANT ID MISMATCH: request expected '$expectedGrantId'." }
    $routine=@(Safe-Property $grant 'routine_actions' @() | ForEach-Object { [string]$_ }); $higher=@(Safe-Property $grant 'higher_reach_actions' @() | ForEach-Object { [string]$_ })
    $type=[string](Safe-Property $Action 'type' ''); $virtualPlan=New-CcRemoteRoutineVirtualPlan $Request $Action
    if ($type -eq 'comment') {
        if ('comment' -notin $routine) { throw 'CC REMOTE ROUTINE GRANT FAILED: comment is not presently granted.' }
        $openDebts=@(Get-OpenCorrectionDebts); $openInvestigations=@(Get-OpenWitnessInvestigations)
        if ($openDebts.Count -gt 0 -or $openInvestigations.Count -gt 0) { throw "CC REMOTE ROUTINE OBLIGATION BLOCK: open correction debts=$($openDebts.Count), open witness investigations=$($openInvestigations.Count)." }
    } elseif ($type -eq 'post') {
        if ('post' -notin $higher) { throw 'CC REMOTE HIGH-REACH GRANT FAILED: post is not presently granted.' }
        $shapeErrors=@(Validate-PlanShape $virtualPlan); if ($shapeErrors.Count -gt 0) { throw ('CC REMOTE HIGH-REACH REVIEW/SHAPE FAILED: ' + ($shapeErrors -join '; ')) }
    } else { throw "CC REMOTE ACTION TYPE FAILED: '$type'." }
    Assert-PlanActionIdsUnspent $virtualPlan; $planHash=Get-PlanHash $virtualPlan; $live=Capture-State; $me=Safe-Property $live 'me' $null
    if ([string](Safe-Property $me 'handle' '') -ne 'cc-relay') { throw "CC REMOTE ACTION IDENTITY FAILED: server returned '$([string](Safe-Property $me 'handle' ''))'." }
    $today=Safe-Property $me 'today' $null
    if ($type -eq 'comment') {
        if ([int](Safe-Property $today 'comments_remaining' 0) -lt 1) { throw 'CC REMOTE ROUTINE QUOTA FAILED: no comments remaining.' }
        $postId=[int](Safe-Property $Action 'post_id' 0); [void](Get-Thread $postId)
        if ($null -ne (Safe-Property $Action 'parent_id' $null)) { throw 'CC REMOTE ROUTINE TARGET FAILED: automated comments are post-level only.' }
        if (@($Action.PSObject.Properties.Name) -contains 'closes_correction_debt_id') { throw 'CC REMOTE ROUTINE REFUSED: correction-debt closure is outside this lane.' }
    } else {
        if ([int](Safe-Property $today 'posts_remaining' 0) -lt 1) { throw 'CC REMOTE HIGH-REACH QUOTA FAILED: no posts remaining.' }
    }
    return [pscustomobject][ordered]@{ ok=$true; grant=$grant; grant_sha256=$grantSha; live=$live; me=$me; virtual_plan=$virtualPlan; virtual_plan_hash=$planHash; raw_carrier_sha256=$RawCarrierSha256 }
}

function New-CcWriteRelayResponse([string]$RequestId, [string]$Status, $Request = $null, $Data = $null, $Reason = $null) {
    $operation=[string](Safe-Property $Request 'operation' '')
    return [ordered]@{
        type='campfire-routine-write-response-v1'; request_id=$RequestId; status=$Status; aperture='cc-relay'; operation=$operation
        action_id=[string](Safe-Property $Request 'action_id' ''); created_at_utc=[DateTime]::UtcNow.ToString('o'); reason=$Reason; data=$Data
        boundaries=[ordered]@{ one_action_per_request=$true; local_filesystem_ingress=$true; github_ingress=$false; batches=$false; threaded_reply=$false; vote=$false
            top_level_post=($operation -eq 'POST'); reviewed_high_reach_post=($operation -eq 'POST'); human_operator_trigger_required_for_post=$false
            comment_requires_routine_enable=$true; post_requires_routine_enable=$false; money_or_treasury=$false; credential_operation=$false; grant_mutation=$false
            cursor_ack=$false; correction_debt_closure=$false; framework_ingress=$false; full_quick_loaded=$false; square_retry=$false
            standing_grant_and_fresh_framework_review_required_for_post=$true }
    }
}

function Write-CcHeadlessWriteStatus([string]$RequestId, [string]$Status, $Response = $null, $Data = $null) {
    if ([string]::IsNullOrWhiteSpace($RequestId)) { return }
    New-Item -ItemType Directory -Force -Path $CcWriteRelayStatusDir | Out-Null
    $row = [ordered]@{
        status_version = 'campfire-cc-routine-write-worker-status-v1'
        request_id = $RequestId
        status = $Status
        worker_pid = $PID
        updated_at_utc = [DateTime]::UtcNow.ToString('o')
        response = $Response
        data = $Data
    }
    Write-Utf8NoBom (Get-CcWriteRelayRequestStatusPath $RequestId) ($row | ConvertTo-Json -Depth 60)
}

function Invoke-CcRemoteRoutineWrite($Envelope, [string]$RawCarrierSha256) {
    $request=Safe-Property $Envelope 'request' $null
    if ($null -eq $request) { throw 'CC REMOTE ACTION REQUEST FILE FAILED: missing request object.' }
    if ([string](Safe-Property $request 'type' '') -ne 'campfire-routine-write-request-v1') { throw 'CC REMOTE ACTION REQUEST FILE FAILED: wrong type.' }
    if ([string](Safe-Property $request 'aperture' '') -ne 'cc-relay') { throw 'CC REMOTE ACTION REQUEST FILE FAILED: aperture must be cc-relay.' }
    if ([bool](Safe-Property $request 'cursor_ack' $true)) { throw 'CC REMOTE ACTION REQUEST FILE FAILED: cursor_ack must be false.' }
    $requestId=[string](Safe-Property $request 'request_id' '')
    if ($requestId -ne $HeadlessWriteRequestId -or $requestId -notmatch '^cc-write-[A-Za-z0-9._:-]{1,100}$') { throw 'CC REMOTE ACTION REQUEST FILE FAILED: request id mismatch.' }
    $action=Convert-CcWriteRelayRequestToAction $request; $preflight=$null
    try {
        $preflight=Preflight-CcRemoteRoutineAction $request $action $RawCarrierSha256
        [void](Append-Event 'CC_REMOTE_ROUTINE_PREFLIGHT_PASSED' ([pscustomobject]@{ request_id=$requestId; action_id=[string](Safe-Property $action 'id' ''); action_type=[string](Safe-Property $action 'type' ''); virtual_plan_hash=$preflight.virtual_plan_hash; raw_request_carrier_sha256=$RawCarrierSha256; grant_id=[string](Safe-Property $preflight.grant 'grant_id' ''); grant_sha256=$preflight.grant_sha256 }) ([pscustomobject]@{ active_aperture='cc-relay'; active_role='CC'; local_operator_trigger=$false; remote_standing_grant_transport=$true; content_endorsement_by_local_operator=$false }))
    }
    catch {
        [void](Append-Event 'CC_REMOTE_ROUTINE_PREFLIGHT_FAILED' ([pscustomobject]@{ request_id=$requestId; action_id=[string](Safe-Property $action 'id' ''); reason=$_.Exception.Message; raw_request_carrier_sha256=$RawCarrierSha256 }) ([pscustomobject]@{ square_write=$false; cursor_ack=$false; remote_standing_grant_transport=$true }))
        return [pscustomobject][ordered]@{ status='REFUSED'; write_occurred=$false; reason=$_.Exception.Message; response=$null; witness=$null; virtual_plan_hash=$null; grant_sha256=$null }
    }
    $type=[string](Safe-Property $action 'type' ''); $id=[string](Safe-Property $action 'id' '')
    [void](Append-Event 'CC_REMOTE_STANDING_GRANT_TRIGGERED' ([pscustomobject]@{ request_id=$requestId; action_id=$id; action_type=$type; grant_id=[string](Safe-Property $preflight.grant 'grant_id' ''); grant_sha256=$preflight.grant_sha256; virtual_plan_hash=$preflight.virtual_plan_hash; raw_request_carrier_sha256=$RawCarrierSha256; trigger_surface='LOCAL cc-relay WriteRelay ingress'; content_endorsement=$false }) ([pscustomobject]@{ local_operator_trigger=$false; explicit_local_bridge_enable_required=($type -eq 'comment'); reviewed_high_reach_post=($type -eq 'post'); active_aperture='cc-relay'; active_role='CC' }))
    $record=[ordered]@{ attempted_at_utc=[DateTime]::UtcNow.ToString('o'); aperture_role='CC'; plan_hash=$preflight.virtual_plan_hash; raw_plan_file_sha256=$RawCarrierSha256; grant_sha256=$preflight.grant_sha256; remote_request_id=$requestId; action_id=$id; type=$type; citizen='cc-relay'; request=$null; result=$null; write_success=$false; witness_status='NOT_RUN'; remote_standing_grant_transport=$true }
    $writeAttempted=$false; $squareReceiptReceived=$false
    try {
        if ($type -eq 'comment') { $payload=[ordered]@{ post_id=[int](Safe-Property $action 'post_id' 0); parent_id=$null; body=[string](Safe-Property $action 'body' '') }; $record.request=[ordered]@{ route='/api/comment'; body=$payload } }
        elseif ($type -eq 'post') { $payload=[ordered]@{ title=[string](Safe-Property $action 'title' ''); body=[string](Safe-Property $action 'body' '') }; $record.request=[ordered]@{ route='/api/post'; body=$payload } }
        else { throw "CC REMOTE ACTION EXECUTION FAILED: unsupported '$type'." }
        $writeAttempted=$true; $squareResponse=Invoke-SquarePost $record.request.route $record.request.body; $squareReceiptReceived=$true
        $record.result=$squareResponse; $record.write_success=$true
        [void](Append-Event 'ACTUATED' ([pscustomobject]@{ plan_hash=$preflight.virtual_plan_hash; raw_plan_file_sha256=$RawCarrierSha256; action_id=$id; action_type=$type; request=$record.request; response=$squareResponse; remote_request_id=$requestId; remote_standing_grant_transport=$true }) ([pscustomobject]@{ write_route=$record.request.route; attempted_at_utc=$record.attempted_at_utc; active_aperture='cc-relay'; active_role='CC'; grant_sha256=$preflight.grant_sha256; local_operator_trigger=$false }))
        $witness=Witness-Action $action $squareResponse $preflight.me $preflight.virtual_plan_hash $RawCarrierSha256
        $record.witness_status=[string](Safe-Property $witness 'status' 'UNVERIFIED'); Append-ActuationLog ([pscustomobject]$record); Capture-State | Out-Null
        if ([string](Safe-Property $witness 'status' '') -ne 'VERIFIED') { Disable-CcWriteRelay; return [pscustomobject][ordered]@{ status='WRITE_OCCURRED_UNVERIFIED'; write_occurred=$true; reason='Square write returned but read-after-write witness did not verify. CC routine circuit disabled.'; response=$squareResponse; witness=$witness; virtual_plan_hash=$preflight.virtual_plan_hash; grant_sha256=$preflight.grant_sha256 } }
        return [pscustomobject][ordered]@{ status='VERIFIED'; write_occurred=$true; reason=$null; response=$squareResponse; witness=$witness; virtual_plan_hash=$preflight.virtual_plan_hash; grant_sha256=$preflight.grant_sha256 }
    }
    catch {
        $failureReason=$_.Exception.Message; $record.result=[ordered]@{ error=$failureReason }; $record.write_success=[bool]$squareReceiptReceived
        try { Append-ActuationLog ([pscustomobject]$record) } catch { }
        try { [void](Append-Event 'ACT_FAILED' ([pscustomobject]@{ plan_hash=$preflight.virtual_plan_hash; raw_plan_file_sha256=$RawCarrierSha256; action_id=$id; action_type=$type; error=$failureReason; remote_request_id=$requestId; remote_standing_grant_transport=$true; square_post_attempted=[bool]$writeAttempted; square_receipt_received=[bool]$squareReceiptReceived; write_outcome_unknown=([bool]$writeAttempted -and -not [bool]$squareReceiptReceived) }) ([pscustomobject]@{ active_aperture='cc-relay'; active_role='CC'; grant_sha256=$preflight.grant_sha256; square_retry=$false })) } catch { }
        if ($squareReceiptReceived) { Disable-CcWriteRelay; return [pscustomobject][ordered]@{ status='WRITE_OCCURRED_UNVERIFIED'; write_occurred=$true; reason=$failureReason; response=$null; witness=$null; virtual_plan_hash=$preflight.virtual_plan_hash; grant_sha256=$preflight.grant_sha256 } }
        if ($writeAttempted) { Disable-CcWriteRelay; return [pscustomobject][ordered]@{ status='OUTCOME_UNKNOWN'; write_occurred=$null; reason=$failureReason; response=$null; witness=$null; virtual_plan_hash=$preflight.virtual_plan_hash; grant_sha256=$preflight.grant_sha256 } }
        return [pscustomobject][ordered]@{ status='FAILED_NO_WRITE'; write_occurred=$false; reason=$failureReason; response=$null; witness=$null; virtual_plan_hash=$preflight.virtual_plan_hash; grant_sha256=$preflight.grant_sha256 }
    }
}

function Invoke-CcHeadlessRoutineWriteRequest {
    if (-not $HeadlessWrite -or $HeadlessCitizen -ne 'cc-relay') { return }
    # request_id must be validated before it is used as a local status filename.
    if ($HeadlessWriteRequestId -notmatch '^cc-write-[A-Za-z0-9._:-]{1,100}$') { throw 'CC headless routine write request id is invalid.' }

    # First durable child evidence. This occurs before profile binding, carrier
    # parsing, preflight or any Square actuation path.
    Write-CcHeadlessWriteStatus $HeadlessWriteRequestId 'DISPATCH_RECEIVED' $null ([pscustomobject]@{
        child_script_entered=$true
        authority_preflight_passed=$false
        square_write=$false
        phase='CHILD_SCRIPT_ENTERED'
    })

    $request = $null
    $envelope = $null
    $rawCarrierSha = $null
    try {
        if ($HeadlessWritePostResponse) { throw 'CC headless routine write does not use GitHub response transport.' }
        if ([string]::IsNullOrWhiteSpace($HeadlessWriteRequestPath) -or -not (Test-Path -LiteralPath $HeadlessWriteRequestPath)) {
            throw 'CC headless routine write request carrier is unavailable.'
        }
        Set-ActiveProfile 'cc-relay'
        New-Item -ItemType Directory -Force -Path $CcWriteRelayStatusDir | Out-Null
        $rawCarrierSha = Get-Sha256File $HeadlessWriteRequestPath
        $envelope = Read-Utf8JsonFile $HeadlessWriteRequestPath
        $request = Safe-Property $envelope 'request' $null
        if ([string](Safe-Property $request 'request_id' '') -ne $HeadlessWriteRequestId) { throw 'CC headless routine write request carrier id mismatch.' }
        Write-CcHeadlessWriteStatus $HeadlessWriteRequestId 'STARTED' $null ([pscustomobject]@{
            carrier_sha256=$rawCarrierSha
            source_file_name=Safe-Property $envelope 'source_file_name' $null
            source_file_sha256=Safe-Property $envelope 'source_file_sha256' $null
            child_script_entered=$true
            authority_preflight_passed=$false
            square_write=$false
            phase='CARRIER_READY'
        })
    }
    catch {
        # No call to Invoke-CcRemoteRoutineWrite has occurred, therefore no
        # /api/comment route is reachable from this failed setup path.
        $failureReason = $_.Exception.Message
        $failedData = [ordered]@{
            write_occurred=$false
            worker_dispatched=$true
            child_script_entered=$true
            authority_preflight_passed=$false
            square_write=$false
            raw_request_carrier_sha256=$rawCarrierSha
            source_file_name=if ($null -ne $envelope) { Safe-Property $envelope 'source_file_name' $null } else { $null }
            source_file_sha256=if ($null -ne $envelope) { Safe-Property $envelope 'source_file_sha256' $null } else { $null }
            phase='PRE_CORE_SETUP_FAILED'
        }
        $failed = New-CcWriteRelayResponse $HeadlessWriteRequestId 'FAILED_NO_WRITE' $request $failedData ('CC worker failed before routine-write core/preflight: ' + $failureReason)
        Write-CcHeadlessWriteStatus $HeadlessWriteRequestId 'FAILED_NO_WRITE' $failed ([pscustomobject]@{
            child_script_entered=$true
            core_entered=$false
            square_write=$false
            square_retry=$false
            phase='PRE_CORE_SETUP_FAILED'
        })
        return 'FAILED_NO_WRITE'
    }

    # After this marker the core owns conservative actuation classification.
    # If the process dies with no later terminal state, the parent must not
    # infer whether /api/comment was reached.
    Write-CcHeadlessWriteStatus $HeadlessWriteRequestId 'CORE_ENTERED' $null ([pscustomobject]@{
        child_script_entered=$true
        core_entered=$true
        square_write=$null
        phase='ROUTINE_WRITE_CORE_ENTERED'
    })

    $result = Invoke-CcRemoteRoutineWrite $envelope $rawCarrierSha
    $responseData = [ordered]@{
        write_occurred=Safe-Property $result 'write_occurred' $null
        square_response=Safe-Property $result 'response' $null
        witness_status=[string](Safe-Property (Safe-Property $result 'witness' $null) 'status' '')
        witness_event_id=Safe-Property (Safe-Property $result 'witness' $null) 'event_id' $null
        receipt_comment_id=Safe-Property (Safe-Property $result 'response' $null) 'comment_id' $null
        public_comment_id=Safe-Property (Safe-Property (Safe-Property $result 'witness' $null) 'public_object_evidence' $null) 'comment_id' $null
        public_body_sha256=Safe-Property (Safe-Property (Safe-Property $result 'witness' $null) 'public_object_evidence' $null) 'body_sha256' $null
        public_evidence_source=Safe-Property (Safe-Property (Safe-Property $result 'witness' $null) 'public_object_evidence' $null) 'source_route' $null
        public_evidence_independence_ceiling=Safe-Property (Safe-Property (Safe-Property $result 'witness' $null) 'public_object_evidence' $null) 'independence_ceiling' $null
        virtual_plan_hash=Safe-Property $result 'virtual_plan_hash' $null
        raw_request_carrier_sha256=$rawCarrierSha
        source_file_name=Safe-Property $envelope 'source_file_name' $null
        source_file_sha256=Safe-Property $envelope 'source_file_sha256' $null
        grant_sha256=Safe-Property $result 'grant_sha256' $null
        campfire_square_source_sha256=if (-not [string]::IsNullOrWhiteSpace([string]$PSCommandPath)) { Get-Sha256File $PSCommandPath } else { $null }
    }
    $response = New-CcWriteRelayResponse $HeadlessWriteRequestId ([string]$result.status) $request $responseData ([string](Safe-Property $result 'reason' ''))
    Write-CcHeadlessWriteStatus $HeadlessWriteRequestId ([string]$result.status) $response ([pscustomobject]@{
        response_transport='LOCAL_RESPONSE_FILE_PENDING'
        square_retry=$false
    })
    return [string]$result.status
}

function Start-CcWriteRelayWorker($Envelope, [string]$RequestPath) {
    $request = Safe-Property $Envelope 'request' $null
    $requestId = [string](Safe-Property $request 'request_id' '')
    $workerScript = if (-not [string]::IsNullOrWhiteSpace([string]$PSCommandPath)) { [string]$PSCommandPath } else { $InstalledScript }
    if ([string]::IsNullOrWhiteSpace([string]$workerScript)) { throw 'CC routine write worker cannot resolve the Square source path.' }
    New-Item -ItemType Directory -Force -Path $CcWriteRelayStatusDir | Out-Null
    $stderrPath = New-CcWriteRelayWorkerStderrPath $requestId
    $argText = @(
        '-NoProfile',
        '-ExecutionPolicy Bypass',
        '-File ' + (Quote-ReadRelayProcessArgument $workerScript),
        '-HeadlessWrite',
        '-HeadlessCitizen cc-relay',
        '-HeadlessWriteRequestPath ' + (Quote-ReadRelayProcessArgument $RequestPath),
        '-HeadlessWriteRequestId ' + (Quote-ReadRelayProcessArgument $requestId)
    )
    return Start-Process powershell.exe -ArgumentList ($argText -join ' ') -WindowStyle Hidden -RedirectStandardError $stderrPath -PassThru
}

function Invoke-CcWriteRelayPoll {
    if ($script:CcWriteRelayPollInProgress) { return }
    $cfg = Get-CcWriteRelayConfig
    $dispatchEnabled = [bool](Safe-Property $cfg 'enabled' $false)
    $script:CcWriteRelayPollInProgress = $true
    try {
        foreach ($dir in @($CcWriteRelayRoot,$CcWriteRelayIngress,$CcWriteRelayInbox,$CcWriteRelayResponses,$CcWriteRelayArchive,$CcWriteRelayStatusDir)) {
            New-Item -ItemType Directory -Force -Path $dir | Out-Null
        }
        $state = Get-CcWriteRelayState
        $active = [string](Safe-Property $state 'active_request_id' '')
        if (-not [string]::IsNullOrWhiteSpace($active)) {
            $statusPath = Get-CcWriteRelayRequestStatusPath $active
            if (Test-Path -LiteralPath $statusPath) {
                $workerStatus = Read-Utf8JsonFile $statusPath
                $terminal = [string](Safe-Property $workerStatus 'status' '')
                if (@('VERIFIED','REFUSED','FAILED_NO_WRITE','WRITE_OCCURRED_UNVERIFIED','OUTCOME_UNKNOWN') -contains $terminal) {
                    $response = Safe-Property $workerStatus 'response' $null
                    if ($null -eq $response) {
                        $response = New-CcWriteRelayResponse $active $terminal $null ([ordered]@{ write_occurred=$null }) 'Worker reached a terminal state without a response envelope.'
                    }
                    $responsePath = Write-CcWriteRelayResponseFile $active $response
                    [void](Write-CcWriteRelayLedgerEvent 'CC_WRITE_RELAY_RESPONSE_WRITTEN' ([pscustomobject]@{
                        request_id=$active; status=$terminal; response_path=$responsePath; square_retry=$false
                    }))
                    if (@('WRITE_OCCURRED_UNVERIFIED','OUTCOME_UNKNOWN') -contains $terminal) {
                        $responseData = Safe-Property $response 'data' $null
                        [void](Write-CcWriteRelayLedgerEvent 'CC_WRITE_RELAY_ATTENTION_REQUIRED' ([pscustomobject]@{
                            request_id=$active
                            status=$terminal
                            reason=[string](Safe-Property $response 'reason' '')
                            public_comment_id=Safe-Property $responseData 'public_comment_id' $null
                            public_body_sha256=Safe-Property $responseData 'public_body_sha256' $null
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
            $startedText = [string](Safe-Property $state 'active_started_at_utc' '')
            $started = [DateTime]::MinValue
            if ([DateTime]::TryParse($startedText, [ref]$started)) {
                if (([DateTime]::UtcNow - $started.ToUniversalTime()).TotalMinutes -gt 5) {
                    $lastWorkerStatus = $null
                    if (Test-Path -LiteralPath $statusPath) {
                        try { $lastWorkerStatus = Read-Utf8JsonFile $statusPath } catch { }
                    }
                    $lastWorkerPhase = if ($null -ne $lastWorkerStatus) { [string](Safe-Property $lastWorkerStatus 'status' '') } else { 'NO_STATUS_FILE' }
                    $stderrCandidate = @(Get-ChildItem -LiteralPath $CcWriteRelayStatusDir -Filter ($active + '.stderr.*.txt') -File -ErrorAction SilentlyContinue | Sort-Object LastWriteTimeUtc -Descending | Select-Object -First 1)
                    $stderrPath = if ($stderrCandidate.Count -gt 0) { [string]$stderrCandidate[0].FullName } else { $null }
                    $stderrPresent = (-not [string]::IsNullOrWhiteSpace($stderrPath)) -and (Test-Path -LiteralPath $stderrPath)
                    $stderrBytes = [int64]0
                    $stderrSha = $null
                    if ($stderrPresent) {
                        try {
                            $stderrItem = Get-Item -LiteralPath $stderrPath
                            $stderrBytes = [int64]$stderrItem.Length
                            $stderrSha = Get-Sha256File $stderrPath
                        } catch { }
                    }
                    $diagnostic = [ordered]@{
                        write_occurred=$null
                        worker_last_status=$lastWorkerPhase
                        worker_stderr_present=[bool]$stderrPresent
                        worker_stderr_bytes=$stderrBytes
                        worker_stderr_sha256=$stderrSha
                        worker_stderr_file=if ($stderrPresent) { [IO.Path]::GetFileName($stderrPath) } else { $null }
                    }
                    [void](Write-CcWriteRelayLedgerEvent 'CC_WRITE_RELAY_OUTCOME_UNKNOWN' ([pscustomobject]@{
                        request_id=$active; reason='No terminal worker status after dispatch grace window.'; square_retry=$false
                        worker_last_status=$lastWorkerPhase; worker_stderr_present=[bool]$stderrPresent
                        worker_stderr_bytes=$stderrBytes; worker_stderr_sha256=$stderrSha
                    }))
                    $unknown = New-CcWriteRelayResponse $active 'OUTCOME_UNKNOWN' $null $diagnostic 'No terminal worker status after dispatch grace window; no Square retry attempted. CC write circuit disabled.'
                    [void](Write-CcWriteRelayResponseFile $active $unknown)
                    [void](Write-CcWriteRelayLedgerEvent 'CC_WRITE_RELAY_ATTENTION_REQUIRED' ([pscustomobject]@{
                        request_id=$active; status='OUTCOME_UNKNOWN'; reason='No terminal worker status after dispatch grace window.'
                        public_comment_id=$null; public_body_sha256=$null; read_must_remain_available=$true; square_retry=$false
                        worker_last_status=$lastWorkerPhase; worker_stderr_present=[bool]$stderrPresent
                        worker_stderr_bytes=$stderrBytes; worker_stderr_sha256=$stderrSha
                    }))
                    Disable-CcWriteRelay
                    $state.active_request_id=$null; $state.active_worker_pid=$null; $state.active_started_at_utc=$null; $state.active_dispatch_phase=$null
                    [void](Set-CcWriteRelayState $state)
                }
            }
            return
        }

        $candidates = @(Get-ChildItem -LiteralPath $CcWriteRelayIngress -Filter '*.json' -File -ErrorAction SilentlyContinue | Sort-Object LastWriteTimeUtc,Name)
        if ($candidates.Count -eq 0) { return }
        if (-not $dispatchEnabled) {
            $candidates = @($candidates | Where-Object {
                try {
                    $probe = Read-Utf8JsonFile $_.FullName
                    ([string](Safe-Property $probe 'type' '') -eq 'campfire-routine-write-request-v1' -and [string](Safe-Property $probe 'operation' '') -eq 'POST')
                } catch { $false }
            })
            if ($candidates.Count -eq 0) { return }
        }
        $file = $candidates[0]
        $request = $null
        $requestId = $null

        # Stage 1: schema/policy validation. A refusal here proves no worker was dispatched.
        try {
            $request = ConvertTo-CcWriteRelayRequestFile $file.FullName
            $requestId = [string](Safe-Property $request 'request_id' '')
        }
        catch {
            $reason = $_.Exception.Message
            try {
                $maybe = Read-Utf8JsonFile $file.FullName
                $requestId = [string](Safe-Property $maybe 'request_id' '')
            } catch { }
            if ($requestId -notmatch '^cc-write-[A-Za-z0-9._:-]{1,100}$') { $requestId = 'cc-write-refused-' + [guid]::NewGuid().ToString('N') }
            [void](Write-CcWriteRelayLedgerEvent 'CC_WRITE_RELAY_REQUEST_REFUSED' ([pscustomobject]@{
                request_id=$requestId; source_file=$file.Name; reason=$reason; square_write=$false; worker_dispatched=$false
            }))
            $refused = New-CcWriteRelayResponse $requestId 'REFUSED' $request ([ordered]@{ write_occurred=$false; worker_dispatched=$false }) $reason
            [void](Write-CcWriteRelayResponseFile $requestId $refused)
            try { [void](Move-CcWriteRelayRequestFile $file.FullName 'refused') } catch { }
            return
        }

        # Stage 2: prepare a durable accepted carrier and PREARM state. Failures before worker launch are FAILED_NO_WRITE.
        $acceptedPath = $null
        try {
            $sourceSha = Get-Sha256File $file.FullName
            [void](Write-CcWriteRelayLedgerEvent 'CC_WRITE_RELAY_REQUEST_OBSERVED' ([pscustomobject]@{
                request_id=$requestId; source_file=$file.Name; source_file_sha256=$sourceSha
            }))
            $envelope = [ordered]@{
                envelope_version='campfire-cc-routine-write-envelope-v1'
                request=$request
                source_file_name=$file.Name
                source_file_sha256=$sourceSha
                accepted_at_utc=[DateTime]::UtcNow.ToString('o')
            }
            $acceptedPath = Join-Path $CcWriteRelayInbox ($requestId + '.json')
            Write-Utf8NoBom $acceptedPath ($envelope | ConvertTo-Json -Depth 40)

            # Durable pre-arm exists before a worker can possibly reach Square.
            $state = Get-CcWriteRelayState
            $state.active_request_id=$requestId
            $state.active_worker_pid=$null
            $state.active_started_at_utc=[DateTime]::UtcNow.ToString('o')
            $state.active_dispatch_phase='PREARMED'
            [void](Set-CcWriteRelayState $state)
            [void](Move-CcWriteRelayRequestFile $file.FullName 'processed')
        }
        catch {
            $reason = $_.Exception.Message
            [void](Write-CcWriteRelayLedgerEvent 'CC_WRITE_RELAY_PREPARE_FAILED_NO_WRITE' ([pscustomobject]@{
                request_id=$requestId; source_file=$file.Name; reason=$reason; square_write=$false; worker_dispatched=$false
            }))
            $failed = New-CcWriteRelayResponse $requestId 'FAILED_NO_WRITE' $request ([ordered]@{ write_occurred=$false; worker_dispatched=$false }) $reason
            [void](Write-CcWriteRelayResponseFile $requestId $failed)
            try { if (Test-Path -LiteralPath $file.FullName) { [void](Move-CcWriteRelayRequestFile $file.FullName 'failed-no-write') } } catch { }
            $state = Get-CcWriteRelayState
            if ([string](Safe-Property $state 'active_request_id' '') -eq $requestId) {
                $state.active_request_id=$null; $state.active_worker_pid=$null; $state.active_started_at_utc=$null; $state.active_dispatch_phase=$null
                [void](Set-CcWriteRelayState $state)
            }
            return
        }

        # Stage 3: process creation is the ambiguity boundary. If Start-Process itself throws, do not claim no process existed.
        try {
            $process = Start-CcWriteRelayWorker $envelope $acceptedPath
            $state = Get-CcWriteRelayState
            $state.active_worker_pid=$process.Id
            $state.active_dispatch_phase='DISPATCHED'
            [void](Set-CcWriteRelayState $state)
            [void](Write-CcWriteRelayLedgerEvent 'CC_WRITE_RELAY_REQUEST_DISPATCHED' ([pscustomobject]@{
                request_id=$requestId; worker_pid=$process.Id; accepted_path=$acceptedPath; square_retry=$false
                meaning='PROCESS_LAUNCHED_ONLY'; authority_preflight_passed=$false; square_write_accepted=$false
            }))
        }
        catch {
            $reason = $_.Exception.Message
            [void](Write-CcWriteRelayLedgerEvent 'CC_WRITE_RELAY_DISPATCH_OUTCOME_UNKNOWN' ([pscustomobject]@{
                request_id=$requestId; accepted_path=$acceptedPath; reason=$reason; square_retry=$false
                note='Process creation threw at the dispatch boundary; no claim is made that a child did or did not start.'
            }))
            $unknown = New-CcWriteRelayResponse $requestId 'OUTCOME_UNKNOWN' $request ([ordered]@{ write_occurred=$null; worker_dispatched=$null }) ('Worker dispatch outcome is unknown: ' + $reason + '. No Square retry attempted; CC write circuit disabled.')
            [void](Write-CcWriteRelayResponseFile $requestId $unknown)
            [void](Write-CcWriteRelayLedgerEvent 'CC_WRITE_RELAY_ATTENTION_REQUIRED' ([pscustomobject]@{
                request_id=$requestId; status='OUTCOME_UNKNOWN'; reason=('Worker dispatch outcome is unknown: ' + $reason)
                public_comment_id=$null; public_body_sha256=$null; read_must_remain_available=$true; square_retry=$false
            }))
            Disable-CcWriteRelay
            $state = Get-CcWriteRelayState
            $state.active_request_id=$null; $state.active_worker_pid=$null; $state.active_started_at_utc=$null; $state.active_dispatch_phase=$null
            [void](Set-CcWriteRelayState $state)
            return
        }
    }
    catch {
        try { [void](Write-CcWriteRelayLedgerEvent 'CC_WRITE_RELAY_POLL_FAILED' ([pscustomobject]@{ reason=$_.Exception.Message; square_retry=$false })) } catch { }
    }
    finally { $script:CcWriteRelayPollInProgress = $false }
}

function Write-HeadlessReadStatus([string]$RequestId, [string]$Status, $Data = $null) {
    if ([string]::IsNullOrWhiteSpace($RequestId)) { return }
    $statusPath = if ($HeadlessCitizen -eq 'cc-relay') { Get-CcReadRelayRequestStatusPath $RequestId } else { Get-ReadRelayRequestStatusPath $RequestId }
    $row = [ordered]@{
        status_version = 'campfire-read-relay-worker-status-v1'
        request_id = $RequestId
        status = $Status
        worker_pid = $PID
        updated_at_utc = [DateTime]::UtcNow.ToString('o')
        data = $Data
    }
    Write-Utf8NoBom $statusPath ($row | ConvertTo-Json -Depth 30)
}

function Invoke-HeadlessReadRequest {
    if (-not $HeadlessRead) { return }
    if ($HeadlessPostResponse -and $HeadlessCitizen -ne 'framework-relay') {
        throw 'Headless GitHub response transport is fixed to framework-relay.'
    }
    if ($HeadlessKind -eq 'THREAD' -and $HeadlessPostId -le 0) {
        throw 'Headless THREAD requires -HeadlessPostId.'
    }
    if ($HeadlessKind -eq 'HEAD' -and $HeadlessPostId -gt 0) {
        throw 'Headless HEAD must not carry -HeadlessPostId.'
    }
    $headlessRequestPattern = if ($HeadlessCitizen -eq 'cc-relay') { '^cc-read-[A-Za-z0-9._:-]{1,100}$' } else { '^fw-read-[A-Za-z0-9._:-]{1,100}$' }
    if ((-not [string]::IsNullOrWhiteSpace($HeadlessRequestId) -or $HeadlessPostResponse) -and $HeadlessRequestId -notmatch $headlessRequestPattern) {
        throw 'Headless relay request id does not match the selected aperture.'
    }

    Set-ActiveProfile $HeadlessCitizen
    if (-not [string]::IsNullOrWhiteSpace($HeadlessOutputDirectory)) {
        New-Item -ItemType Directory -Force -Path $HeadlessOutputDirectory | Out-Null
        $script:ApertureArtifactDirectory = $HeadlessOutputDirectory
    }
    Write-HeadlessReadStatus $HeadlessRequestId 'STARTED' ([pscustomobject]@{
        aperture = $HeadlessCitizen
        operation = $HeadlessKind
        post_id = $HeadlessPostId
    })
    [void](Append-Event 'READ_RELAY_HEADLESS_STARTED' ([pscustomobject]@{
        request_id = $HeadlessRequestId
        operation = $HeadlessKind
        post_id = $HeadlessPostId
        post_response = [bool]$HeadlessPostResponse
    }) ([pscustomobject]@{
        read_only = $true
        cursor_ack = $false
        square_write = $false
    }))

    try {
        $path = if ($HeadlessKind -eq 'HEAD') {
            Export-CampfireApertureHead
        }
        else {
            Export-CampfireApertureThread $HeadlessPostId
        }
        $sha = Get-Sha256File $path
        $fileBytes = (Get-Item -LiteralPath $path).Length
        $artifact = Read-Utf8JsonFile $path
        $encoding = Compress-ReadRelayArtifactBase64 $path
        $completeness = if ($HeadlessKind -eq 'HEAD') {
            [pscustomobject][ordered]@{
                semantic_bodies_loaded = Safe-Property (Safe-Property $artifact 'aperture_invariant' $null) 'semantic_bodies_loaded' $false
                attention_rows_total = Safe-Property (Safe-Property $artifact 'aperture_budget' $null) 'attention_rows_total' $null
                attention_rows_included = Safe-Property (Safe-Property $artifact 'aperture_budget' $null) 'attention_rows_included' $null
                attention_rows_omitted = Safe-Property (Safe-Property $artifact 'aperture_budget' $null) 'attention_rows_omitted' $null
            }
        }
        else { Safe-Property $artifact 'completeness' $null }
        $response = [ordered]@{
            type = 'campfire-read-response-v1'
            request_id = $HeadlessRequestId
            status = 'COMPLETE'
            aperture = $HeadlessCitizen
            operation = $HeadlessKind
            post_id = if ($HeadlessKind -eq 'THREAD') { $HeadlessPostId } else { $null }
            created_at_utc = [DateTime]::UtcNow.ToString('o')
            artifact = [ordered]@{
                filename = [IO.Path]::GetFileName($path)
                exact_json_sha256 = $sha
                exact_json_bytes = $fileBytes
                hard_byte_ceiling = 65536
                campfire_square_source_sha256 = if (-not [string]::IsNullOrWhiteSpace([string]$PSCommandPath)) { Get-Sha256File $PSCommandPath } else { $null }
                completeness = $completeness
            }
            encoding = [ordered]@{
                kind = 'gzip+base64'
                gzip_bytes = $encoding.gzip_bytes
                payload = $encoding.base64
            }
            boundaries = [ordered]@{
                square_write = $false
                cursor_ack = $false
                full_quick_loaded = $false
                transport_completion_is_not_semantic_read = $true
                github_route_identity_is_not_runtime_identity = $true
            }
        }
        $responseCommentId = $null
        if ($HeadlessPostResponse) {
            $posted = Post-ReadRelayCommentJson $response
            $responseCommentId = Safe-Property $posted 'id' $null
        }
        [void](Append-Event 'READ_RELAY_RESPONSE_POSTED' ([pscustomobject]@{
            request_id = $HeadlessRequestId
            operation = $HeadlessKind
            post_id = $HeadlessPostId
            artifact_sha256 = $sha
            artifact_bytes = $fileBytes
            response_comment_id = $responseCommentId
            github_mirror = [bool]$HeadlessPostResponse
        }) ([pscustomobject]@{
            read_only_square_operation = $true
            external_transport = if ($HeadlessPostResponse) { 'private GitHub issue' } else { 'local filesystem' }
        }))
        Write-HeadlessReadStatus $HeadlessRequestId 'COMPLETE' ([pscustomobject]@{
            artifact_path = $path
            artifact_sha256 = $sha
            artifact_bytes = $fileBytes
            response_comment_id = $responseCommentId
        })
        return $path
    }
    catch {
        $reason = $_.Exception.Message
        $failureCommentId = $null
        if ($HeadlessPostResponse) {
            try {
                $postedFailure = Post-ReadRelayFailureResponse $HeadlessRequestId $HeadlessKind $HeadlessPostId $reason
                $failureCommentId = Safe-Property $postedFailure 'id' $null
            }
            catch { }
        }
        try {
            [void](Append-Event 'READ_RELAY_RESPONSE_FAILED' ([pscustomobject]@{
                request_id = $HeadlessRequestId
                operation = $HeadlessKind
                post_id = $HeadlessPostId
                reason = $reason
                failure_comment_id = $failureCommentId
                silent_retry = $false
            }) ([pscustomobject]@{ read_only_square_operation = $true }))
        }
        catch { }
        Write-HeadlessReadStatus $HeadlessRequestId 'FAILED' ([pscustomobject]@{
            reason = $reason
            failure_comment_id = $failureCommentId
        })
        throw
    }
}

# ----------------------------- FRAMEWORK RELAY EXPORT -------------------------
function Get-FullThreadForExport([int]$PostId) {
    $first = Invoke-SquareGet ("/api/post/" + $PostId)

    $all = [System.Collections.Generic.List[object]]::new()

    foreach ($c in @(Safe-Property $first 'comments' @())) {
        $all.Add($c)
    }

    $hasMore = [bool](Safe-Property $first 'has_more' $false)
    $cursor = Safe-Property $first 'next_since' $null
    $guard = 0

    while ($hasMore) {
        if ($null -eq $cursor -or [string]::IsNullOrWhiteSpace([string]$cursor)) {
            throw "Thread #$PostId says has_more but supplies no next_since cursor."
        }
        if ($guard -ge 100) {
            throw "Thread #$PostId exceeded the 100-page comment-pagination guard."
        }
        $guard++

        $page = Invoke-SquareGet (
            "/api/post/" +
            $PostId +
            "?since=" +
            [uri]::EscapeDataString([string]$cursor)
        )

        foreach ($c in @(Safe-Property $page 'comments' @())) {
            $all.Add($c)
        }

        $hasMore = [bool](Safe-Property $page 'has_more' $false)
        $cursor = Safe-Property $page 'next_since' $null
    }

    return [pscustomobject]@{
        post = Safe-Property $first 'post' $null
        tags = Safe-Property $first 'tags' @()
        comments = @($all.ToArray())
        comments_total = Safe-Property $first 'comments_total' $all.Count
        comments_exported = $all.Count
        has_more_after_export = $false
        pagination_guard_hit = $false
        pagination_snapshot_bound = $false
    }
}

function Export-CampfireRelayPacket(
    [ValidateSet('QUICK','FULL')]
    [string]$ExportMode = 'QUICK'
) {
    Update-ExportProgress -Phase 'Capturing current Square state' -AllowCancellation
    $state = Capture-State
    Update-ExportProgress -Phase 'Reading capability surface' -AllowCancellation
    $surface = Invoke-SquareGet '/api/surface'
    $grant = Get-ActiveGrant
    $grantSha = Get-ActiveGrantSha256

    # ---------------- FIRE ----------------
    $fireIds = @(Get-FirePostIds $state | Sort-Object)
    $fireThreads = [System.Collections.Generic.List[object]]::new()
    for ($firePosition = 0; $firePosition -lt $fireIds.Count; $firePosition++) {
        $postId = $fireIds[$firePosition]
        Update-ExportProgress `
            -Phase 'Reading required participation FIRE threads' `
            -Completed ($firePosition + 1) `
            -Total $fireIds.Count `
            -AllowCancellation
        try {
            $thread = Get-FullThreadForExport ([int]$postId)
            $fireThreads.Add([pscustomobject]@{
                post_id = [int]$postId
                ok = $true
                thread = $thread
            })
        }
        catch [System.OperationCanceledException] {
            throw
        }
        catch {
            $fireThreads.Add([pscustomobject]@{
                post_id = [int]$postId
                ok = $false
                error = $_.Exception.Message
            })
        }
    }

    # ---------------- REQUESTED READS ----------------
    $requestedIds = @(Get-RequestedPostIds)
    $requestedThreads = [System.Collections.Generic.List[object]]::new()
    for ($requestedPosition = 0; $requestedPosition -lt $requestedIds.Count; $requestedPosition++) {
        $postId = $requestedIds[$requestedPosition]
        Update-ExportProgress `
            -Phase 'Reading required directed threads' `
            -Completed ($requestedPosition + 1) `
            -Total $requestedIds.Count `
            -AllowCancellation
        try {
            $thread = Get-FullThreadForExport ([int]$postId)
            $requestedThreads.Add([pscustomobject]@{
                post_id = [int]$postId
                ok = $true
                reason = 'profile-local directed read; visible in FIRE queue as REQUESTED, not participation membership'
                thread = $thread
            })
        }
        catch [System.OperationCanceledException] {
            throw
        }
        catch {
            $requestedThreads.Add([pscustomobject]@{
                post_id = [int]$postId
                ok = $false
                reason = 'profile-local directed read; failed loudly'
                error = $_.Exception.Message
            })
        }
    }

    # Project repeated state before optional expansion. The complete discovery
    # index remains available below; bodies duplicated by /api/me, feeds,
    # history, and the local event ledger are deliberately reduced to refs.
    $stateProjection = Get-RelayStateProjection $state
    $eventIndex = @(Get-RelayEventIndex 500)
    $openDebtIndex = @(
        @(Get-OpenCorrectionDebts) |
        ForEach-Object { ConvertTo-RelayEventReference $_ }
    )
    $openInvestigationIndex = @(
        @(Get-OpenWitnessInvestigations) |
        ForEach-Object { ConvertTo-RelayEventReference $_ }
    )

    # ---------------- HORIZON DISCOVERY + DYNAMIC EXPANSION ----------------
    $horizonIndex = @(Get-HorizonRows $state)

    # Do not assign an empty pipeline result from an if-expression. Under
    # Windows PowerShell strict mode that becomes $null, so the later .Count
    # access fails before QUICK can serialize its index-only carrier.
    $horizonCandidates = @()
    if ($ExportMode -eq 'FULL') {
        $horizonCandidates = @(Get-HorizonExpansionCandidates $state)
    }
    $horizonThreads = [System.Collections.Generic.List[object]]::new()
    $horizonAttempts = [System.Collections.Generic.List[object]]::new()
    $horizonBytesUsed = 0L
    $horizonAttemptCount = 0
    $horizonStopCause = if ($ExportMode -eq 'FULL') {
        'CANDIDATE_EXHAUSTED'
    }
    else {
        'QUICK_MODE_INDEX_ONLY'
    }
    $horizonCancelled = $false
    $utf8 = New-Object System.Text.UTF8Encoding($false)

    # The expansion allowance is derived from what the required regions cost
    # now. It is not a fixed thread count and it cannot consume the space needed
    # for packet metadata. Complete discovery is preserved by the compact index
    # even when no full Horizon thread fits.
    $requiredBudgetProbe = [ordered]@{
        current_state = $stateProjection
        surface = $surface
        standing_grant = $grant
        fire_threads = @($fireThreads.ToArray())
        requested_threads = @($requestedThreads.ToArray())
        horizon_index = $horizonIndex
        local_event_index = $eventIndex
        open_correction_debts = $openDebtIndex
        open_witness_investigations = $openInvestigationIndex
    }
    $requiredBaseBytes = [int64]$utf8.GetByteCount(
        ($requiredBudgetProbe | ConvertTo-Json -Depth 90 -Compress)
    )
    $availableOptionalThreadBytes = [int64][math]::Max(
        0,
        ($RelayPacketByteBudget - $RelayPacketMetadataReserve - $requiredBaseBytes)
    )
    $horizonExpansionByteBudget = if ($ExportMode -eq 'FULL') {
        $availableOptionalThreadBytes
    }
    else {
        [int64]0
    }
    if ($ExportMode -eq 'FULL' -and $horizonExpansionByteBudget -le 0) {
        $horizonStopCause = 'NO_OPTIONAL_BYTES_AFTER_REQUIRED_REGIONS'
    }

    for ($horizonPosition = 0; $horizonPosition -lt $horizonCandidates.Count; $horizonPosition++) {
        $row = $horizonCandidates[$horizonPosition]
        if ($horizonExpansionByteBudget -le 0 -or $horizonBytesUsed -ge $horizonExpansionByteBudget) {
            if ($horizonStopCause -eq 'CANDIDATE_EXHAUSTED') {
                $horizonStopCause = 'TOTAL_PACKET_BYTE_BUDGET_REACHED'
            }
            break
        }
        $horizonAttemptCount++
        $postId = [int](Safe-Property $row 'id' 0)
        if($postId -le 0){ continue }

        try {
            Update-ExportProgress `
                -Phase "Expanding optional Horizon thread #$postId" `
                -Completed ($horizonPosition + 1) `
                -Total $horizonCandidates.Count `
                -AcceptedBytes $horizonBytesUsed `
                -AllowCancellation
            $thread = Get-FullThreadForExport $postId
            $threadBytes = [int64]$utf8.GetByteCount(($thread | ConvertTo-Json -Depth 90 -Compress))
            if (($horizonBytesUsed + $threadBytes) -gt $horizonExpansionByteBudget) {
                $horizonAttempts.Add([pscustomobject]@{
                    post_id = $postId
                    selection_reason = [string](Safe-Property $row 'selection_reason' '')
                    result = 'SKIPPED_OVER_REMAINING_BYTE_BUDGET'
                    thread_bytes = $threadBytes
                })
                continue
            }
            $horizonThreads.Add([pscustomobject]@{
                post_id = $postId
                ok = $true
                reason = [string](Safe-Property $row 'selection_reason' '')
                thread_bytes = $threadBytes
                thread = $thread
            })
            $horizonBytesUsed += $threadBytes
            $horizonAttempts.Add([pscustomobject]@{
                post_id = $postId
                selection_reason = [string](Safe-Property $row 'selection_reason' '')
                result = 'EXPANDED'
                thread_bytes = $threadBytes
            })
        }
        catch [System.OperationCanceledException] {
            $horizonStopCause = 'USER_CANCELLED'
            $horizonCancelled = $true
            break
        }
        catch {
            $horizonThreads.Add([pscustomobject]@{
                post_id = $postId
                ok = $false
                reason = [string](Safe-Property $row 'selection_reason' '')
                error = $_.Exception.Message
            })
            $horizonAttempts.Add([pscustomobject]@{
                post_id = $postId
                selection_reason = [string](Safe-Property $row 'selection_reason' '')
                result = 'FETCH_FAILED'
                error = $_.Exception.Message
            })
        }
    }

    Update-ExportProgress `
        -Phase "Serializing packet; Horizon stop cause: $horizonStopCause" `
        -Completed $horizonAttemptCount `
        -Total $horizonCandidates.Count `
        -AcceptedBytes $horizonBytesUsed

    $sourceHash = $null
    try {
        $sourceHash = (Get-FileHash -LiteralPath $InstalledScript -Algorithm SHA256).Hash.ToLowerInvariant()
    }
    catch { }

    $configuredApertures = [System.Collections.Generic.List[object]]::new()
    foreach ($key in $ProfileCatalog.Keys) {
        $p = $ProfileCatalog[$key]
        $credentialPresent = $false
        try {
            $credentialPresent = @(
                $p.credential_candidates |
                Where-Object { Test-Path -LiteralPath $_ }
            ).Count -eq 1
        }
        catch { }

        $configuredApertures.Add([pscustomobject]@{
            role = [string]$p.role
            citizen = [string]$p.citizen
            credential_present_locally = $credentialPresent
            credential_path_exported = $false
        })
    }

    $packet = [ordered]@{
        packet_version = '0.9'
        packet_type = 'campfire-relay-live-world'
        export_mode = $ExportMode
        created_at_utc = [DateTime]::UtcNow.ToString('o')
        read_only_export = $true

        intended_consumers = @('Framework','CC','Mark')

        active_aperture = [ordered]@{
            role = $ActiveRole
            citizen = $ExpectedCitizen
            local_profile_namespace = "Profiles/$ExpectedCitizen"
        }

        configured_apertures = @($configuredApertures.ToArray())

        source_world = [ordered]@{
            adapter = '1f916'
            source = $Base
            citizen = $ExpectedCitizen
        }

        semantics = [ordered]@{
            shared_gui_does_not_imply_shared_identity = $true
            shared_packet_does_not_imply_shared_read = $true
            fw_act_does_not_imply_cc_act = $true
            profile_switch_does_not_transfer_credential = $true
            packet_exists_does_not_imply_possession = $true
            packet_possession_does_not_imply_processing = $true
            packet_processing_does_not_imply_reading = $true
            packet_reading_does_not_imply_comprehension = $true
            one_aperture_read_does_not_imply_another_read = $true
            requested_read_does_not_imply_participation = $true
            requested_read_is_visible_in_fire_queue = $true
            requested_read_does_not_imply_participation_fire_membership = $true
            requested_read_does_not_imply_model_read = $true
            horizon_index_does_not_imply_full_thread_expansion = $true
            quick_export_preserves_complete_horizon_index = $true
            quick_export_omits_automatic_horizon_full_threads = $true
            full_export_expands_horizon_under_total_carrier_budget = $true
            deterministic_sampling_does_not_imply_representativeness = $true
            square_cursor_is_delivery_watermark = $true
            square_cursor_is_not_cognition_receipt = $true
            verification_is_bound_to_the_verified_object = $true
            byte_identity_does_not_prove_source_truth = $true
            com_carrier_does_not_prove_runtime_identity = $true
        }

        exact_byte_identity = [ordered]@{
            scheme = 'sha256-in-filename-v1'
            algorithm = 'SHA-256'
            scope = 'exact raw bytes of this JSON file'
            producer_encoding = 'UTF-8 without BOM'
            canonicalisation_required = $false
            digest_location = 'filename suffix __SHA256_<64-lowercase-hex>'
            verification_rule = 'compute SHA-256 over received file bytes and compare with filename digest'
            proves = 'byte identity of the received carrier'
            does_not_prove = 'source truth, freshness, reading, comprehension, authority, runtime identity, or semantic correctness'
        }

        credential_boundary = [ordered]@{
            authenticated_reads_performed_locally = $true
            active_credential_citizen = $ExpectedCitizen
            bearer_secret_included = $false
            credential_exported = $false
            other_aperture_credential_read = $false
        }

        campfire_square = [ordered]@{
            version = $AppVersion
            source_sha256 = $sourceHash
        }

        carrier_budget = [ordered]@{
            total_packet_byte_budget = [int64]$RelayPacketByteBudget
            metadata_reserve_bytes = [int64]$RelayPacketMetadataReserve
            required_region_probe_bytes = [int64]$requiredBaseBytes
            available_optional_thread_capacity_bytes = [int64]$availableOptionalThreadBytes
            derived_optional_thread_budget_bytes = [int64]$horizonExpansionByteBudget
            budget_is_operational_not_epistemic = $true
            complete_horizon_index_preserved_independently = $true
            exact_final_packet_bytes = [int64]0
            exact_final_packet_within_budget = $true
        }

        standing_grant = [ordered]@{
            source = 'profile-local standing-grant.json'
            file_sha256 = $grantSha
            grant = $grant
        }

        regions = [ordered]@{
            current_state = $stateProjection
            surface = $surface
            fire = [ordered]@{
                post_ids = $fireIds
                display_post_ids = @(Get-FireDisplayPostIds $state | Sort-Object)
                directed_read_post_ids = $requestedIds
                count = $fireThreads.Count
                participation_count = $fireThreads.Count
                display_count = @(Get-FireDisplayPostIds $state).Count
                semantics = 'threads carries participation FIRE; display_post_ids is the UI reading queue union and preserves requested reads separately'
                threads = @($fireThreads.ToArray())
            }
            requested_reads = [ordered]@{
                request_source = 'profile-local Data/requested-reads.json'
                request_file_sha256 = if (Test-Path -LiteralPath $RequestedReadsPath) { Get-Sha256File $RequestedReadsPath } else { $null }
                post_ids = $requestedIds
                count = $requestedThreads.Count
                semantics = 'directed read; visible in FIRE queue as REQUESTED but not participation membership, vote, comment, quota use, cursor movement, or cognition receipt'
                threads = @($requestedThreads.ToArray())
            }
            horizon = [ordered]@{
                label = if ($ExportMode -eq 'FULL') { 'HORIZON DISCOVERY INDEX + TRANSPARENT FULL-THREAD SAMPLE' } else { 'HORIZON COMPLETE DISCOVERY INDEX; AUTOMATIC FULL-THREAD EXPANSION OMITTED' }
                source = if ($ExportMode -eq 'FULL') { 'snapshot-bounded paged /api/new index; full-thread expansions selected by round-robin strata under declared operational budget' } else { 'snapshot-bounded paged /api/new index; full bodies available through FIRE, requested reads, or deliberate FULL export' }
                expansion_enabled = ($ExportMode -eq 'FULL')
                universe_count = [int](Safe-Property (Safe-Property $state 'discovery' $null) 'count' 0)
                board_total = [int](Safe-Property (Safe-Property $state 'discovery' $null) 'board_total' 0)
                universe_complete = [bool](Safe-Property (Safe-Property $state 'discovery' $null) 'complete' $false)
                eligible_count = $horizonIndex.Count
                expanded_count = @($horizonThreads | Where-Object { [bool](Safe-Property $_ 'ok' $false) }).Count
                failed_count = @($horizonThreads | Where-Object { -not [bool](Safe-Property $_ 'ok' $false) }).Count
                expansion_byte_budget = [int64]$horizonExpansionByteBudget
                expansion_bytes_used = [int64]$horizonBytesUsed
                expansion_attempt_guard = $null
                expansion_stop_rule = if ($ExportMode -eq 'FULL') { 'finite candidate list, remaining total-carrier byte budget, or explicit user cancellation; no fixed thread-count cap' } else { 'QUICK mode deliberately makes no automatic Horizon full-thread calls; complete index remains present' }
                expansion_stop_cause = $horizonStopCause
                expansion_cancelled_by_operator = $horizonCancelled
                expansion_attempts = $horizonAttemptCount
                selection_order = @('materially_changed','newly_created','oldest_index_edge','quiet_tail','ranked_front','deterministic_tail_sample')
                deterministic_sample_seed = [string](Safe-Property (Safe-Property $state 'discovery' $null) 'snapshot_id' '0')
                index = $horizonIndex
                attempts = @($horizonAttempts.ToArray())
                threads = @($horizonThreads.ToArray())
            }
            local_evidence = [ordered]@{
                aperture_role = $ActiveRole
                citizen = $ExpectedCitizen
                recent_event_index = $eventIndex
                recent_event_limit = 500
                recent_event_window_is_obligation_horizon = $false
                obligation_reconstruction_scope = 'complete_profile_event_ledger'
                verbose_event_fields_omitted = $true
                witnessed_event_check_policy = 'target identity, all check names/results and evidence-group identity retained; detail retained only for failed checks; neither check count nor evidence-group count is an independent-witness count'
                open_correction_debts = $openDebtIndex
                open_witness_investigations = $openInvestigationIndex
                event_ledger_path_exported = $false
            }
        }

        provenance = [ordered]@{
            produced_by = 'Campfire Square local Windows tool'
            carrier = 'Campfire Relay Live World packet'
            direct_framework_network_access = $false
            direct_cc_network_access = $false
            meaning = 'Active-aperture authenticated source artifact. Exact-byte identity, possession, processing, reading and comprehension remain separate claims.'
        }
    }

    $json = $packet | ConvertTo-Json -Depth 90 -Compress

    # The probe deliberately reserved metadata space. Check the exact carrier,
    # then deterministically remove only optional Horizon expansions if the
    # estimate was still too small. Required regions are never silently cut.
    $exactPacketBytes = [int64]$utf8.GetByteCount($json)
    while ($exactPacketBytes -gt $RelayPacketByteBudget -and $horizonThreads.Count -gt 0) {
        $lastIndex = $horizonThreads.Count - 1
        $lastThread = $horizonThreads[$lastIndex]
        $lastBytes = [int64](Safe-Property $lastThread 'thread_bytes' 0)
        $horizonThreads.RemoveAt($lastIndex)
        $horizonBytesUsed = [math]::Max(0, ($horizonBytesUsed - $lastBytes))
        $horizonStopCause = 'FINAL_TOTAL_BUDGET_TRIM'
        $packet.regions.horizon.threads = @($horizonThreads.ToArray())
        $packet.regions.horizon.expanded_count = @(
            $horizonThreads |
            Where-Object { [bool](Safe-Property $_ 'ok' $false) }
        ).Count
        $packet.regions.horizon.failed_count = @(
            $horizonThreads |
            Where-Object { -not [bool](Safe-Property $_ 'ok' $false) }
        ).Count
        $packet.regions.horizon.expansion_bytes_used = [int64]$horizonBytesUsed
        $packet.regions.horizon.expansion_stop_cause = $horizonStopCause
        $json = $packet | ConvertTo-Json -Depth 90 -Compress
        $exactPacketBytes = [int64]$utf8.GetByteCount($json)
    }
    if ($exactPacketBytes -gt $RelayPacketByteBudget) {
        throw (
            'REQUIRED_RELAY_REGIONS_EXCEED_TOTAL_BYTE_BUDGET. ' +
            'Required bytes: ' + $exactPacketBytes +
            '; budget: ' + $RelayPacketByteBudget +
            '. No packet was written.'
        )
    }
    # Stabilise the disclosed exact size. The field changes the carrier size,
    # so measure and rewrite until the integer is self-consistent.
    for ($sizePass = 0; $sizePass -lt 6; $sizePass++) {
        $packet.carrier_budget.exact_final_packet_bytes = [int64]$exactPacketBytes
        $json = $packet | ConvertTo-Json -Depth 90 -Compress
        $measuredPacketBytes = [int64]$utf8.GetByteCount($json)
        if ($measuredPacketBytes -eq $exactPacketBytes) { break }
        $exactPacketBytes = $measuredPacketBytes
    }
    $json = $packet | ConvertTo-Json -Depth 90 -Compress
    $exactPacketBytes = [int64]$utf8.GetByteCount($json)
    if ([int64]$packet.carrier_budget.exact_final_packet_bytes -ne $exactPacketBytes) {
        throw 'FINAL_PACKET_SIZE_DISCLOSURE_DID_NOT_STABILISE. No packet was written.'
    }
    if ($exactPacketBytes -gt $RelayPacketByteBudget) {
        throw 'FINAL_BUDGET_DISCLOSURE_EXCEEDED_TOTAL_BYTE_BUDGET. No packet was written.'
    }
    if($json -match '1f916_sk_[A-Za-z0-9_-]+'){
        throw 'SECRET-SHAPED VALUE DETECTED. Export refused.'
    }

    $stamp = [DateTime]::UtcNow.ToString('yyyyMMdd_HHmmssZ')
    $temporary = Join-Path $Downloads (
        'UPLOAD_THIS_TO_CAMPFIRE_RELAY_' +
        $ExpectedCitizen + '_' + $ExportMode + '_' +
        $stamp +
        '__PENDING.json'
    )
    Write-Utf8NoBom $temporary $json

    $digest = (Get-FileHash -LiteralPath $temporary -Algorithm SHA256).Hash.ToLowerInvariant()
    $final = Join-Path $Downloads (
        'UPLOAD_THIS_TO_CAMPFIRE_RELAY_' +
        $ExpectedCitizen + '_' + $ExportMode + '_' +
        $stamp +
        '__SHA256_' +
        $digest +
        '.json'
    )

    Move-Item -LiteralPath $temporary -Destination $final -Force

    $verifyDigest = (Get-FileHash -LiteralPath $final -Algorithm SHA256).Hash.ToLowerInvariant()
    if($verifyDigest -ne $digest){
        Remove-Item -LiteralPath $final -Force -ErrorAction SilentlyContinue
        throw 'Exact-byte SHA verification failed after final rename.'
    }

    $bytes = (Get-Item -LiteralPath $final).Length
    $script:LastRelaySha256 = $digest

    [void](Append-Event 'RELAY_PACKET_EXPORTED' ([pscustomobject]@{
        path_basename = [IO.Path]::GetFileName($final)
        exact_file_sha256 = $digest
        exact_file_bytes = $bytes
        aperture_role = $ActiveRole
        citizen = $ExpectedCitizen
        export_mode = $ExportMode
        fire_threads = $fireThreads.Count
        requested_read_threads = $requestedThreads.Count
        horizon_eligible_threads = $horizonIndex.Count
        horizon_expanded_threads = $horizonThreads.Count
        horizon_expansion_bytes = $horizonBytesUsed
        bearer_secret_included = $false
    }) ([pscustomobject]@{
        read_only_export = $true
        aperture_neutral_carrier = $true
        active_aperture_specific_observation = $true
        byte_identity_scheme = 'sha256-in-filename-v1'
    }))

    return $final
}


# ----------------------------- BUILD GUI --------------------------------------
Ensure-StableInstall

if ($HeadlessRead -and $HeadlessWrite) {
    Write-Error 'Headless read and headless write modes are mutually exclusive.'
    exit 1
}

if ($HeadlessRead) {
    try {
        $resultPath = Invoke-HeadlessReadRequest
        if (-not [string]::IsNullOrWhiteSpace([string]$resultPath)) { Write-Output $resultPath }
        exit 0
    }
    catch {
        Write-Error $_.Exception.Message
        exit 1
    }
}

if ($HeadlessWrite) {
    try {
        $resultStatus = Invoke-HeadlessRoutineWriteRequest
        if (-not [string]::IsNullOrWhiteSpace([string]$resultStatus)) { Write-Output $resultStatus }
        exit 0
    }
    catch {
        Write-Error $_.Exception.Message
        exit 1
    }
}

$form = New-Object System.Windows.Forms.Form
$form.Text = "Campfire Square v$AppVersion - $ActiveRole / $ExpectedCitizen"
$form.Size = New-Object System.Drawing.Size(1250, 850)
$form.StartPosition = 'CenterScreen'
$form.MinimumSize = New-Object System.Drawing.Size(1000, 700)

$topPanel = New-Object System.Windows.Forms.Panel
$topPanel.Dock = 'Top'
$topPanel.Height = 88

$contentPanel = New-Object System.Windows.Forms.Panel
$contentPanel.Dock = 'Fill'

# Add the fill region first and the top bar second. More importantly, the tabs
# live inside their own content panel, so they can never slide underneath the
# status bar regardless of WinForms z-order/docking quirks.
$form.Controls.Add($contentPanel)
$form.Controls.Add($topPanel)

$titleLabel = New-Object System.Windows.Forms.Label
$titleLabel.Text = 'CAMPFIRE SQUARE'
$titleLabel.Location = New-Object System.Drawing.Point(12, 8)
$titleLabel.AutoSize = $true
$titleLabel.Font = New-Object System.Drawing.Font('Segoe UI', 16, [System.Drawing.FontStyle]::Bold)
$topPanel.Controls.Add($titleLabel)

$apertureLabel = New-Object System.Windows.Forms.Label
$apertureLabel.Text = 'APERTURE'
$apertureLabel.Location = New-Object System.Drawing.Point(245, 14)
$apertureLabel.AutoSize = $true
$apertureLabel.Font = New-Object System.Drawing.Font('Segoe UI', 9, [System.Drawing.FontStyle]::Bold)
$topPanel.Controls.Add($apertureLabel)

$apertureCombo = New-Object System.Windows.Forms.ComboBox
$apertureCombo.DropDownStyle = 'DropDownList'
$apertureCombo.Location = New-Object System.Drawing.Point(320, 10)
$apertureCombo.Size = New-Object System.Drawing.Size(245, 30)
foreach ($key in $ProfileCatalog.Keys) {
    [void]$apertureCombo.Items.Add([string]$ProfileCatalog[$key].display)
}
$apertureCombo.SelectedIndex = 0
$topPanel.Controls.Add($apertureCombo)

$apertureStateLabel = New-Object System.Windows.Forms.Label
$apertureStateLabel.Text = 'Shared GUI; credential/state/grant remain profile-local.'
$apertureStateLabel.Location = New-Object System.Drawing.Point(580, 14)
$apertureStateLabel.Size = New-Object System.Drawing.Size(430, 24)
$topPanel.Controls.Add($apertureStateLabel)

$statusLabel = New-Object System.Windows.Forms.Label
$statusLabel.Text = 'Not refreshed yet'
$statusLabel.Location = New-Object System.Drawing.Point(220, 50)
$statusLabel.Size = New-Object System.Drawing.Size(790, 24)
$statusLabel.Font = New-Object System.Drawing.Font('Segoe UI', 10)
$topPanel.Controls.Add($statusLabel)

$refreshButton = New-Object System.Windows.Forms.Button
$refreshButton.Text = 'Refresh now'
$refreshButton.Location = New-Object System.Drawing.Point(1030, 46)
$refreshButton.Size = New-Object System.Drawing.Size(100, 32)
$topPanel.Controls.Add($refreshButton)

$autoCheck = New-Object System.Windows.Forms.CheckBox
$autoCheck.Text = 'Auto'
$autoCheck.Checked = $true
$autoCheck.Location = New-Object System.Drawing.Point(1140, 52)
$autoCheck.AutoSize = $true
$topPanel.Controls.Add($autoCheck)

$tabs = New-Object System.Windows.Forms.TabControl
$tabs.Dock = 'Fill'
$contentPanel.Controls.Add($tabs)

# HOME TAB
$homeTab = New-Object System.Windows.Forms.TabPage
$homeTab.Text = 'NOW'
$tabs.TabPages.Add($homeTab)

$homeText = New-ReadOnlyTextBox -Location (New-Object System.Drawing.Point(12,12)) -Size (New-Object System.Drawing.Size(1180,650))
$homeText.Anchor = 'Top,Bottom,Left,Right'
$homeTab.Controls.Add($homeText)

$openDataButton = New-Object System.Windows.Forms.Button
$openDataButton.Text = 'Open local Campfire folder'
$openDataButton.Location = New-Object System.Drawing.Point(12,675)
$openDataButton.Size = New-Object System.Drawing.Size(190,32)
$openDataButton.Anchor = 'Bottom,Left'
$homeTab.Controls.Add($openDataButton)

# SQUARE TAB
$squareTab = New-Object System.Windows.Forms.TabPage
$squareTab.Text = 'FIRE'
$tabs.TabPages.Add($squareTab)

$split = New-Object System.Windows.Forms.SplitContainer
$split.Dock = 'Fill'
$split.Orientation = 'Vertical'
$split.SplitterDistance = 460
$squareTab.Controls.Add($split)

$postGrid = New-Object System.Windows.Forms.DataGridView
$postGrid.Dock = 'Fill'
$postGrid.ReadOnly = $true
$postGrid.AllowUserToAddRows = $false
$postGrid.AllowUserToDeleteRows = $false
$postGrid.SelectionMode = 'FullRowSelect'
$postGrid.MultiSelect = $false
$postGrid.AutoSizeColumnsMode = 'Fill'
$split.Panel1.Controls.Add($postGrid)

$threadText = New-Object System.Windows.Forms.TextBox
$threadText.Dock = 'Fill'
$threadText.Multiline = $true
$threadText.ReadOnly = $true
$threadText.ScrollBars = 'Both'
$threadText.WordWrap = $true
$threadText.Font = New-Object System.Drawing.Font('Segoe UI', 10)
$split.Panel2.Controls.Add($threadText)

# HORIZON TAB
$horizonTab = New-Object System.Windows.Forms.TabPage
$horizonTab.Text = 'HORIZON'
$tabs.TabPages.Add($horizonTab)

$horizonSplit = New-Object System.Windows.Forms.SplitContainer
$horizonSplit.Dock = 'Fill'
$horizonSplit.Orientation = 'Vertical'
$horizonSplit.SplitterDistance = 460
$horizonTab.Controls.Add($horizonSplit)

$horizonGrid = New-Object System.Windows.Forms.DataGridView
$horizonGrid.Dock = 'Fill'
$horizonGrid.ReadOnly = $true
$horizonGrid.AllowUserToAddRows = $false
$horizonGrid.AllowUserToDeleteRows = $false
$horizonGrid.SelectionMode = 'FullRowSelect'
$horizonGrid.MultiSelect = $false
$horizonGrid.AutoSizeColumnsMode = 'Fill'
$horizonSplit.Panel1.Controls.Add($horizonGrid)

$horizonText = New-Object System.Windows.Forms.TextBox
$horizonText.Dock = 'Fill'
$horizonText.Multiline = $true
$horizonText.ReadOnly = $true
$horizonText.ScrollBars = 'Both'
$horizonText.WordWrap = $true
$horizonText.Font = New-Object System.Drawing.Font('Segoe UI', 10)
$horizonText.Text = "HORIZON DISCOVERY INDEX for $ExpectedCitizen. Complete snapshot-bounded metadata where pagination succeeds; Relay full-thread expansion is budgeted and explicitly selected."
$horizonSplit.Panel2.Controls.Add($horizonText)

# REQUESTED READS TAB
$requestedTab = New-Object System.Windows.Forms.TabPage
$requestedTab.Text = 'REQUESTED READS'
$tabs.TabPages.Add($requestedTab)

$requestedTopPanel = New-Object System.Windows.Forms.Panel
$requestedTopPanel.Dock = 'Top'
$requestedTopPanel.Height = 62
$requestedTab.Controls.Add($requestedTopPanel)

$requestedIdLabel = New-Object System.Windows.Forms.Label
$requestedIdLabel.Text = 'Post ID:'
$requestedIdLabel.Location = New-Object System.Drawing.Point(12,17)
$requestedIdLabel.AutoSize = $true
$requestedTopPanel.Controls.Add($requestedIdLabel)

$requestedIdText = New-Object System.Windows.Forms.TextBox
$requestedIdText.Location = New-Object System.Drawing.Point(72,13)
$requestedIdText.Size = New-Object System.Drawing.Size(100,28)
$requestedTopPanel.Controls.Add($requestedIdText)

$requestedAddButton = New-Object System.Windows.Forms.Button
$requestedAddButton.Text = 'ADD READ'
$requestedAddButton.Location = New-Object System.Drawing.Point(182,10)
$requestedAddButton.Size = New-Object System.Drawing.Size(110,32)
$requestedTopPanel.Controls.Add($requestedAddButton)

$requestedRemoveButton = New-Object System.Windows.Forms.Button
$requestedRemoveButton.Text = 'REMOVE SELECTED'
$requestedRemoveButton.Location = New-Object System.Drawing.Point(302,10)
$requestedRemoveButton.Size = New-Object System.Drawing.Size(165,32)
$requestedTopPanel.Controls.Add($requestedRemoveButton)

$requestedMeaningLabel = New-Object System.Windows.Forms.Label
$requestedMeaningLabel.Text = 'Directed reads appear in FIRE as REQUESTED. They remain profile-local and are not participation.'
$requestedMeaningLabel.Location = New-Object System.Drawing.Point(485,17)
$requestedMeaningLabel.Size = New-Object System.Drawing.Size(920,32)
$requestedTopPanel.Controls.Add($requestedMeaningLabel)

$requestedSplit = New-Object System.Windows.Forms.SplitContainer
$requestedSplit.Dock = 'Fill'
$requestedSplit.Orientation = 'Vertical'
$requestedSplit.SplitterDistance = 560
$requestedSplit.SplitterWidth = 6
$requestedTab.Controls.Add($requestedSplit)
$requestedTopPanel.BringToFront()

$requestedGrid = New-Object System.Windows.Forms.DataGridView
$requestedGrid.Dock = 'Fill'
$requestedGrid.ReadOnly = $true
$requestedGrid.AllowUserToAddRows = $false
$requestedGrid.AllowUserToDeleteRows = $false
$requestedGrid.SelectionMode = 'FullRowSelect'
$requestedGrid.MultiSelect = $false
$requestedGrid.AutoSizeColumnsMode = 'Fill'
$requestedSplit.Panel1.Controls.Add($requestedGrid)

$requestedText = New-Object System.Windows.Forms.TextBox
$requestedText.Dock = 'Fill'
$requestedText.Multiline = $true
$requestedText.ReadOnly = $true
$requestedText.ScrollBars = 'Both'
$requestedText.WordWrap = $true
$requestedText.Font = New-Object System.Drawing.Font('Segoe UI', 10)
$requestedText.Text = "Add a post ID to fetch it now and place it in FIRE as a clearly labelled REQUESTED read.`r`n`r`nThis changes no Square state and does not claim that Framework or CC read or understood it."
$requestedSplit.Panel2.Controls.Add($requestedText)

# ACT TAB
$airTab = New-Object System.Windows.Forms.TabPage
$airTab.Text = 'ACT'
$tabs.TabPages.Add($airTab)

$actTopPanel = New-Object System.Windows.Forms.Panel
$actTopPanel.Dock = 'Top'
$actTopPanel.Height = 150

$actBody = New-Object System.Windows.Forms.SplitContainer
$actBody.Dock = 'Fill'
$actBody.Orientation = 'Vertical'
$actBody.FixedPanel = [System.Windows.Forms.FixedPanel]::Panel2

$airTab.Controls.Add($actBody)
$airTab.Controls.Add($actTopPanel)

$loadPlanButton = New-Object System.Windows.Forms.Button
$loadPlanButton.Text = 'Load newest local plan'
$loadPlanButton.Location = New-Object System.Drawing.Point(12,10)
$loadPlanButton.Size = New-Object System.Drawing.Size(185,34)
$actTopPanel.Controls.Add($loadPlanButton)

$importComPlanButton = New-Object System.Windows.Forms.Button
$importComPlanButton.Text = 'Import latest COM plan'
$importComPlanButton.Location = New-Object System.Drawing.Point(207,10)
$importComPlanButton.Size = New-Object System.Drawing.Size(190,34)
$actTopPanel.Controls.Add($importComPlanButton)

$choosePlanButton = New-Object System.Windows.Forms.Button
$choosePlanButton.Text = 'Choose plan...'
$choosePlanButton.Location = New-Object System.Drawing.Point(407,10)
$choosePlanButton.Size = New-Object System.Drawing.Size(110,34)
$actTopPanel.Controls.Add($choosePlanButton)

$planPathLabel = New-Object System.Windows.Forms.Label
$planPathLabel.Text = 'No plan loaded.'
$planPathLabel.Location = New-Object System.Drawing.Point(12,52)
$planPathLabel.Size = New-Object System.Drawing.Size(1160,42)
$planPathLabel.Anchor = 'Top,Left,Right'
$actTopPanel.Controls.Add($planPathLabel)

$standingGrantLabel = New-Object System.Windows.Forms.Label
$standingGrantLabel.Text = 'Active profile grant not read yet.'
$standingGrantLabel.Location = New-Object System.Drawing.Point(12,98)
$standingGrantLabel.Size = New-Object System.Drawing.Size(1160,42)
$standingGrantLabel.Anchor = 'Top,Left,Right'
$actTopPanel.Controls.Add($standingGrantLabel)

$planText = New-ReadOnlyTextBox `
    -Location (New-Object System.Drawing.Point(0,0)) `
    -Size (New-Object System.Drawing.Size(700,600))

$planText.Dock = 'Fill'
$actBody.Panel1.Controls.Add($planText)

$actTable = New-Object System.Windows.Forms.TableLayoutPanel
$actTable.Dock = 'Fill'
$actTable.ColumnCount = 1
$actTable.RowCount = 4
$actTable.Padding = New-Object System.Windows.Forms.Padding(8)

[void]$actTable.ColumnStyles.Add(
    (
        New-Object System.Windows.Forms.ColumnStyle(
            [System.Windows.Forms.SizeType]::Percent,
            100
        )
    )
)

[void]$actTable.RowStyles.Add(
    (
        New-Object System.Windows.Forms.RowStyle(
            [System.Windows.Forms.SizeType]::Absolute,
            52
        )
    )
)

[void]$actTable.RowStyles.Add(
    (
        New-Object System.Windows.Forms.RowStyle(
            [System.Windows.Forms.SizeType]::Percent,
            65
        )
    )
)

[void]$actTable.RowStyles.Add(
    (
        New-Object System.Windows.Forms.RowStyle(
            [System.Windows.Forms.SizeType]::Absolute,
            60
        )
    )
)

[void]$actTable.RowStyles.Add(
    (
        New-Object System.Windows.Forms.RowStyle(
            [System.Windows.Forms.SizeType]::Percent,
            35
        )
    )
)

$actBody.Panel2.Controls.Add($actTable)

$preflightButton = New-Object System.Windows.Forms.Button
$preflightButton.Text = 'Check plan against LIVE Square'
$preflightButton.Dock = 'Fill'
$preflightButton.Enabled = $false
$actTable.Controls.Add($preflightButton,0,0)

$preflightText = New-ReadOnlyTextBox `
    -Location (New-Object System.Drawing.Point(0,0)) `
    -Size (New-Object System.Drawing.Size(400,300))

$preflightText.Dock = 'Fill'
$actTable.Controls.Add($preflightText,0,1)

$executeButton = New-Object System.Windows.Forms.Button
$executeButton.Text = 'RUN ACTIVE APERTURE PLAN'
$executeButton.Dock = 'Fill'
$executeButton.Enabled = $false

$executeButton.Font =
    New-Object System.Drawing.Font(
        'Segoe UI',
        10,
        [System.Drawing.FontStyle]::Bold
    )

$actTable.Controls.Add($executeButton,0,2)

$executionText = New-ReadOnlyTextBox `
    -Location (New-Object System.Drawing.Point(0,0)) `
    -Size (New-Object System.Drawing.Size(400,150))

$executionText.Dock = 'Fill'
$actTable.Controls.Add($executionText,0,3)

function Set-ActSplitter {
    try {
        $available =
            $actBody.ClientSize.Width -
            $actBody.SplitterWidth

        if($available -gt 800){
            $actBody.SplitterDistance =
                $available - 450
        }
    }
    catch { }
}

# WITNESS TAB
$witnessTab = New-Object System.Windows.Forms.TabPage
$witnessTab.Text = 'WITNESS'
$tabs.TabPages.Add($witnessTab)

$witnessText = New-ReadOnlyTextBox -Location (New-Object System.Drawing.Point(12,12)) -Size (New-Object System.Drawing.Size(1180,650))
$witnessText.Anchor = 'Top,Bottom,Left,Right'
$witnessText.Text = Get-WitnessSummary
$witnessTab.Controls.Add($witnessText)

$openLedgerButton = New-Object System.Windows.Forms.Button
$openLedgerButton.Text = 'Open event ledger'
$openLedgerButton.Location = New-Object System.Drawing.Point(12,675)
$openLedgerButton.Size = New-Object System.Drawing.Size(150,32)
$openLedgerButton.Anchor = 'Bottom,Left'
$witnessTab.Controls.Add($openLedgerButton)

# RELAY TAB
$relayTab = New-Object System.Windows.Forms.TabPage
$relayTab.Text = 'RELAY'
$tabs.TabPages.Add($relayTab)

$relayIntro = New-Object System.Windows.Forms.Label
$relayIntro.Text = 'CARRIER != APERTURE. Use bounded HEAD/THREAD for normal handoff. QUICK/FULL are forensic carriers and should normally stay cold.'
$relayIntro.Location = New-Object System.Drawing.Point(14,14)
$relayIntro.Size = New-Object System.Drawing.Size(1140,32)
$relayIntro.Anchor = 'Top,Left,Right'
$relayTab.Controls.Add($relayIntro)

$boundedReadsLabel = New-Object System.Windows.Forms.Label
$boundedReadsLabel.Text = 'BOUNDED READS - manual, <=64 KiB, no cursor acknowledgement'
$boundedReadsLabel.Location = New-Object System.Drawing.Point(14,48)
$boundedReadsLabel.Size = New-Object System.Drawing.Size(560,22)
$relayTab.Controls.Add($boundedReadsLabel)

$exportHeadButton = New-Object System.Windows.Forms.Button
$exportHeadButton.Text = 'EXPORT APERTURE HEAD'
$exportHeadButton.Location = New-Object System.Drawing.Point(14,72)
$exportHeadButton.Size = New-Object System.Drawing.Size(230,44)
$relayTab.Controls.Add($exportHeadButton)

$threadPostLabel = New-Object System.Windows.Forms.Label
$threadPostLabel.Text = 'Post ID:'
$threadPostLabel.Location = New-Object System.Drawing.Point(264,86)
$threadPostLabel.Size = New-Object System.Drawing.Size(52,22)
$relayTab.Controls.Add($threadPostLabel)

$threadPostIdBox = New-Object System.Windows.Forms.TextBox
$threadPostIdBox.Location = New-Object System.Drawing.Point(318,83)
$threadPostIdBox.Size = New-Object System.Drawing.Size(82,24)
$relayTab.Controls.Add($threadPostIdBox)

$exportThreadButton = New-Object System.Windows.Forms.Button
$exportThreadButton.Text = 'EXPORT THREAD'
$exportThreadButton.Location = New-Object System.Drawing.Point(414,72)
$exportThreadButton.Size = New-Object System.Drawing.Size(170,44)
$relayTab.Controls.Add($exportThreadButton)

$openDownloadsButton = New-Object System.Windows.Forms.Button
$openDownloadsButton.Text = 'Open Downloads'
$openDownloadsButton.Location = New-Object System.Drawing.Point(598,72)
$openDownloadsButton.Size = New-Object System.Drawing.Size(150,44)
$relayTab.Controls.Add($openDownloadsButton)

$verifyRelayButton = New-Object System.Windows.Forms.Button
$verifyRelayButton.Text = 'Verify artifact bytes...'
$verifyRelayButton.Location = New-Object System.Drawing.Point(762,72)
$verifyRelayButton.Size = New-Object System.Drawing.Size(180,44)
$relayTab.Controls.Add($verifyRelayButton)

$cancelExportButton = New-Object System.Windows.Forms.Button
$cancelExportButton.Text = 'CANCEL EXPORT'
$cancelExportButton.Location = New-Object System.Drawing.Point(956,72)
$cancelExportButton.Size = New-Object System.Drawing.Size(154,44)
$cancelExportButton.Enabled = $false
$relayTab.Controls.Add($cancelExportButton)

$forensicLabel = New-Object System.Windows.Forms.Label
$forensicLabel.Text = 'FORENSIC CARRIERS - normally leave cold'
$forensicLabel.Location = New-Object System.Drawing.Point(14,128)
$forensicLabel.Size = New-Object System.Drawing.Size(270,22)
$relayTab.Controls.Add($forensicLabel)

$exportQuickButton = New-Object System.Windows.Forms.Button
$exportQuickButton.Text = 'EXPORT FORENSIC QUICK'
$exportQuickButton.Location = New-Object System.Drawing.Point(14,152)
$exportQuickButton.Size = New-Object System.Drawing.Size(230,38)
$relayTab.Controls.Add($exportQuickButton)

$exportFullButton = New-Object System.Windows.Forms.Button
$exportFullButton.Text = 'EXPORT FORENSIC FULL'
$exportFullButton.Location = New-Object System.Drawing.Point(258,152)
$exportFullButton.Size = New-Object System.Drawing.Size(230,38)
$relayTab.Controls.Add($exportFullButton)

$bridgeLabel = New-Object System.Windows.Forms.Label
$bridgeLabel.Text = 'AUTOMATIC BRIDGES - one operator control per aperture; read/write circuits remain mechanically separate'
$bridgeLabel.Location = New-Object System.Drawing.Point(14,202)
$bridgeLabel.Size = New-Object System.Drawing.Size(900,22)
$relayTab.Controls.Add($bridgeLabel)

$readRelayStatusLabel = New-Object System.Windows.Forms.Label
$readRelayStatusLabel.Text = 'FRAMEWORK BRIDGE - checking local state...'
$readRelayStatusLabel.Location = New-Object System.Drawing.Point(14,230)
$readRelayStatusLabel.Size = New-Object System.Drawing.Size(1130,24)
$readRelayStatusLabel.Anchor = 'Top,Left,Right'
$relayTab.Controls.Add($readRelayStatusLabel)

$startReadRelayButton = New-Object System.Windows.Forms.Button
$startReadRelayButton.Text = 'START FRAMEWORK BRIDGE'
$startReadRelayButton.Location = New-Object System.Drawing.Point(14,258)
$startReadRelayButton.Size = New-Object System.Drawing.Size(230,42)
$relayTab.Controls.Add($startReadRelayButton)
$startReadRelayButton.BringToFront()

$stopReadRelayButton = New-Object System.Windows.Forms.Button
$stopReadRelayButton.Text = 'STOP FRAMEWORK BRIDGE'
$stopReadRelayButton.Location = New-Object System.Drawing.Point(258,258)
$stopReadRelayButton.Size = New-Object System.Drawing.Size(230,42)
$relayTab.Controls.Add($stopReadRelayButton)
$stopReadRelayButton.BringToFront()

$ccReadRelayStatusLabel = New-Object System.Windows.Forms.Label
$ccReadRelayStatusLabel.Text = 'CC BRIDGE - checking local state...'
$ccReadRelayStatusLabel.Location = New-Object System.Drawing.Point(14,312)
$ccReadRelayStatusLabel.Size = New-Object System.Drawing.Size(1130,24)
$ccReadRelayStatusLabel.Anchor = 'Top,Left,Right'
$relayTab.Controls.Add($ccReadRelayStatusLabel)

$startCcReadRelayButton = New-Object System.Windows.Forms.Button
$startCcReadRelayButton.Text = 'START CC BRIDGE'
$startCcReadRelayButton.Location = New-Object System.Drawing.Point(14,340)
$startCcReadRelayButton.Size = New-Object System.Drawing.Size(230,42)
$relayTab.Controls.Add($startCcReadRelayButton)
$startCcReadRelayButton.BringToFront()

$stopCcReadRelayButton = New-Object System.Windows.Forms.Button
$stopCcReadRelayButton.Text = 'STOP CC BRIDGE'
$stopCcReadRelayButton.Location = New-Object System.Drawing.Point(258,340)
$stopCcReadRelayButton.Size = New-Object System.Drawing.Size(230,42)
$relayTab.Controls.Add($stopCcReadRelayButton)
$stopCcReadRelayButton.BringToFront()

# R27 presentation repair: retain the Framework write circuit as a distinct
# mechanism, but remove its separate operator buttons. The combined Framework
# control starts/stops both circuits. A write circuit-breaker may still disable
# write while leaving bounded reads available.
$writeRelayStatusLabel = New-Object System.Windows.Forms.Label
$writeRelayStatusLabel.Visible = $false
$relayTab.Controls.Add($writeRelayStatusLabel)

$startWriteRelayButton = New-Object System.Windows.Forms.Button
$startWriteRelayButton.Visible = $false
$relayTab.Controls.Add($startWriteRelayButton)

$stopWriteRelayButton = New-Object System.Windows.Forms.Button
$stopWriteRelayButton.Visible = $false
$relayTab.Controls.Add($stopWriteRelayButton)

$relayText = New-ReadOnlyTextBox `
    -Location (New-Object System.Drawing.Point(14,396)) `
    -Size (New-Object System.Drawing.Size(1160,270))

$relayText.Anchor = 'Top,Bottom,Left,Right'
$relayText.Text = 'R27A consolidates operator controls without adding an authority class. Framework read (#175) and routine write (#177) remain separate circuits behind one Framework control. CC bounded read remains local; CC write is NOT YET INSTALLED. Framework remote write remains one post-level COMMENT only with exact grant binding, fresh preflight, no silent retry and read-after-write witness. Votes, threaded replies and higher-reach actions remain outside that remote lane.'
$relayTab.Controls.Add($relayText)

# UPDATE TAB
$updateTab = New-Object System.Windows.Forms.TabPage
$updateTab.Text = 'UPDATE'
$tabs.TabPages.Add($updateTab)

$updateIntro = New-Object System.Windows.Forms.Label
$updateIntro.Text = 'Verified local update: scans Downloads, binds from-SHA to this exact installed source, stages, hashes, parses, backs up, then replaces. No silent background install.'
$updateIntro.Location = New-Object System.Drawing.Point(14,14)
$updateIntro.Size = New-Object System.Drawing.Size(1130,50)
$updateIntro.Anchor = 'Top,Left,Right'
$updateTab.Controls.Add($updateIntro)

$checkUpdateButton = New-Object System.Windows.Forms.Button
$checkUpdateButton.Text = 'CHECK DOWNLOADS FOR UPDATE'
$checkUpdateButton.Location = New-Object System.Drawing.Point(14,72)
$checkUpdateButton.Size = New-Object System.Drawing.Size(250,44)
$updateTab.Controls.Add($checkUpdateButton)

$installUpdateButton = New-Object System.Windows.Forms.Button
$installUpdateButton.Text = 'INSTALL VERIFIED UPDATE'
$installUpdateButton.Location = New-Object System.Drawing.Point(278,72)
$installUpdateButton.Size = New-Object System.Drawing.Size(230,44)
$installUpdateButton.Enabled = $false
$updateTab.Controls.Add($installUpdateButton)

$updateOpenDownloadsButton = New-Object System.Windows.Forms.Button
$updateOpenDownloadsButton.Text = 'Open Downloads'
$updateOpenDownloadsButton.Location = New-Object System.Drawing.Point(522,72)
$updateOpenDownloadsButton.Size = New-Object System.Drawing.Size(150,44)
$updateTab.Controls.Add($updateOpenDownloadsButton)

$updateText = New-ReadOnlyTextBox `
    -Location (New-Object System.Drawing.Point(14,130)) `
    -Size (New-Object System.Drawing.Size(1160,540))
$updateText.Anchor = 'Top,Bottom,Left,Right'
$updateText.Text = 'No update checked this run.'
$updateTab.Controls.Add($updateText)

$script:VerifiedUpdateInspection = $null

# AUDIT TAB
$auditTab = New-Object System.Windows.Forms.TabPage
$auditTab.Text = 'Audit'
$tabs.TabPages.Add($auditTab)

$auditText = New-ReadOnlyTextBox -Location (New-Object System.Drawing.Point(12,12)) -Size (New-Object System.Drawing.Size(1180,585))
$auditText.Anchor = 'Top,Bottom,Left,Right'
$auditText.Text = $AuditEnglish
$auditTab.Controls.Add($auditText)

$sourceButton = New-Object System.Windows.Forms.Button
$sourceButton.Text = 'Open exact source in Notepad'
$sourceButton.Location = New-Object System.Drawing.Point(12,610)
$sourceButton.Size = New-Object System.Drawing.Size(200,34)
$sourceButton.Anchor = 'Bottom,Left'
$auditTab.Controls.Add($sourceButton)

$logButton = New-Object System.Windows.Forms.Button
$logButton.Text = 'Open actuation log'
$logButton.Location = New-Object System.Drawing.Point(222,610)
$logButton.Size = New-Object System.Drawing.Size(160,34)
$logButton.Anchor = 'Bottom,Left'
$auditTab.Controls.Add($logButton)

$selfTestButton = New-Object System.Windows.Forms.Button
$selfTestButton.Text = 'Run live READ-ONLY self-test'
$selfTestButton.Location = New-Object System.Drawing.Point(392,610)
$selfTestButton.Size = New-Object System.Drawing.Size(220,34)
$selfTestButton.Anchor = 'Bottom,Left'
$auditTab.Controls.Add($selfTestButton)

$selfTestText = New-ReadOnlyTextBox -Location (New-Object System.Drawing.Point(625,610)) -Size (New-Object System.Drawing.Size(555,90))
$selfTestText.Anchor = 'Bottom,Left,Right'
$auditTab.Controls.Add($selfTestText)

# ----------------------------- GUI BEHAVIOUR ----------------------------------
function New-PostTable($Rows) {
    $table = New-Object System.Data.DataTable
    [void]$table.Columns.Add('id',[int])
    [void]$table.Columns.Add('author',[string])
    [void]$table.Columns.Add('title',[string])
    [void]$table.Columns.Add('reason',[string])
    [void]$table.Columns.Add('comments',[string])
    [void]$table.Columns.Add('votes',[string])

    foreach ($p in @($Rows)) {
        $row = $table.NewRow()
        $row.id = [int](Safe-Property $p 'id' 0)
        $row.author = [string](Safe-Property $p 'author' '')
        $row.title = [string](Safe-Property $p 'title' '')
        $row.reason = [string](Safe-Property $p 'reason' '')
        $row.comments = [string](Safe-Property $p 'comments' '')
        $row.votes = [string](Safe-Property $p 'votes' '')
        $table.Rows.Add($row)
    }
    return ,$table
}

function Set-PostGridRows($Grid,$Rows) {
    $script:PopulatingGrid = $true
    try {
        $Grid.DataSource = $null
        $Grid.Rows.Clear()
        $Grid.Columns.Clear()

        foreach($spec in @(
            @{ name='id'; header='ID'; width=60 },
            @{ name='author'; header='Author'; width=145 },
            @{ name='title'; header='Title'; width=360 },
            @{ name='reason'; header='Why here'; width=240 },
            @{ name='comments'; header='Comments'; width=70 },
            @{ name='votes'; header='Votes'; width=55 }
        )) {
            $col = New-Object System.Windows.Forms.DataGridViewTextBoxColumn
            $col.Name = $spec.name
            $col.HeaderText = $spec.header
            $col.Width = $spec.width
            [void]$Grid.Columns.Add($col)
        }

        foreach($p in $Rows) {
            [void]$Grid.Rows.Add(
                [int](Safe-Property $p 'id' 0),
                [string](Safe-Property $p 'author' ''),
                [string](Safe-Property $p 'title' ''),
                [string](Safe-Property $p 'reason' ''),
                [string](Safe-Property $p 'comments' ''),
                [string](Safe-Property $p 'votes' '')
            )
        }

        if($Grid.Columns.Contains('title')) {
            $Grid.Columns['title'].AutoSizeMode = 'Fill'
        }

        $Grid.ClearSelection()
        $Grid.CurrentCell = $null
    }
    finally {
        $script:PopulatingGrid = $false
    }
}

function Set-RequestedReadGridRows($Rows) {
    $script:PopulatingGrid = $true
    try {
        $requestedGrid.DataSource = $null
        $requestedGrid.Rows.Clear()
        $requestedGrid.Columns.Clear()

        foreach ($spec in @(
            @{ name='status'; header='Source'; width=95 },
            @{ name='id'; header='ID'; width=65 },
            @{ name='author'; header='Author'; width=155 },
            @{ name='title'; header='Title'; width=420 },
            @{ name='comments'; header='Comments'; width=75 },
            @{ name='votes'; header='Votes'; width=60 }
        )) {
            $col = New-Object System.Windows.Forms.DataGridViewTextBoxColumn
            $col.Name = $spec.name
            $col.HeaderText = $spec.header
            $col.Width = $spec.width
            [void]$requestedGrid.Columns.Add($col)
        }

        foreach ($p in $Rows) {
            [void]$requestedGrid.Rows.Add(
                [string](Safe-Property $p 'status' 'REQUESTED'),
                [int](Safe-Property $p 'id' 0),
                [string](Safe-Property $p 'author' ''),
                [string](Safe-Property $p 'title' ''),
                [string](Safe-Property $p 'comments' ''),
                [string](Safe-Property $p 'votes' '')
            )
        }

        $requestedGrid.Columns['title'].AutoSizeMode = 'Fill'
        $requestedGrid.ClearSelection()
        $requestedGrid.CurrentCell = $null
    }
    finally {
        $script:PopulatingGrid = $false
    }
}

function Set-RequestedReadsSplitter {
    $width = [int]$requestedSplit.ClientSize.Width
    if ($width -lt 900) { return }
    $target = [int][Math]::Floor($width * 0.43)
    $target = [Math]::Max(500, $target)
    $target = [Math]::Min(($width - 560), $target)
    if ($target -gt 0 -and $requestedSplit.SplitterDistance -ne $target) {
        $requestedSplit.SplitterDistance = $target
    }
}

function Refresh-ReadRelayUiStatus {
    $readStatus = 'DEGRADED'
    $readEnabled = $false
    try {
        $readStatus = Get-ReadRelayHumanStatus
        $cfg = Get-ReadRelayConfig
        $readEnabled = [bool](Safe-Property $cfg 'enabled' $false)
    }
    catch {
        $readStatus = 'DEGRADED - ' + $_.Exception.Message
    }

    $writeStatus = 'DEGRADED'
    $writeEnabled = $false
    try {
        $writeStatus = Get-WriteRelayHumanStatus
        $writeCfg = Get-WriteRelayConfig
        $writeEnabled = [bool](Safe-Property $writeCfg 'enabled' $false)
    }
    catch {
        $writeStatus = 'DEGRADED - ' + $_.Exception.Message
    }

    # One operator surface, two independent circuits. If write trips its own
    # circuit breaker, Framework reads remain available and the START control
    # can retry only the missing capability.
    $readRelayStatusLabel.Text = "FRAMEWORK BRIDGE - READ: $readStatus | WRITE: $writeStatus"
    $startReadRelayButton.Enabled = (-not ($readEnabled -and $writeEnabled))
    $stopReadRelayButton.Enabled = ($readEnabled -or $writeEnabled)

    # Hidden compatibility controls retain the underlying circuit state for
    # existing code paths; they are not shown to the operator in R27.
    $writeRelayStatusLabel.Text = 'Framework routine write bridge: ' + $writeStatus
    $startWriteRelayButton.Enabled = (-not $writeEnabled)
    $stopWriteRelayButton.Enabled = $writeEnabled

    $ccReadStatus = 'DEGRADED'
    $ccReadEnabled = $false
    try {
        $ccReadStatus = Get-CcReadRelayHumanStatus
        $ccCfg = Get-CcReadRelayConfig
        $ccReadEnabled = [bool](Safe-Property $ccCfg 'enabled' $false)
    }
    catch { $ccReadStatus = 'DEGRADED - ' + $_.Exception.Message }

    $ccWriteStatus = 'DEGRADED'
    $ccWriteEnabled = $false
    try {
        $ccWriteStatus = Get-CcWriteRelayHumanStatus
        $ccWriteCfg = Get-CcWriteRelayConfig
        $ccWriteEnabled = [bool](Safe-Property $ccWriteCfg 'enabled' $false)
    }
    catch { $ccWriteStatus = 'DEGRADED - ' + $_.Exception.Message }

    $ccReadRelayStatusLabel.Text = "CC BRIDGE - READ: $ccReadStatus | WRITE: $ccWriteStatus"
    $startCcReadRelayButton.Enabled = (-not ($ccReadEnabled -and $ccWriteEnabled))
    $stopCcReadRelayButton.Enabled = ($ccReadEnabled -or $ccWriteEnabled)
}

function Refresh-UiState {
    try {
        $statusLabel.Text = "Reading live Square as $ActiveRole / $ExpectedCitizen..."
        $form.Refresh()
        $state = Capture-State
        $homeText.Text = ((Get-HumanHomeSummary) -split '\r?\n') -join [Environment]::NewLine

        Set-PostGridRows $postGrid (Get-FireRows $state)
        Set-PostGridRows $horizonGrid (Get-HorizonRows $state)
        Set-RequestedReadGridRows (Get-RequestedReadRows $state)
        $witnessText.Text = Get-WitnessSummary

        $today = $state.me.today
        $serverUtc = Safe-Property $state.front 'now_utc' '?'
        $statusLabel.Text = "$ActiveRole / $ExpectedCitizen | LIVE $serverUtc | posts $($today.posts_remaining) | comments $($today.comments_remaining) | votes $($today.votes_remaining)"
        $form.Text = "Campfire Square v$AppVersion - $ActiveRole / $ExpectedCitizen"
        $standingGrantLabel.Text = "Active grant: " + [string](Safe-Property (Get-ActiveGrant) 'grant_id' 'UNKNOWN') + " | routine: comment/vote | post: second-aperture review"
        $discovery = Safe-Property $state 'discovery' $null
        $horizonText.Text = "HORIZON DISCOVERY INDEX for $ExpectedCitizen. $([int](Safe-Property $discovery 'count' 0)) metadata rows of board total $([int](Safe-Property $discovery 'board_total' 0)); complete=$([bool](Safe-Property $discovery 'complete' $false)). Select any row to read it in full. Relay expansion uses disclosed strata and byte budget."
    }
    catch {
        $statusLabel.Text = "$ActiveRole / $ExpectedCitizen | READ FAILED: $($_.Exception.Message)"
        $homeText.Text = "READ FAILED`r`n`r`n$($_.Exception.Message)`r`n`r`nNo Square write was attempted."
    }
}

function Load-PlanFile([string]$Path) {
    try {
        if ([string]::IsNullOrWhiteSpace($Path) -or -not (Test-Path -LiteralPath $Path)) {
            throw 'Plan file does not exist.'
        }
        $rawPlanFileSha256 = Get-Sha256File $Path
        $raw = Read-Utf8TextFile $Path
        $plan = $raw | ConvertFrom-Json
        $errors = @(Validate-PlanShape $plan)

        $script:LoadedPlan = $plan
        $script:LoadedPlanPath = $Path
        $script:LoadedPlanRawSha256 = $rawPlanFileSha256
        $script:Preflight = $null
        $script:PreflightPlanHash = $null
        $script:PreflightRawPlanSha256 = $null
        $executeButton.Enabled = $false

        $planPathLabel.Text = $Path
        $planText.Text = Plan-ToEnglish $plan
        [void](Append-Event 'PLAN_LOADED' ([pscustomobject]@{
            plan_hash = Get-PlanHash $plan
            raw_plan_file_sha256 = $rawPlanFileSha256
            plan_path = $Path
            action_count = @(Safe-Property $plan 'actions' @()).Count
            requested_read_count = @(Get-PlanRequestedPostIds $plan).Count
        }) ([pscustomobject]@{
            local_file = $Path
            raw_file_sha256 = $rawPlanFileSha256
        }))

        if ($errors.Count -gt 0) {
            $preflightText.Text = "PLAN FORMAT FAILED:`r`n- " + ($errors -join "`r`n- ")
            $preflightButton.Enabled = $false
        }
        else {
            $preflightText.Text = 'Plan format looks valid. No write has occurred. Press live preflight.'
            $preflightButton.Enabled = $true
        }
    }
    catch {
        $script:LoadedPlan = $null
        $script:LoadedPlanPath = $null
        $script:LoadedPlanRawSha256 = $null
        $script:Preflight = $null
        $script:PreflightPlanHash = $null
        $script:PreflightRawPlanSha256 = $null
        $preflightButton.Enabled = $false
        $executeButton.Enabled = $false
        $planPathLabel.Text = 'Plan load failed.'
        $planText.Text = $_.Exception.Message
    }
}

$refreshButton.Add_Click({
    if ($script:ExportInProgress) { return }
    Refresh-UiState
})

$apertureCombo.Add_SelectedIndexChanged({
    if ($script:ExportInProgress) { return }
    try {
        $selected = [string]$apertureCombo.SelectedItem
        $target = $null
        foreach ($key in $ProfileCatalog.Keys) {
            if ([string]$ProfileCatalog[$key].display -eq $selected) {
                $target = [string]$ProfileCatalog[$key].citizen
                break
            }
        }
        if ([string]::IsNullOrWhiteSpace($target) -or $target -eq $ExpectedCitizen) { return }

        Set-ActiveProfile $target
        Reset-LoadedPlanState

        $planPathLabel.Text = 'No plan loaded for this aperture.'
        $planText.Text = ''
        $preflightText.Text = 'Aperture switched. Fresh live identity read required.'
        $executionText.Text = ''
        $preflightButton.Enabled = $false
        $executeButton.Enabled = $false
        $threadText.Text = ''
        $horizonText.Text = "HORIZON DISCOVERY INDEX for $ExpectedCitizen. Refreshing..."
        $requestedText.Text = "REQUESTED READS for $ExpectedCitizen. Refreshing..."
        $form.Text = "Campfire Square v$AppVersion - $ActiveRole / $ExpectedCitizen"

        Refresh-UiState
    }
    catch {
        $statusLabel.Text = "APERTURE SWITCH FAILED: $($_.Exception.Message)"
        [void][System.Windows.Forms.MessageBox]::Show(
            "Aperture switch failed closed.`r`n`r`n$($_.Exception.Message)",
            'Campfire Square',
            [System.Windows.Forms.MessageBoxButtons]::OK,
            [System.Windows.Forms.MessageBoxIcon]::Stop
        )
    }
})

$openDataButton.Add_Click({
    try { Start-Process explorer.exe -ArgumentList "`"$ProfileRoot`"" } catch { }
})

$postGrid.Add_SelectionChanged({
    try {
        if ($script:PopulatingGrid) { return }
        if ($postGrid.SelectedRows.Count -lt 1) { return }
        $postId = [int]$postGrid.SelectedRows[0].Cells['id'].Value
        if ($postId -le 0) { return }
        $threadText.Text = "Reading post #$postId..."
        if (Test-RequestedPostId $postId) {
            $thread = Get-FullThreadForExport $postId
            $script:CurrentThreads[$postId] = $thread
            Register-LocalOpen $postId 'REQUESTED_READ'
            $threadText.Text = (
                "DIRECTED READ #$postId`r`n" +
                "Visible in FIRE as REQUESTED; not participation and not a model-read claim.`r`n`r`n" +
                (Format-ThreadEnglish $thread)
            )
        }
        else {
            $thread = Get-Thread $postId
            Register-LocalOpen $postId 'FIRE'
            $threadText.Text = Format-ThreadEnglish $thread
        }
    } catch {
        $threadText.Text = "THREAD READ FAILED:`r`n$($_.Exception.Message)"
    }
})

$horizonGrid.Add_SelectionChanged({
    try {
        if ($script:PopulatingGrid) { return }
        if ($horizonGrid.SelectedRows.Count -lt 1) { return }
        $postId = [int]$horizonGrid.SelectedRows[0].Cells['id'].Value
        if ($postId -le 0) { return }
        $horizonText.Text = "Reading post #$postId..."
        $thread = Get-Thread $postId
        Register-LocalOpen $postId 'HORIZON'
        $horizonText.Text = Format-ThreadEnglish $thread
    } catch {
        $horizonText.Text = "THREAD READ FAILED:`r`n$($_.Exception.Message)"
    }
})

$requestedGrid.Add_SelectionChanged({
    try {
        if ($script:PopulatingGrid) { return }
        if ($requestedGrid.SelectedRows.Count -lt 1) { return }
        $postId = [int]$requestedGrid.SelectedRows[0].Cells['id'].Value
        if ($postId -le 0) { return }
        $requestedText.Text = "Reading requested post #$postId..."
        $thread = Get-FullThreadForExport $postId
        $script:CurrentThreads[$postId] = $thread
        Register-LocalOpen $postId 'REQUESTED_READ'
        $requestedText.Text = (
            "DIRECTED READ #$postId`r`n" +
            "Profile-local request; visible in FIRE as REQUESTED; no participation or cognition claim.`r`n`r`n" +
            (Format-ThreadEnglish $thread)
        )
    } catch {
        $requestedText.Text = "REQUESTED READ FAILED:`r`n$($_.Exception.Message)"
    }
})

$requestedAddButton.Add_Click({
    try {
        $postId = 0
        if (-not [int]::TryParse($requestedIdText.Text.Trim(), [ref]$postId) -or $postId -le 0) {
            throw 'Enter one positive numeric post ID.'
        }
        # Fail before persistence if the target does not exist, is unreachable,
        # or cannot be read completely under the thread pagination contract.
        $thread = Get-FullThreadForExport $postId
        $script:CurrentThreads[$postId] = $thread
        [void](Add-RequestedPostId $postId)
        Set-RequestedReadGridRows (Get-RequestedReadRows $script:CurrentState)
        Set-PostGridRows $postGrid (Get-FireRows $script:CurrentState)
        $requestedIdText.Text = ''
        Register-LocalOpen $postId 'REQUESTED_READ'
        $requestedText.Text = (
            "DIRECTED READ #$postId ADDED`r`n" +
            "It now appears in FIRE with source REQUESTED. No Square write, quota, vote, comment, cursor movement, karma effect, participation, model-read or cognition claim occurred.`r`n`r`n" +
            (Format-ThreadEnglish $thread)
        )
    } catch {
        $requestedText.Text = "ADD REQUESTED READ FAILED:`r`n$($_.Exception.Message)"
    }
})

$requestedRemoveButton.Add_Click({
    try {
        if ($requestedGrid.SelectedRows.Count -lt 1) { throw 'Select one requested post first.' }
        $postId = [int]$requestedGrid.SelectedRows[0].Cells['id'].Value
        [void](Remove-RequestedPostId $postId)
        Set-RequestedReadGridRows (Get-RequestedReadRows $script:CurrentState)
        Set-PostGridRows $postGrid (Get-FireRows $script:CurrentState)
        $requestedText.Text = "Post #$postId removed from the directed-read list and from FIRE's REQUESTED lane. If this citizen participates in the thread independently, it remains in FIRE for that separate reason. Existing evidence and prior packets remain unchanged."
    } catch {
        $requestedText.Text = "REMOVE REQUESTED READ FAILED:`r`n$($_.Exception.Message)"
    }
})

$loadPlanButton.Add_Click({
    $latest = Find-LatestPlanInDownloads
    if ($null -eq $latest) {
        [System.Windows.Forms.MessageBox]::Show(
            "No local action plan matching active citizen $ExpectedCitizen was found in Downloads.",
            'No matching local plan',
            [System.Windows.Forms.MessageBoxButtons]::OK,
            [System.Windows.Forms.MessageBoxIcon]::Information
        ) | Out-Null
        return
    }
    Load-PlanFile $latest
})

$importComPlanButton.Add_Click({
    try {
        $planPathLabel.Text = "Reading COM issue #$ComIssueNumber for $ActiveRole / $ExpectedCitizen..."
        $form.Refresh()
        $path = Import-LatestComPlanForActiveProfile
        Load-PlanFile $path
    }
    catch {
        [void][System.Windows.Forms.MessageBox]::Show(
            "COM plan import failed closed.`r`n`r`n$($_.Exception.Message)",
            'Campfire Square',
            [System.Windows.Forms.MessageBoxButtons]::OK,
            [System.Windows.Forms.MessageBoxIcon]::Stop
        )
    }
})

$choosePlanButton.Add_Click({
    $dialog = New-Object System.Windows.Forms.OpenFileDialog
    $dialog.InitialDirectory = $Downloads
    $dialog.Filter = 'Campfire action plans (*.json)|*.json|All files (*.*)|*.*'
    if ($dialog.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
        Load-PlanFile $dialog.FileName
    }
})

$preflightButton.Add_Click({
    if ($null -eq $script:LoadedPlan) { return }
    try {
        $executeButton.Enabled = $false
        $preflightText.Text = 'Running live preflight...'
        $form.Refresh()

        $pre = Preflight-Plan $script:LoadedPlan $script:LoadedPlanRawSha256
        $script:Preflight = $pre
        $script:PreflightPlanHash = $pre.plan_hash
        $script:PreflightRawPlanSha256 = $pre.raw_plan_file_sha256
        $preflightText.Text = $pre.summary
        [void](Append-Event ($(if ($pre.ok) { 'PREFLIGHT_PASSED' } else { 'PREFLIGHT_FAILED' })) ([pscustomobject]@{
            plan_hash = $pre.plan_hash
            raw_plan_file_sha256 = $pre.raw_plan_file_sha256
            summary = $pre.summary
            phase = 'active-aperture-preflight'
        }) ([pscustomobject]@{
            live_state_observed = $true
        }))
        $executeButton.Enabled = [bool]$pre.ok
        Refresh-UiState
    }
    catch {
        $script:Preflight = $null
        $script:PreflightPlanHash = $null
        $script:PreflightRawPlanSha256 = $null
        $executeButton.Enabled = $false
        $preflightText.Text = "PREFLIGHT FAILED:`r`n$($_.Exception.Message)"
    }
})

$executeButton.Add_Click({
    if ($null -eq $script:LoadedPlan -or
        $null -eq $script:Preflight -or
        -not $script:Preflight.ok -or
        [string]::IsNullOrWhiteSpace($script:PreflightPlanHash) -or
        [string]::IsNullOrWhiteSpace($script:PreflightRawPlanSha256)) {
        return
    }

    $shapeErrors = @(Validate-PlanShape $script:LoadedPlan)
    if ($shapeErrors.Count -gt 0) {
        [void][System.Windows.Forms.MessageBox]::Show(
            ("Plan no longer satisfies active aperture/grant:`r`n`r`n- " + ($shapeErrors -join "`r`n- ")),
            'Campfire Square',
            [System.Windows.Forms.MessageBoxButtons]::OK,
            [System.Windows.Forms.MessageBoxIcon]::Stop
        )
        return
    }

    $actions = @(Safe-Property $script:LoadedPlan 'actions' @())
    $localActions = @(Safe-Property $script:LoadedPlan 'local_actions' @())
    $requestedPostIds = @(Get-PlanRequestedPostIds $script:LoadedPlan)
    $hasSquareActions = ($actions.Count -gt 0)
    $grant = $null
    $grantSha = 'NOT_APPLICABLE_READ_ONLY_PLAN'

    if ($hasSquareActions) {
        try {
            $grant = Get-ActiveGrant
            $grantSha = Get-ActiveGrantSha256
        }
        catch {
            [void][System.Windows.Forms.MessageBox]::Show(
                "Active standing grant unavailable. Execution refused.`r`n`r`n$($_.Exception.Message)",
                'Campfire Square',
                [System.Windows.Forms.MessageBoxButtons]::OK,
                [System.Windows.Forms.MessageBoxIcon]::Stop
            )
            return
        }
    }

    $votes = @($actions | Where-Object { $_.type -eq 'vote' }).Count
    $comments = @($actions | Where-Object { $_.type -eq 'comment' }).Count
    $posts = @($actions | Where-Object { $_.type -eq 'post' }).Count

    $message = @"
ACTIVE APERTURE
$ActiveRole / $ExpectedCitizen

This local trigger will run the aperture-owned plan.

$($requestedPostIds.Count) profile-local requested read(s)
$($localActions.Count) local witness-investigation resolution(s)

$votes vote(s)
$comments comment/reply action(s)
$posts top-level post(s)

Canonical plan hash:
$($script:PreflightPlanHash)

Raw plan file SHA-256:
$($script:PreflightRawPlanSha256)

Actuation grant:
$(if ($hasSquareActions) { [string](Safe-Property $grant 'grant_id' 'UNKNOWN') + ' / ' + $grantSha } else { 'NOT APPLICABLE - THIS PLAN CONTAINS NO SQUARE WRITE ACTIONS' })

The complete live preflight will run again before any local state change or Square write.
Requested reads are verified completely before profile-local persistence.
$(if ($hasSquareActions) { 'Identity/quota/grant are checked again during execution. Every successful write must pass read-after-write witness.' } elseif ($localActions.Count -gt 0) { 'Fresh direct/public-thread evidence is checked again. No standing-grant trigger, Square write, quota use or public speech follows from this local-only plan.' } else { 'No standing-grant actuation trigger, Square write, quota use, vote, comment, post, cursor movement, karma effect or participation follows from this read-only plan.' })
No silent retries. First failure stops the batch.

THIS CLICK IS TRANSPORT / CREDENTIAL CUSTODY.
IT IS NOT MARK'S EDITORIAL APPROVAL OR ENDORSEMENT OF THE CONTENT.

Run this exact active-aperture plan?
"@

    $choice = [System.Windows.Forms.MessageBox]::Show(
        $message,
        'Run active aperture plan',
        [System.Windows.Forms.MessageBoxButtons]::YesNo,
        [System.Windows.Forms.MessageBoxIcon]::Warning
    )

    if ($choice -ne [System.Windows.Forms.DialogResult]::Yes) { return }

    if ($hasSquareActions) {
        [void](Append-Event 'STANDING_GRANT_TRIGGERED' ([pscustomobject]@{
            plan_hash = $script:PreflightPlanHash
            raw_plan_file_sha256 = $script:PreflightRawPlanSha256
            requested_post_ids = @($requestedPostIds)
            action_count = $actions.Count
            votes = $votes
            comments = $comments
            posts = $posts
            grant_id = [string](Safe-Property $grant 'grant_id' 'UNKNOWN')
            grant_sha256 = $grantSha
            trigger_surface = 'Campfire Square ACT local transport trigger'
            content_endorsement = $false
        }) ([pscustomobject]@{
            local_operator_trigger = $true
            operator_identity_used_as_content_authority = $false
            active_aperture = $ExpectedCitizen
            active_role = $ActiveRole
            triggered_at_utc = [DateTime]::UtcNow.ToString('o')
        }))
    }
    elseif ($localActions.Count -gt 0) {
        [void](Append-Event 'LOCAL_PLAN_TRIGGERED' ([pscustomobject]@{
            plan_hash = $script:PreflightPlanHash
            raw_plan_file_sha256 = $script:PreflightRawPlanSha256
            local_action_ids = @($localActions | ForEach-Object { [string](Safe-Property $_ 'id' '') })
            action_count = 0
            trigger_surface = 'Campfire Square ACT local transport trigger'
            content_endorsement = $false
            square_write = $false
        }) ([pscustomobject]@{
            local_operator_trigger = $true
            operator_identity_used_as_content_authority = $false
            standing_grant_triggered = $false
            active_aperture = $ExpectedCitizen
            active_role = $ActiveRole
            triggered_at_utc = [DateTime]::UtcNow.ToString('o')
        }))
    }
    else {
        [void](Append-Event 'READ_PLAN_TRIGGERED' ([pscustomobject]@{
            plan_hash = $script:PreflightPlanHash
            raw_plan_file_sha256 = $script:PreflightRawPlanSha256
            requested_post_ids = @($requestedPostIds)
            action_count = 0
            trigger_surface = 'Campfire Square ACT local transport trigger'
            content_endorsement = $false
            square_write = $false
        }) ([pscustomobject]@{
            local_operator_trigger = $true
            operator_identity_used_as_content_authority = $false
            standing_grant_triggered = $false
            active_aperture = $ExpectedCitizen
            active_role = $ActiveRole
            triggered_at_utc = [DateTime]::UtcNow.ToString('o')
        }))
    }

    try {
        $executeButton.Enabled = $false
        $executionText.Text = if ($hasSquareActions) {
            "Executing $ActiveRole / $ExpectedCitizen plan under active profile grant..."
        }
        elseif ($localActions.Count -gt 0) {
            "Resolving $ActiveRole / $ExpectedCitizen witness investigation from fresh public evidence..."
        }
        else {
            "Applying $ActiveRole / $ExpectedCitizen read-only requested-read plan..."
        }
        $form.Refresh()

        $results = @(Execute-AperturePlan $script:LoadedPlan $script:PreflightPlanHash $script:PreflightRawPlanSha256)
        $lines = [System.Collections.Generic.List[string]]::new()
        foreach ($r in $results) {
            $lines.Add("$($r.id): write=$($r.write_success) witness=$($r.witness_status)")
            if (-not $r.success) { $lines.Add("  batch stopped or action unresolved") }
        }
        $executionText.Text = ($lines -join "`r`n")

        $script:Preflight = $null
        $script:PreflightPlanHash = $null
        $script:PreflightRawPlanSha256 = $null
        $executeButton.Enabled = $false
        $preflightText.Text = if ($hasSquareActions) {
            'Execution finished. Live preflight cleared. Read-after-write witness recorded. Re-preflight before any further action.'
        }
        elseif ($localActions.Count -gt 0) {
            'Local evidence plan applied. Public projection confirmation and investigation disposition were appended; no Square write occurred.'
        }
        else {
            'Read-only plan applied. Live preflight cleared. Profile-local requested-read evidence recorded; no Square write occurred.'
        }
        Refresh-UiState
    }
    catch {
        $executionText.Text = "EXECUTION STOPPED:`r`n$($_.Exception.Message)"
        $script:Preflight = $null
        $script:PreflightPlanHash = $null
        $script:PreflightRawPlanSha256 = $null
        $executeButton.Enabled = $false
        Refresh-UiState
    }
})

$openLedgerButton.Add_Click({
    try {
        if (-not (Test-Path -LiteralPath $EventLedger)) { Write-Utf8NoBom $EventLedger '' }
        Start-Process notepad.exe -ArgumentList "`"$EventLedger`""
    } catch { }
})

function Start-RelayPacketExport([ValidateSet('QUICK','FULL')][string]$ExportMode) {
    if ($script:ExportInProgress) { return }
    try {
        $script:ExportInProgress = $true
        $script:ExportCancelRequested = $false
        $script:ExportStartedAtUtc = [DateTime]::UtcNow
        $script:ExportMode = $ExportMode

        $exportHeadButton.Enabled = $false
        $exportThreadButton.Enabled = $false
        $threadPostIdBox.Enabled = $false
        $exportQuickButton.Enabled = $false
        $exportFullButton.Enabled = $false
        $cancelExportButton.Enabled = $true
        $verifyRelayButton.Enabled = $false
        $openDownloadsButton.Enabled = $false
        $apertureCombo.Enabled = $false
        $refreshButton.Enabled = $false
        $autoCheck.Enabled = $false
        foreach ($page in $tabs.TabPages) {
            if ($page -ne $relayTab) { $page.Enabled = $false }
        }

        Update-ExportProgress -Phase "Starting $ExportMode export" -AllowCancellation

        $path =
            Export-CampfireRelayPacket -ExportMode $ExportMode

        $relayText.Text =
            "CAMPFIRE RELAY $ExportMode PACKET READY`r`n`r`n" +
            $path +
            "`r`n`r`nThis is a FORENSIC carrier. Keep it cold by default. Use APERTURE HEAD for the normal Framework/CC handoff." +
            "`r`nThe bearer secret is not included. The SHA-256 in the filename covers the exact raw file bytes."

        try {
            Set-Clipboard -Value $path
        }
        catch { }
    }
    catch [System.OperationCanceledException] {
        $relayText.Text = @"
EXPORT CANCELLED BEFORE REQUIRED REGIONS COMPLETED

No packet was written.
FIRE and requested-read regions are required and are not silently truncated.
Start a new export when ready.
"@
    }
    catch {

        $relayText.Text =
            "EXPORT FAILED`r`n`r`n" +
            $_.Exception.Message
    }
    finally {
        $script:ExportInProgress = $false
        $script:ExportCancelRequested = $false
        $script:ExportStartedAtUtc = $null
        $script:ExportMode = 'NONE'

        $exportHeadButton.Enabled = $true
        $exportThreadButton.Enabled = $true
        $threadPostIdBox.Enabled = $true
        $exportQuickButton.Enabled = $true
        $exportFullButton.Enabled = $true
        $cancelExportButton.Enabled = $false
        $verifyRelayButton.Enabled = $true
        $openDownloadsButton.Enabled = $true
        $apertureCombo.Enabled = $true
        $refreshButton.Enabled = $true
        $autoCheck.Enabled = $true
        foreach ($page in $tabs.TabPages) { $page.Enabled = $true }
    }
}

function Start-ApertureArtifactExport([ValidateSet('HEAD','THREAD')][string]$Kind, [int]$PostId = 0) {
    if ($script:ExportInProgress) { return }
    try {
        $script:ExportInProgress = $true
        $script:ExportCancelRequested = $false
        $script:ExportStartedAtUtc = [DateTime]::UtcNow
        $script:ExportMode = if ($Kind -eq 'THREAD') { "THREAD #$PostId" } else { 'HEAD' }

        $exportHeadButton.Enabled = $false
        $exportThreadButton.Enabled = $false
        $threadPostIdBox.Enabled = $false
        $exportQuickButton.Enabled = $false
        $exportFullButton.Enabled = $false
        $cancelExportButton.Enabled = $true
        $verifyRelayButton.Enabled = $false
        $openDownloadsButton.Enabled = $false
        $apertureCombo.Enabled = $false
        $refreshButton.Enabled = $false
        $autoCheck.Enabled = $false
        foreach ($page in $tabs.TabPages) {
            if ($page -ne $relayTab) { $page.Enabled = $false }
        }

        $path = if ($Kind -eq 'HEAD') {
            Export-CampfireApertureHead
        }
        else {
            Export-CampfireApertureThread $PostId
        }

        $relayText.Text = if ($Kind -eq 'HEAD') {
            "APERTURE HEAD READY`r`n`r`n$path`r`n`r`nUpload this HEAD to Framework or CC. It contains no post/comment bodies and is hard-bounded to 64 KiB.`r`nIf a specific thread is needed, export that post separately."
        }
        else {
            "APERTURE THREAD #$PostId READY`r`n`r`n$path`r`n`r`nUpload this one bounded thread artifact. Omitted comments, if any, are disclosed in the artifact."
        }
        try { Set-Clipboard -Value $path } catch { }
    }
    catch [System.OperationCanceledException] {
        $relayText.Text = "APERTURE EXPORT CANCELLED`r`n`r`nNo bounded artifact was accepted as complete. Start a new export when ready."
    }
    catch {
        $relayText.Text = "APERTURE EXPORT FAILED`r`n`r`n" + $_.Exception.Message
    }
    finally {
        $script:ExportInProgress = $false
        $script:ExportCancelRequested = $false
        $script:ExportStartedAtUtc = $null
        $script:ExportMode = 'NONE'

        $exportHeadButton.Enabled = $true
        $exportThreadButton.Enabled = $true
        $threadPostIdBox.Enabled = $true
        $exportQuickButton.Enabled = $true
        $exportFullButton.Enabled = $true
        $cancelExportButton.Enabled = $false
        $verifyRelayButton.Enabled = $true
        $openDownloadsButton.Enabled = $true
        $apertureCombo.Enabled = $true
        $refreshButton.Enabled = $true
        $autoCheck.Enabled = $true
        foreach ($page in $tabs.TabPages) { $page.Enabled = $true }
    }
}

$exportHeadButton.Add_Click({
    Start-ApertureArtifactExport -Kind 'HEAD'
})

$exportThreadButton.Add_Click({
    $postId = 0
    if (-not [int]::TryParse($threadPostIdBox.Text.Trim(),[ref]$postId) -or $postId -le 0) {
        $relayText.Text = 'THREAD EXPORT NEEDS A POSITIVE NUMERIC POST ID.'
        return
    }
    Start-ApertureArtifactExport -Kind 'THREAD' -PostId $postId
})

$exportQuickButton.Add_Click({
    Start-RelayPacketExport -ExportMode 'QUICK'
})

$exportFullButton.Add_Click({
    Start-RelayPacketExport -ExportMode 'FULL'
})

$cancelExportButton.Add_Click({
    if (-not $script:ExportInProgress) { return }
    $script:ExportCancelRequested = $true
    $cancelExportButton.Enabled = $false
    $relayText.Text = @"
CANCELLATION REQUESTED

The current network operation is being interrupted.
If required FIRE/requested regions are incomplete, no packet will be written.
If optional Horizon expansion has begun, the packet will finish with
expansion_stop_cause = USER_CANCELLED.
"@
    [System.Windows.Forms.Application]::DoEvents()
})

$openDownloadsButton.Add_Click({

    try {
        Start-Process `
            explorer.exe `
            (Join-Path $env:USERPROFILE 'Downloads')
    }
    catch { }
})
$verifyRelayButton.Add_Click({

    try {

        $dialog =
            New-Object System.Windows.Forms.OpenFileDialog

        $dialog.Title =
            'Choose Campfire Relay artifact'

        $dialog.InitialDirectory =
            Join-Path $env:USERPROFILE 'Downloads'

        $dialog.Filter =
            'Campfire Relay JSON artifact (*.json)|*.json'

        if(
            $dialog.ShowDialog() -ne
            [System.Windows.Forms.DialogResult]::OK
        ){
            return
        }

        $path =
            $dialog.FileName

        $name =
            [IO.Path]::GetFileName($path)

        $match =
            [regex]::Match(
                $name,
                '__SHA256_([0-9a-fA-F]{64})\.json$'
            )

        if(-not $match.Success){

            $relayText.Text =
                "VERIFY FAILED`r`n`r`n" +
                'Filename does not contain a Campfire Relay exact-byte SHA-256.'

            return
        }

        $expected =
            $match.Groups[1].Value.ToLowerInvariant()

        $actual =
            (
                Get-FileHash `
                    -LiteralPath $path `
                    -Algorithm SHA256
            ).Hash.ToLowerInvariant()

        $bytes =
            (Get-Item -LiteralPath $path).Length

        if($actual -eq $expected){

            $relayText.Text =
                "EXACT-BYTE VERIFY: MATCH`r`n`r`n" +
                "Bytes: $bytes`r`n" +
                "SHA-256: $actual`r`n`r`n" +
                'This establishes carrier byte identity only.' +
                "`r`nIt does not establish truth, freshness, reading or comprehension."

        }
        else {

            $relayText.Text =
                "EXACT-BYTE VERIFY: MISMATCH`r`n`r`n" +
                "Expected: $expected`r`n" +
                "Actual:   $actual`r`n`r`n" +
                'Do not use this packet as the claimed artifact.'
        }

    }
    catch {

        $relayText.Text =
            "VERIFY FAILED`r`n`r`n" +
            $_.Exception.Message
    }
})
$startReadRelayButton.Add_Click({
    $errors = [System.Collections.Generic.List[string]]::new()
    try {
        $readRelayStatusLabel.Text = 'FRAMEWORK BRIDGE - starting bounded read + routine comment circuits...'
        $form.Refresh()

        try {
            $cfg = Get-ReadRelayConfig
            if (-not [bool](Safe-Property $cfg 'enabled' $false)) {
                Initialize-ReadRelay
            }
        }
        catch {
            $errors.Add('READ: ' + $_.Exception.Message)
        }

        try {
            $writeCfg = Get-WriteRelayConfig
            if (-not [bool](Safe-Property $writeCfg 'enabled' $false)) {
                Initialize-WriteRelay
            }
        }
        catch {
            try { Disable-WriteRelay } catch { }
            $errors.Add('WRITE: ' + $_.Exception.Message)
        }

        Refresh-ReadRelayUiStatus

        if ($errors.Count -gt 0) {
            $relayText.Text = @"
FRAMEWORK BRIDGE PARTIAL / DEGRADED

$($errors -join "`r`n")

The read and write circuits are mechanically separate. A write-side refusal does not disable bounded reads. No failed/ambiguous Square write is silently retried.
"@
        }
        else {
            $relayText.Text = @"
FRAMEWORK BRIDGE ENABLED

READ
- private machine lane: $ReadRelayRepo issue #$ReadRelayIssueNumber
- allowed: HEAD or one THREAD for framework-relay
- hard object ceiling: 65536 bytes
- no cursor acknowledgement; no FULL/QUICK

WRITE
- private machine lane: $ReadRelayRepo issue #$WriteRelayIssueNumber
- allowed: exactly one post-level COMMENT per request
- exact standing-grant id + SHA binding
- fresh identity/quota/target/replay/obligation preflight
- read-after-write witness required
- no silent Square retry
- unknown/unverified outcome disables WRITE without disabling READ

OUTSIDE REMOTE WRITE
threaded replies, votes, top-level posts, batches, money/treasury, credentials, grant mutation, cursor acknowledgement, correction-debt closure, requested-read/local-evidence actions, CC writes and FULL/QUICK.

One operator control does not merge the underlying authority or failure circuits.
"@
        }
    }
    catch {
        Refresh-ReadRelayUiStatus
        $readRelayStatusLabel.Text = 'FRAMEWORK BRIDGE - START FAILED - ' + $_.Exception.Message
    }
})

$stopReadRelayButton.Add_Click({
    $errors = [System.Collections.Generic.List[string]]::new()
    try {
        try { Disable-WriteRelay } catch { $errors.Add('WRITE: ' + $_.Exception.Message) }
        try { Disable-ReadRelay } catch { $errors.Add('READ: ' + $_.Exception.Message) }
        Refresh-ReadRelayUiStatus

        if ($errors.Count -gt 0) {
            $relayText.Text = "FRAMEWORK BRIDGE STOP PARTIAL / DEGRADED`r`n`r`n" + ($errors -join "`r`n")
        }
        else {
            $relayText.Text = "FRAMEWORK BRIDGE stopped. No new remote Framework reads or routine comments will be dispatched. Already-running bounded reads may finish; an already-issued Square write is never silently retried."
        }
    }
    catch {
        Refresh-ReadRelayUiStatus
        $readRelayStatusLabel.Text = 'FRAMEWORK BRIDGE - STOP FAILED - ' + $_.Exception.Message
    }
})

$startCcReadRelayButton.Add_Click({
    $errors = [System.Collections.Generic.List[string]]::new()
    try {
        $ccReadRelayStatusLabel.Text = 'CC BRIDGE - starting bounded read + local routine comment circuits...'
        $form.Refresh()
        try {
            $ccCfg = Get-CcReadRelayConfig
            if (-not [bool](Safe-Property $ccCfg 'enabled' $false)) { Initialize-CcReadRelay }
        }
        catch { $errors.Add('READ: ' + $_.Exception.Message) }
        try {
            $ccWriteCfg = Get-CcWriteRelayConfig
            if (-not [bool](Safe-Property $ccWriteCfg 'enabled' $false)) { Initialize-CcWriteRelay }
        }
        catch {
            try { Disable-CcWriteRelay } catch { }
            $errors.Add('WRITE: ' + $_.Exception.Message)
        }
        Refresh-ReadRelayUiStatus
        if ($errors.Count -gt 0) {
            $relayText.Text = @"
CC BRIDGE PARTIAL / DEGRADED

$($errors -join "`r`n")

The CC read and write circuits are mechanically separate. A write-side refusal does not disable bounded reads. No failed or ambiguous Square write is silently retried.
"@
        }
        else {
            $relayText.Text = @"
CC BRIDGE ENABLED

READ
- transport: LOCAL FILESYSTEM ONLY
- ingress: $CcReadRelayIngress
- responses: $CcReadRelayResponses
- artifacts: $CcReadRelayOutbox
- allowed: HEAD or one THREAD for cc-relay
- hard object ceiling: 65536 bytes
- no cursor acknowledgement; no FULL/QUICK

WRITE
- transport: LOCAL FILESYSTEM ONLY
- ingress: $CcWriteRelayIngress
- responses: $CcWriteRelayResponses
- allowed: exactly one post-level COMMENT per request
- COMMENT-only narrows transport/target shape; it is not a semantic harmlessness claim
- content authority remains CC; body semantics are not machine-screened for truth/harm/fitness
- if files exist before enable, first START records names+SHA256 and refuses; second START acknowledges only an unchanged set and archives it without execution
- exact cc-relay standing-grant id + SHA binding
- fresh identity/quota/target/replay/obligation preflight
- read-after-write witness required
- no silent Square retry
- unknown/unverified outcome disables WRITE without disabling READ

OUTSIDE CC ROUTINE WRITE
threaded replies, votes, top-level posts, batches, money/treasury, credentials, grant mutation, cursor acknowledgement, correction-debt closure, Framework ingress and FULL/QUICK.

One operator control does not merge the underlying authority or failure circuits.
"@
        }
    }
    catch {
        Refresh-ReadRelayUiStatus
        $ccReadRelayStatusLabel.Text = 'CC BRIDGE - START FAILED - ' + $_.Exception.Message
    }
})

$stopCcReadRelayButton.Add_Click({
    $errors = [System.Collections.Generic.List[string]]::new()
    try {
        try { Disable-CcWriteRelay } catch { $errors.Add('WRITE: ' + $_.Exception.Message) }
        try { Disable-CcReadRelay } catch { $errors.Add('READ: ' + $_.Exception.Message) }
        Refresh-ReadRelayUiStatus
        if ($errors.Count -gt 0) {
            $relayText.Text = "CC BRIDGE STOP PARTIAL / DEGRADED`r`n`r`n" + ($errors -join "`r`n")
        }
        else {
            $relayText.Text = "CC BRIDGE stopped. No new local CC bounded reads or routine comments will be dispatched. Already-running bounded reads may finish; an already-issued Square write is never silently retried."
        }
    }
    catch {
        Refresh-ReadRelayUiStatus
        $ccReadRelayStatusLabel.Text = 'CC BRIDGE - STOP FAILED - ' + $_.Exception.Message
    }
})

$checkUpdateButton.Add_Click({
    $installUpdateButton.Enabled = $false
    $script:VerifiedUpdateInspection = $null
    try {
        $package = Find-LatestUpdatePackage
        if ($null -eq $package) {
            $updateText.Text = "No CAMPFIRE_SQUARE_UPDATE_*.zip found in Downloads."
            return
        }

        $updateText.Text = "Inspecting update package...`r`n$package"
        $form.Refresh()

        $inspection = Inspect-UpdatePackage $package
        $script:VerifiedUpdateInspection = $inspection
        $updateText.Text = $inspection.summary
        $installUpdateButton.Enabled = $true
    }
    catch {
        $message = [string]$_.Exception.Message
        if ($message.StartsWith('NO_APPLICABLE_UPDATE')) {
            $lines = @($message -split '\r?\n')
            $detail = @($lines | Select-Object -Skip 1) -join "`r`n"
            $updateText.Text =
                "NO APPLICABLE UPDATE`r`n`r`n" +
                $detail +
                "`r`n`r`nThis is not an install failure. It means Downloads contains no verified next-hop package from the exact source currently installed."
        }
        else {
            $updateText.Text = "UPDATE CHECK FAILED CLOSED`r`n`r`n$message"
        }
    }
})

$installUpdateButton.Add_Click({
    if ($null -eq $script:VerifiedUpdateInspection) { return }

    $inspection = $script:VerifiedUpdateInspection
    $boundaryLine = if ([bool]$inspection.boundary_change) {
        "`r`nWARNING: this update declares an actuation/grant boundary change."
    } else {
        "`r`nThe package declares no actuation/grant boundary change."
    }

    $choice = [System.Windows.Forms.MessageBox]::Show(
        (
            "Install verified Campfire Square update?`r`n`r`n" +
            "Current SHA: $($inspection.current_sha256)`r`n" +
            "Target version: $($inspection.target_version)`r`n" +
            "Target SHA: $($inspection.target_sha256)" +
            $boundaryLine +
            "`r`n`r`nThe existing source will be backed up first."
        ),
        'Install verified update',
        [System.Windows.Forms.MessageBoxButtons]::YesNo,
        [System.Windows.Forms.MessageBoxIcon]::Warning
    )

    if ($choice -ne [System.Windows.Forms.DialogResult]::Yes) { return }

    try {
        $result = Install-VerifiedUpdate $inspection
        $updateText.Text = "UPDATE INSTALLED`r`n`r`nVersion: $($result.version)`r`nSHA-256: $($result.sha256)`r`n`r`nRelaunching..."
        $form.Refresh()

        Start-Process powershell.exe -ArgumentList (
            "-NoProfile -ExecutionPolicy Bypass -File `"$InstalledScript`""
        )

        $form.Close()
    }
    catch {
        $installUpdateButton.Enabled = $false
        $script:VerifiedUpdateInspection = $null
        $updateText.Text = "UPDATE INSTALL FAILED`r`n`r`n$($_.Exception.Message)"
    }
})

$updateOpenDownloadsButton.Add_Click({
    try { Start-Process explorer.exe (Join-Path $env:USERPROFILE 'Downloads') } catch { }
})

$sourceButton.Add_Click({
    try { Start-Process notepad.exe -ArgumentList "`"$InstalledScript`"" } catch { }
})

$logButton.Add_Click({
    try {
        if (-not (Test-Path -LiteralPath $ActionLog)) {
            Write-Utf8NoBom $ActionLog ''
        }
        Start-Process notepad.exe -ArgumentList "`"$ActionLog`""
    } catch { }
})

$selfTestButton.Add_Click({
    $selfTestText.Text = 'Running live read-only self-test...'
    $form.Refresh()
    try {
        $result = Run-SelfTest
        $selfTestText.Text = $result.text
    } catch {
        $selfTestText.Text = "SELF-TEST FAILED TO COMPLETE:`r`n$($_.Exception.Message)"
    }
})

$readRelayTimer = New-Object System.Windows.Forms.Timer
$readRelayTimer.Interval = $ReadRelayPollSeconds * 1000
$readRelayTimer.Add_Tick({
    try { Invoke-ReadRelayPoll }
    catch { $readRelayStatusLabel.Text = 'FRAMEWORK BRIDGE - READ POLL FAILED - ' + $_.Exception.Message }
    try { Invoke-CcReadRelayPoll }
    catch { $ccReadRelayStatusLabel.Text = 'CC BRIDGE - READ POLL FAILED - ' + $_.Exception.Message }
    try { Invoke-CcWriteRelayPoll }
    catch { $ccReadRelayStatusLabel.Text = 'CC BRIDGE - WRITE POLL FAILED - ' + $_.Exception.Message }
    try { Invoke-WriteRelayPoll }
    catch { $writeRelayStatusLabel.Text = 'Framework routine write bridge: POLL FAILED - ' + $_.Exception.Message }
    Refresh-ReadRelayUiStatus
})
$readRelayTimer.Start()

$timer = New-Object System.Windows.Forms.Timer
$timer.Interval = $RefreshSeconds * 1000
$timer.Add_Tick({
    if (-not $script:ExportInProgress -and $autoCheck.Checked) {
        Refresh-UiState
    }
})
$timer.Start()

$form.Add_Shown({
    Set-RequestedReadsSplitter
    try { Protect-CcWriteRelayAfterR28DUpgrade } catch { $relayText.Text = 'CC WRITE R28E UPGRADE GUARD FAILED: ' + $_.Exception.Message }
    Refresh-UiState
    Refresh-ReadRelayUiStatus
    # Surface a matching local plan if one exists; never load or execute it automatically.
    $latest = Find-LatestPlanInDownloads
    if ($null -ne $latest) {
        $planPathLabel.Text = "Local plan available for $ActiveRole / ${ExpectedCitizen}: $latest`r`nPress 'Load newest local plan' to inspect it."
    }
})

$form.Add_SizeChanged({
    Set-ActSplitter
    Set-RequestedReadsSplitter
})

$form.Add_FormClosing({
    param($sender,$eventArgs)
    if ($script:ExportInProgress) {
        $script:ExportCancelRequested = $true
        $eventArgs.Cancel = $true
        $relayText.Text = @"
CLOSE REQUEST RECEIVED AS EXPORT CANCELLATION

The current network operation is being interrupted safely.
Close the window again after the export has stopped.
"@
        [System.Windows.Forms.Application]::DoEvents()
    }
})

$form.Add_FormClosed({
    $readRelayTimer.Stop()
    $readRelayTimer.Dispose()
    $timer.Stop()
    $timer.Dispose()
})

[void]$form.ShowDialog()
