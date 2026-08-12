$ErrorActionPreference = 'Stop'

$expectedCurrent =
    '352a8ae35df20bea4df8d6667391219d069868ca52bd7cb25d5ec378b62bd537'

$expectedPackage =
    '57e66b999e5d98cc2edbb248c37e0fa436ffa605bd39fd839fb09c53b05c075f'

$expectedTarget =
    '45911968814398e9505ff51d69d25b2d4a8981d6f777706cb93944d9b9313456'

$expectedFilename =
    'CAMPFIRE_SQUARE_UPDATE_v0.5.3_FROM_v0.5.2_REQUESTED_READING_WORKING_CANDIDATE_R4.zip'

$receiptUrl =
    'https://raw.githubusercontent.com/markgoodbody-bit/COM/c0a3ca41a0b3764c79a05e47a3b77de1b4b01646/CAMPFIRE_SQUARE_UPDATE_RECEIPTS/57e66b999e5d98cc2edbb248c37e0fa436ffa605bd39fd839fb09c53b05c075f.json'

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

$runningByTitle = @(
    Get-Process powershell,pwsh -ErrorAction SilentlyContinue |
    Where-Object { $_.MainWindowTitle -like '*Campfire Square*' }
)

$runningByCommandLine = @()
try {
    $runningByCommandLine = @(
        Get-CimInstance `
            -ClassName Win32_Process `
            -Filter "Name='powershell.exe' OR Name='pwsh.exe'" |
        Where-Object {
            [int]$_.ProcessId -ne $PID -and
            [string]$_.CommandLine -match 'Campfire-Square\.ps1'
        }
    )
}
catch {
    throw "Could not prove Campfire Square is closed from the process command lines. Nothing changed. $($_.Exception.Message)"
}

