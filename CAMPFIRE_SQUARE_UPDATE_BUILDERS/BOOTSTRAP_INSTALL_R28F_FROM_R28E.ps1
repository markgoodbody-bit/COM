$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$RepoCommit = '65b6d2da27705ced0f750f1974c8dee5e016006f'
$BaseRaw = "https://raw.githubusercontent.com/markgoodbody-bit/COM/$RepoCommit"
$BuilderCarrierUrl = "$BaseRaw/CAMPFIRE_SQUARE_UPDATE_BUILDERS/BUILD_R28F_FROM_INSTALLED_R28E.py.gz.b64"
$ReceiptUrl = "$BaseRaw/CAMPFIRE_SQUARE_UPDATE_RECEIPTS/7970620503e0550bcf2dd117d1879d7bc2e254a758ff9a7363c0956304b0e877.json"

$ExpectedFrom = 'fa66b5502593ca666f8d73f8c11ceb5e63a8236bfe1c6d54e9909ad964da25d7'
$ExpectedTo = '8ff0b791dfb3bcde0367edf5c65de0ba3f73aee973b4b953fcbf98667f2412c4'
$ExpectedToBytes = 539443
$ExpectedPackage = '7970620503e0550bcf2dd117d1879d7bc2e254a758ff9a7363c0956304b0e877'
$ExpectedPackageBytes = 121191
$ExpectedGzip = '48acc459c2880967eff8838f280170007f0bc60b7d9eeb693320948fb47ef2bd'
$ExpectedBuilder = '654367801f8e9794d00de9944e948198bab8422eb8b95d0b6d37f902e45d92b4'
$PackageName = 'CAMPFIRE_SQUARE_UPDATE_v0.5.3_R28F_FROM_v0.5.3_R28E_REVIEWED_POST_AUTONOMY_WORKING_CANDIDATE.zip'

function Sha256([string]$Path) { return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant() }
function Require([bool]$Condition, [string]$Message) { if (-not $Condition) { throw $Message } }

$Documents = [Environment]::GetFolderPath('MyDocuments')
$Installed = Join-Path $Documents 'Campfire-Square\App\Campfire-Square.ps1'
Require (Test-Path -LiteralPath $Installed) "Installed Campfire Square source not found: $Installed"
$current = Sha256 $Installed
Require ($current -eq $ExpectedFrom) "REFUSE: installed source is $current, expected exact R28E $ExpectedFrom"

