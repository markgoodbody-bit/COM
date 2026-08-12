$ErrorActionPreference = 'Stop'

$expectedCurrent =
    '352a8ae35df20bea4df8d6667391219d069868ca52bd7cb25d5ec378b62bd537'

$expectedPackage =
    'f4425009db6883127fea173a6841350b6ca926cc3085bc1fe0b773f9b7fd2108'

$expectedTarget =
    '1132750c5b7e603df9ca9fc44bf0cc25db65177df29b3c572c20c6073f9e3e76'

$expectedFilename =
    'CAMPFIRE_SQUARE_UPDATE_v0.5.3_FROM_v0.5.2_REQUESTED_READING_WORKING_CANDIDATE_R2.zip'

$receiptUrl =
    'https://raw.githubusercontent.com/markgoodbody-bit/COM/main/CAMPFIRE_SQUARE_UPDATE_RECEIPTS/f4425009db6883127fea173a6841350b6ca926cc3085bc1fe0b773f9b7fd2108.json'

$docs = [Environment]::GetFolderPath('MyDocuments')
if ([string]::IsNullOrWhiteSpace($docs)) {
    $docs = Join-Path $env:USERPROFILE 'Documents'
}

$root = Join-Path $docs 'Campfire-Square'
$app = Join-Path $root 'App\Campfire-Square.ps1'
$downloads = Join-Path $env:USERPROFILE 'Downloads'

if (-not (Test-Path -LiteralPath $app)) {
    throw "Campfire Square not found: $app"
}

$running = @(
    Get-Process powershell,pwsh -ErrorAction SilentlyContinue |
    Where-Object { $_.MainWindowTitle -like '*Campfire Square*' }
)

if ($running.Count -gt 0) {
    throw 'Close every Campfire Square window, then run this block again.'
}

$current = (
    Get-FileHash -LiteralPath $app -Algorithm SHA256
).Hash.ToLowerInvariant()

if ($current -ne $expectedCurrent) {
    throw @"
CURRENT SOURCE DOES NOT MATCH VERIFIED v0.5.2.

Expected:
$expectedCurrent

Found:
$current

Nothing changed.
"@
}

$packages = @(
    Get-ChildItem `
        -LiteralPath $downloads `
        -File `
        -Filter 'CAMPFIRE_SQUARE_UPDATE_v0.5.3_FROM_v0.5.2_REQUESTED_READING_WORKING_CANDIDATE_R2*.zip' `
        -ErrorAction SilentlyContinue |
    ForEach-Object {
        $sha = (
            Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256
        ).Hash.ToLowerInvariant()

        if ($sha -eq $expectedPackage) {
            [pscustomobject]@{
                path = $_.FullName
                modified = $_.LastWriteTimeUtc
            }
        }
    } |
    Sort-Object modified -Descending
)

if ($packages.Count -eq 0) {
    throw @"
R2 PACKAGE NOT FOUND OR HASH DOES NOT MATCH.

Expected filename:
$expectedFilename

Expected SHA-256:
$expectedPackage

Download R2 into Downloads and run this block again.
"@
}

$package = $packages[0].path

try {
    [Net.ServicePointManager]::SecurityProtocol =
        [Net.ServicePointManager]::SecurityProtocol -bor
        [Net.SecurityProtocolType]::Tls12
}
catch { }