if ($runningByTitle.Count -gt 0 -or $runningByCommandLine.Count -gt 0) {
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
        -Filter 'CAMPFIRE_SQUARE_UPDATE_v0.5.3_FROM_v0.5.2_REQUESTED_READING_WORKING_CANDIDATE_R4*.zip' `
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
R4 PACKAGE NOT FOUND OR HASH DOES NOT MATCH.

Expected filename:
$expectedFilename

Expected SHA-256:
$expectedPackage

Download R4 into Downloads and run this block again.
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
    $request.UserAgent = 'Campfire-Square-v0.5.3-R4-bootstrap'
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
    [string]$receipt.carrier_type -ne 'COM_REPOSITORY_PACKAGE_KEYED_PATH' -or
    [string]$receipt.status -ne 'CANDIDATE_AVAILABLE' -or
    [string]$receipt.issuer_login -ne 'markgoodbody-bit' -or
    [int]$receipt.candidate_revision -ne 4 -or
    [string]$receipt.from_source_sha256 -ne $expectedCurrent -or
    [string]$receipt.to_source_sha256 -ne $expectedTarget -or
    [string]$receipt.package_sha256 -ne $expectedPackage -or
    [string]$receipt.package_filename -ne $expectedFilename -or
    [bool]$receipt.grant_surface_changed -ne $false -or
    [bool]$receipt.network_write_routes_changed -ne $false -or
    [bool]$receipt.package_authenticated -ne $false
) {
    throw 'Pinned COM publication receipt does not describe this R4 transition. Nothing changed.'
}

Write-Host ''
Write-Host 'COM PUBLICATION RECEIPT: PRESENT AND CONSISTENT'
Write-Host 'PACKAGE AUTHENTICATED BY RECEIPT: NO'
Write-Host $receiptUrl

$stage = Join-Path (
    [IO.Path]::GetTempPath()
) ('Campfire-Square-v053-R4-' + [guid]::NewGuid().ToString('n'))

New-Item -ItemType Directory -Force -Path $stage | Out-Null

$backupRoot = Join-Path $root (
    'Backups\v0.5.3-R4-bootstrap-' +
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
        [int]$manifest.candidate_revision -ne 4 -or
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
    $ast = [System.Management.Automation.Language.Parser]::ParseFile(
        $newSource,
        [ref]$tokens,
        [ref]$parseErrors
    )

    if (@($parseErrors).Count -gt 0) {
        $parseErrors | Format-List Message,Extent
        throw "v0.5.3 R4 has $(@($parseErrors).Count) parser error(s)."
    }

    $gatewayDefinitions = @(
        $ast.FindAll(
            {
                param($node)
                $node -is [System.Management.Automation.Language.FunctionDefinitionAst] -and
                $node.Name -eq 'Invoke-SquarePost'
            },
            $true
        )
    )

    $writeGatewayCount = $gatewayDefinitions.Count

    if ($writeGatewayCount -ne 1) {
        throw "Expected one Square network-write gateway; found $writeGatewayCount."
    }

    $commandAsts = @(
        $ast.FindAll(
            {
                param($node)
                $node -is [System.Management.Automation.Language.CommandAst]
            },
            $true
        )
    )

    $postCalls = @(
        $commandAsts |
        Where-Object { $_.GetCommandName() -eq 'Invoke-SquarePost' }
    )

    $routes = @(
        foreach ($call in $postCalls) {
            $elements = @($call.CommandElements)
            if (
                $elements.Count -lt 2 -or
                $elements[1] -isnot [System.Management.Automation.Language.StringConstantExpressionAst]
            ) {
                throw 'Invoke-SquarePost has a non-literal or missing route argument.'
            }
            [string]($elements[1].Value)
        }
    )

    $routes = @(
        $routes |
        Sort-Object -Unique
    )
    $expectedRoutes = @('/api/comment','/api/post','/api/vote')

    if (
        $routes.Count -ne $expectedRoutes.Count -or
        (Compare-Object $routes $expectedRoutes).Count -ne 0
    ) {
        throw "Unexpected Square network-write routes: $($routes -join ', ')"
    }

    $directPostCount = 0
    foreach ($call in $commandAsts) {
        $rawCommandName = [string]$call.GetCommandName()
        $commandName = switch ($rawCommandName.ToLowerInvariant()) {
            'irm'  { 'Invoke-RestMethod' }
            'iwr'  { 'Invoke-WebRequest' }
            'curl' { 'Invoke-WebRequest' }
            'wget' { 'Invoke-WebRequest' }
            default { $rawCommandName }
        }
        if ($commandName -notin @('Invoke-RestMethod','Invoke-WebRequest')) {
            continue
        }

        $elements = @($call.CommandElements)
        for ($index = 0; $index -lt $elements.Count; $index++) {
            $element = $elements[$index]
            if (
                $element -isnot [System.Management.Automation.Language.CommandParameterAst] -or
                $element.ParameterName -ine 'Method'
            ) {
                continue
            }

            if (
                $index + 1 -ge $elements.Count -or
                $elements[$index + 1] -isnot [System.Management.Automation.Language.StringConstantExpressionAst]
            ) {
                throw "$commandName uses a non-literal -Method value."
            }

            $method = [string]$elements[$index + 1].Value
            if ($method -ine 'Post') { continue }

            $owner = $call.Parent
            while (
                $null -ne $owner -and
                $owner -isnot [System.Management.Automation.Language.FunctionDefinitionAst]
            ) {
                $owner = $owner.Parent
            }

            if (
                $null -eq $owner -or
                [string]$owner.Name -ne 'Invoke-SquarePost'
            ) {
                throw "$commandName performs POST outside Invoke-SquarePost."
            }

            $directPostCount++
        }
    }

    if ($directPostCount -ne 1) {
        throw "Expected one AST-visible direct POST inside Invoke-SquarePost; found $directPostCount."
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
CAMPFIRE SQUARE v0.5.3 R4 BOOTSTRAP

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
    Write-Host 'v0.5.3 R4 INSTALL FAILED CLOSED'
    Write-Host 'v0.5.2 SOURCE PRESERVED OR RESTORED'
    Write-Host ''
    Write-Host $_.Exception.Message
    throw
}

Remove-Item -LiteralPath $stage -Recurse -Force -ErrorAction SilentlyContinue

Write-Host ''
Write-Host 'CAMPFIRE SQUARE v0.5.3 R4 INSTALLED'
Write-Host ''
Write-Host 'Exact v0.5.2 source: PASS'
Write-Host 'R4 package SHA: PASS'
Write-Host 'Pinned COM publication receipt: PRESENT AND CONSISTENT'
Write-Host 'Package authenticated by receipt: NO'
Write-Host 'Windows PowerShell parser: PASS'
Write-Host 'AST-visible Square write calls/routes unchanged: PASS'
Write-Host 'Credentials touched: NO'
Write-Host 'Profiles or grants changed: NO'
Write-Host 'Launch uses ExecutionPolicy Bypass: YES (no elevation)'
Write-Host ''
Write-Host 'Installed source SHA-256:'
Write-Host $expectedTarget
Write-Host ''
Write-Host 'Opening Campfire Square...'

powershell.exe `
    -NoProfile `
    -ExecutionPolicy Bypass `
    -File "$app"