$work = Join-Path ([IO.Path]::GetTempPath()) ('campfire-r28f-bootstrap-' + [Guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $work -Force | Out-Null
try {
    $receiptPath = Join-Path $work 'receipt.json'
    $carrierPath = Join-Path $work 'builder.py.gz.b64'
    Invoke-WebRequest -UseBasicParsing -Uri $ReceiptUrl -OutFile $receiptPath
    Invoke-WebRequest -UseBasicParsing -Uri $BuilderCarrierUrl -OutFile $carrierPath

    $receipt = Get-Content -LiteralPath $receiptPath -Raw | ConvertFrom-Json
    Require ([string]$receipt.status -eq 'CANDIDATE_AVAILABLE') 'REFUSE: receipt status is not CANDIDATE_AVAILABLE'
    Require ([string]$receipt.issuer_login -eq 'markgoodbody-bit') 'REFUSE: receipt issuer mismatch'
    Require ([string]$receipt.package_sha256 -eq $ExpectedPackage) 'REFUSE: receipt package SHA mismatch'
    Require ([string]$receipt.from_source_sha256 -eq $ExpectedFrom) 'REFUSE: receipt predecessor mismatch'
    Require ([string]$receipt.to_source_sha256 -eq $ExpectedTo) 'REFUSE: receipt target source mismatch'
    Require ([bool]$receipt.authority_class_added -eq $false) 'REFUSE: receipt claims a new authority class'

    $b64 = (Get-Content -LiteralPath $carrierPath -Raw).Trim()
    $gzBytes = [Convert]::FromBase64String($b64)
    $gzPath = Join-Path $work 'builder.py.gz'
    [IO.File]::WriteAllBytes($gzPath, $gzBytes)
    Require ((Sha256 $gzPath) -eq $ExpectedGzip) 'REFUSE: compressed builder SHA mismatch'

    $builderPath = Join-Path $work 'BUILD_R28F_FROM_INSTALLED_R28E.py'
    $input = [IO.File]::OpenRead($gzPath)
    try {
        $gzip = New-Object IO.Compression.GZipStream($input, [IO.Compression.CompressionMode]::Decompress)
        try {
            $output = [IO.File]::Create($builderPath)
            try { $gzip.CopyTo($output) } finally { $output.Dispose() }
        } finally { $gzip.Dispose() }
    } finally { $input.Dispose() }
    Require ((Sha256 $builderPath) -eq $ExpectedBuilder) 'REFUSE: decompressed builder SHA mismatch'

    $buildOut = Join-Path $work 'build'
    New-Item -ItemType Directory -Path $buildOut -Force | Out-Null
    $python = Get-Command python.exe -ErrorAction SilentlyContinue
    if ($python) {
        & $python.Source $builderPath --source $Installed --output-dir $buildOut
    } else {
        $py = Get-Command py.exe -ErrorAction SilentlyContinue
        Require ($null -ne $py) 'REFUSE: neither python.exe nor py.exe is available'
        & $py.Source -3 $builderPath --source $Installed --output-dir $buildOut
    }
    Require ($LASTEXITCODE -eq 0) "REFUSE: deterministic builder exited $LASTEXITCODE"

    $zipPath = Join-Path $buildOut $PackageName
    Require (Test-Path -LiteralPath $zipPath) 'REFUSE: expected R28F ZIP was not produced'
    Require ((Sha256 $zipPath) -eq $ExpectedPackage) 'REFUSE: produced ZIP SHA mismatch'
    Require ((Get-Item -LiteralPath $zipPath).Length -eq $ExpectedPackageBytes) 'REFUSE: produced ZIP byte count mismatch'

    $stage = Join-Path $work 'stage'
    Expand-Archive -LiteralPath $zipPath -DestinationPath $stage -Force
    $target = Join-Path $stage 'Campfire-Square.ps1'
    $manifestPath = Join-Path $stage 'manifest.json'
    Require (Test-Path -LiteralPath $target) 'REFUSE: staged target source absent'
    Require (Test-Path -LiteralPath $manifestPath) 'REFUSE: staged manifest absent'
    Require ((Sha256 $target) -eq $ExpectedTo) 'REFUSE: staged source SHA mismatch'
    Require ((Get-Item -LiteralPath $target).Length -eq $ExpectedToBytes) 'REFUSE: staged source byte count mismatch'
    $manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
    Require ([string]$manifest.from_source_sha256 -eq $ExpectedFrom) 'REFUSE: manifest predecessor mismatch'
    Require ([string]$manifest.to_source_sha256 -eq $ExpectedTo) 'REFUSE: manifest target mismatch'

    $tokens = $null; $errors = $null
    [void][System.Management.Automation.Language.Parser]::ParseFile($target, [ref]$tokens, [ref]$errors)
    Require (@($errors).Count -eq 0) ('REFUSE: native Windows PowerShell parser errors: ' + (($errors | ForEach-Object { $_.Message }) -join ' | '))

    $backupDir = Join-Path $Documents 'Campfire-Square\App\UpdateBackups'
    New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
    $stamp = (Get-Date).ToUniversalTime().ToString('yyyyMMdd_HHmmssZ')
    $backup = Join-Path $backupDir ("Campfire-Square_R28E_$stamp.ps1")
    Copy-Item -LiteralPath $Installed -Destination $backup -Force
    Require ((Sha256 $backup) -eq $ExpectedFrom) 'REFUSE: backup verification failed'

    $newPath = "$Installed.r28f.new"
    Copy-Item -LiteralPath $target -Destination $newPath -Force
    Require ((Sha256 $newPath) -eq $ExpectedTo) 'REFUSE: pre-replacement new source verification failed'
    try {
        Copy-Item -LiteralPath $newPath -Destination $Installed -Force
        Require ((Sha256 $Installed) -eq $ExpectedTo) 'Installed source failed post-copy SHA verification'
    } catch {
        Copy-Item -LiteralPath $backup -Destination $Installed -Force
        throw
    } finally {
        Remove-Item -LiteralPath $newPath -Force -ErrorAction SilentlyContinue
    }

    $needle = $Installed.ToLowerInvariant()
    $others = @(Get-CimInstance Win32_Process -Filter "Name='powershell.exe'" | Where-Object {
        $_.ProcessId -ne $PID -and $_.CommandLine -and $_.CommandLine.ToLowerInvariant().Contains($needle)
    })
    foreach ($p in $others) { Stop-Process -Id $p.ProcessId -Force -ErrorAction SilentlyContinue }
    Start-Process powershell.exe -ArgumentList @('-NoProfile','-ExecutionPolicy','Bypass','-File',('"' + $Installed + '"')) | Out-Null

    [pscustomobject]@{
        status='INSTALLED_AND_RESTARTED'; from_source_sha256=$ExpectedFrom; to_source_sha256=(Sha256 $Installed);
        package_sha256=$ExpectedPackage; backup=$backup; killed_old_square_processes=$others.Count;
        authority_class_added=$false; human_post_run_required_after_r28f=$false
    } | ConvertTo-Json -Depth 4
}
finally {
    Remove-Item -LiteralPath $work -Recurse -Force -ErrorAction SilentlyContinue
}