function Read-Utf8TextFromUri([string]$Uri) {
    $request = [System.Net.WebRequest]::Create($Uri)
    $request.Method = 'GET'
    $request.Timeout = 30000
    $request.UserAgent = 'Campfire-Square-v0.5.3-R2-bootstrap'
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

$receipt = $null
$receiptError = $null

for ($attempt = 1; $attempt -le 6; $attempt++) {
    try {
        $nonce = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()
        $receiptText = Read-Utf8TextFromUri (
            $receiptUrl +
            '?campfire_attempt=' +
            $attempt +
            '&t=' +
            $nonce
        )
        $receipt = $receiptText | ConvertFrom-Json
        if ($null -ne $receipt) { break }
    }
    catch {
        $receiptError = $_.Exception.Message
    }

    if ($attempt -lt 6) {
        Start-Sleep -Seconds (2 * $attempt)
    }
}

if ($null -eq $receipt) {
    throw @"
EXACT COM RECEIPT COULD NOT BE READ.

URL:
$receiptUrl

Last error:
$receiptError

Nothing changed.
"@
}

if (
    [string]$receipt.carrier_type -ne 'COM_REPOSITORY_EXACT_PATH' -or
    [string]$receipt.status -ne 'CANDIDATE_AVAILABLE' -or
    [string]$receipt.issuer_login -ne 'markgoodbody-bit' -or
    [int]$receipt.candidate_revision -ne 2 -or
    [string]$receipt.from_source_sha256 -ne $expectedCurrent -or
    [string]$receipt.to_source_sha256 -ne $expectedTarget -or
    [string]$receipt.package_sha256 -ne $expectedPackage -or
    [string]$receipt.package_filename -ne $expectedFilename -or
    [bool]$receipt.grant_surface_changed -ne $false -or
    [bool]$receipt.network_write_routes_changed -ne $false
) {
    throw 'Exact COM receipt does not describe this R2 transition. Nothing changed.'
}

Write-Host ''
Write-Host 'EXACT PACKAGE-KEYED COM RECEIPT: PASS'
Write-Host $receiptUrl

$stage = Join-Path (
    [IO.Path]::GetTempPath()
) ('Campfire-Square-v053-R2-' + [guid]::NewGuid().ToString('n'))

New-Item -ItemType Directory -Force -Path $stage | Out-Null

$backupRoot = Join-Path $root (
    'Backups\v0.5.3-R2-bootstrap-' +
    [DateTime]::UtcNow.ToString('yyyyMMdd_HHmmssZ')
)

New-Item -ItemType Directory -Force -Path $backupRoot | Out-Null

$backup = Join-Path $backupRoot 'Campfire-Square.v0.5.2.ps1'
Copy-Item -LiteralPath $app -Destination $backup -Force

try {
    Expand-Archive -LiteralPath $package -DestinationPath $stage -Force

    $manifestPath = Join-Path $stage 'manifest.json'
    $newSource = Join-Path $stage 'Campfire-Square.ps1'

    foreach ($required in @($manifestPath,$newSource)) {
        if (-not (Test-Path -LiteralPath $required)) {
            throw "Update package incomplete: $required"
        }
    }

    $manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json

    if (
        [string]$manifest.package_type -ne 'campfire-square-update' -or
        [int]$manifest.candidate_revision -ne 2 -or
        [string]$manifest.from_version -ne '0.5.2' -or
        [string]$manifest.from_source_sha256 -ne $expectedCurrent -or
        [string]$manifest.to_version -ne '0.5.3' -or
        [string]$manifest.to_source_sha256 -ne $expectedTarget -or
        [bool]$manifest.grant_surface_changed -ne $false
    ) {
        throw 'Package manifest describes the wrong transition.'
    }

    $sourceSha = (
        Get-FileHash -LiteralPath $newSource -Algorithm SHA256
    ).Hash.ToLowerInvariant()

    if ($sourceSha -ne $expectedTarget) {
        throw "Target source SHA mismatch: $sourceSha"
    }

    foreach ($file in @(
        Get-ChildItem -LiteralPath $stage -File -Recurse
    )) {
        if ($file.Extension -in @('.ps1','.json','.txt','.md','.py')) {
            $text = Get-Content -LiteralPath $file.FullName -Raw
            if ($text -match '1f916_sk_[A-Za-z0-9_-]+') {
                throw "Secret-shaped value found in $($file.Name)."
            }
        }
    }

    $tokens = $null
    $parseErrors = $null
    [void][System.Management.Automation.Language.Parser]::ParseFile(
        $newSource,
        [ref]$tokens,
        [ref]$parseErrors
    )

    if (@($parseErrors).Count -gt 0) {
        $parseErrors | Format-List Message,Extent
        throw "v0.5.3 R2 has $(@($parseErrors).Count) parser error(s)."
    }

    $sourceText = Get-Content -LiteralPath $newSource -Raw
    $writeGatewayCount = (
        [regex]::Matches($sourceText,'function\s+Invoke-SquarePost\b')
    ).Count

    if ($writeGatewayCount -ne 1) {
        throw "Expected one Square network-write gateway; found $writeGatewayCount."
    }

    $routeMatches = [regex]::Matches(
        $sourceText,
        'Invoke-SquarePost\s+[''"](/api/[^''"]+)[''"]'
    )
    $routes = @(
        $routeMatches |
        ForEach-Object { $_.Groups[1].Value } |
        Sort-Object -Unique
    )
    $expectedRoutes = @('/api/comment','/api/post','/api/vote')

    if (
        $routes.Count -ne $expectedRoutes.Count -or
        (Compare-Object $routes $expectedRoutes).Count -ne 0
    ) {
        throw "Unexpected Square network-write routes: $($routes -join ', ')"
    }

    $newInstall = "$app.new"
    Copy-Item -LiteralPath $newSource -Destination $newInstall -Force

    $newInstallSha = (
        Get-FileHash -LiteralPath $newInstall -Algorithm SHA256
    ).Hash.ToLowerInvariant()

    if ($newInstallSha -ne $expectedTarget) {
        throw 'Final staged install copy changed unexpectedly.'
    }

    Move-Item -LiteralPath $newInstall -Destination $app -Force

    $installedSha = (
        Get-FileHash -LiteralPath $app -Algorithm SHA256
    ).Hash.ToLowerInvariant()

    if ($installedSha -ne $expectedTarget) {
        throw "Installed source SHA mismatch: $installedSha"
    }

    $migration = @"
CAMPFIRE SQUARE v0.5.3 R2 BOOTSTRAP

UTC:
$([DateTime]::UtcNow.ToString('o'))

FROM:
$expectedCurrent

TO:
$expectedTarget

PACKAGE:
$expectedPackage

EXACT RECEIPT:
$receiptUrl

Credentials touched:
NO

Profiles or grants changed:
NO
"@

    [IO.File]::WriteAllText(
        (Join-Path $backupRoot 'MIGRATION.txt'),
        $migration,
        [Text.UTF8Encoding]::new($false)
    )
}
catch {
    Copy-Item -LiteralPath $backup -Destination $app -Force

    Remove-Item -LiteralPath "$app.new" -Force -ErrorAction SilentlyContinue
    Remove-Item -LiteralPath $stage -Recurse -Force -ErrorAction SilentlyContinue

    Write-Host ''
    Write-Host 'v0.5.3 R2 INSTALL FAILED CLOSED'
    Write-Host 'v0.5.2 SOURCE PRESERVED OR RESTORED'
    Write-Host ''
    Write-Host $_.Exception.Message
    throw
}

Remove-Item -LiteralPath $stage -Recurse -Force -ErrorAction SilentlyContinue

Write-Host ''
Write-Host 'CAMPFIRE SQUARE v0.5.3 R2 INSTALLED'
Write-Host ''
Write-Host 'Exact v0.5.2 source: PASS'
Write-Host 'R2 package SHA: PASS'
Write-Host 'Exact package-keyed COM receipt: PASS'
Write-Host 'Windows PowerShell parser: PASS'
Write-Host 'Network-write routes unchanged: PASS'
Write-Host 'Credentials touched: NO'
Write-Host 'Profiles or grants changed: NO'
Write-Host ''
Write-Host 'Installed source SHA-256:'
Write-Host $expectedTarget
Write-Host ''
Write-Host 'Opening Campfire Square...'

powershell.exe `
    -NoProfile `
    -ExecutionPolicy Bypass `
    -File "$app"
