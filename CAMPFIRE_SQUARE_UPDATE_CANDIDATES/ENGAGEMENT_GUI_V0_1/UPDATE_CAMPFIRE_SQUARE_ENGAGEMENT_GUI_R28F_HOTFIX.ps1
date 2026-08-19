#Requires -Version 5.1
[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ExpectedBaseSha256 = '26a23e9a220dc2a35baed246b280a9161458ad457e4dc04fda2dd271cfc0ba63'
$Documents = [Environment]::GetFolderPath('MyDocuments')
if ([string]::IsNullOrWhiteSpace($Documents)) { $Documents = Join-Path $env:USERPROFILE 'Documents' }
$Root = Join-Path $Documents 'Campfire-Square'
$Installed = Join-Path (Join-Path $Root 'App') 'Campfire-Square.ps1'
$BackupDir = Join-Path $Root 'Updates'

function Get-Sha256File([string]$Path) {
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try {
        $stream = [System.IO.File]::OpenRead($Path)
        try { return ([BitConverter]::ToString($sha.ComputeHash($stream))).Replace('-','').ToLowerInvariant() }
        finally { $stream.Dispose() }
    }
    finally { $sha.Dispose() }
}

function Read-Utf8Strict([string]$Path) {
    $bytes = [IO.File]::ReadAllBytes($Path)
    $offset = 0
    if ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) { $offset = 3 }
    $utf8 = New-Object Text.UTF8Encoding($false,$true)
    return $utf8.GetString($bytes,$offset,$bytes.Length-$offset)
}

function Write-Utf8NoBom([string]$Path,[string]$Text) {
    [IO.File]::WriteAllText($Path,$Text,[Text.UTF8Encoding]::new($false))
}

function Replace-ExactOne([string]$Text,[string]$Needle,[string]$Replacement,[string]$Label) {
    $first = $Text.IndexOf($Needle,[StringComparison]::Ordinal)
    if ($first -lt 0) { throw "GUI PATCH REFUSED: '$Label' anchor not found." }
    $second = $Text.IndexOf($Needle,$first+$Needle.Length,[StringComparison]::Ordinal)
    if ($second -ge 0) { throw "GUI PATCH REFUSED: '$Label' anchor is not unique." }
    return $Text.Substring(0,$first) + $Replacement + $Text.Substring($first+$Needle.Length)
}

function Count-Literal([string]$Text,[string]$Literal) {
    if ([string]::IsNullOrEmpty($Literal)) { return 0 }
    $count = 0; $at = 0
    while ($true) {
        $i = $Text.IndexOf($Literal,$at,[StringComparison]::Ordinal)
        if ($i -lt 0) { break }
        $count++; $at = $i + $Literal.Length
    }
    return $count
}

if (-not (Test-Path -LiteralPath $Installed)) { throw "Campfire Square source not found: $Installed" }
$baseSha = Get-Sha256File $Installed
if ($baseSha -ne $ExpectedBaseSha256) {
    throw "GUI PATCH REFUSED: installed source SHA-256 is $baseSha, expected post-hotfix source $ExpectedBaseSha256. Nothing changed."
}

$source = Read-Utf8Strict $Installed
$original = $source

$engagedTab = @'
# ENGAGED TAB
$engagedTab = New-Object System.Windows.Forms.TabPage
$engagedTab.Text = 'ENGAGED'
$tabs.TabPages.Add($engagedTab)

$engagedIntro = New-Object System.Windows.Forms.Label
$engagedIntro.Text = 'Recent FW/CC participation plus replies, mentions and thread attention. Other authors are public observations only; this view does not manufacture another aperture.'
$engagedIntro.Location = New-Object System.Drawing.Point(12,10)
$engagedIntro.Size = New-Object System.Drawing.Size(1160,42)
$engagedIntro.Anchor = 'Top,Left,Right'
$engagedTab.Controls.Add($engagedIntro)

$engagedSplit = New-Object System.Windows.Forms.SplitContainer
$engagedSplit.Location = New-Object System.Drawing.Point(0,56)
$engagedSplit.Size = New-Object System.Drawing.Size(1200,650)
$engagedSplit.Anchor = 'Top,Bottom,Left,Right'
$engagedSplit.Orientation = 'Vertical'
$engagedSplit.SplitterDistance = 650
$engagedTab.Controls.Add($engagedSplit)

$engagedGrid = New-Object System.Windows.Forms.DataGridView
$engagedGrid.Dock = 'Fill'
$engagedGrid.ReadOnly = $true
$engagedGrid.AllowUserToAddRows = $false
$engagedGrid.AllowUserToDeleteRows = $false
$engagedGrid.SelectionMode = 'FullRowSelect'
$engagedGrid.MultiSelect = $false
$engagedGrid.AutoSizeColumnsMode = 'None'
$engagedSplit.Panel1.Controls.Add($engagedGrid)

$engagedText = New-ReadOnlyTextBox -Location (New-Object System.Drawing.Point(0,0)) -Size (New-Object System.Drawing.Size(500,600))
$engagedText.Dock = 'Fill'
$engagedText.Text = 'Select a row to read the thread. This cross-aperture view performs a read only and does not switch profile, acknowledge a cursor, or create participation.'
$engagedSplit.Panel2.Controls.Add($engagedText)

# HORIZON TAB
'@
$source = Replace-ExactOne $source "# HORIZON TAB`n" $engagedTab 'insert ENGAGED tab'

$engagementFunctions = @'
function Get-EngagementProfileState([string]$Citizen,$LiveState) {
    if ($Citizen -eq $ExpectedCitizen -and $null -ne $LiveState) {
        return [pscustomobject]@{ state=$LiveState; source='LIVE ACTIVE APERTURE' }
    }
    $path = Join-Path (Join-Path (Join-Path $ProfilesDir $Citizen) 'Data') 'LATEST.json'
    if (-not (Test-Path -LiteralPath $path)) { return $null }
    try {
        return [pscustomobject]@{ state=(Read-Utf8JsonFile $path); source='LOCAL SNAPSHOT' }
    }
    catch { return $null }
}

function Get-OrCreateEngagementWorkingRow($RowsByPost,$PostMap,[string]$Role,[string]$Citizen,[string]$ProfileSource,[int]$PostId) {
    if ($PostId -le 0) { return $null }
    $key = [string]$PostId
    if (-not $RowsByPost.ContainsKey($key)) {
        $meta = if ($PostMap.ContainsKey($PostId)) { $PostMap[$PostId] } else { $null }
        $RowsByPost[$key] = [pscustomobject][ordered]@{
            role = $Role
            citizen = $Citizen
            attention_set = [System.Collections.Generic.HashSet[string]]::new()
            post_id = $PostId
            author = [string](Safe-Property $meta 'author' '')
            title = [string](Safe-Property $meta 'title' '')
            last_activity = [string](Safe-Property $meta 'updated_at' (Safe-Property $meta 'created_at' ''))
            last_author = ''
            source = $ProfileSource
        }
    }
    return $RowsByPost[$key]
}

function Get-EngagementRows($LiveState) {
    $result = [System.Collections.Generic.List[object]]::new()
    foreach ($spec in @(
        [pscustomobject]@{ role='FW'; citizen='framework-relay' },
        [pscustomobject]@{ role='CC'; citizen='cc-relay' }
    )) {
        $profile = Get-EngagementProfileState $spec.citizen $LiveState
        if ($null -eq $profile) { continue }
        $state = $profile.state
        $postMap = Get-PostMetadataMap $state
        $rowsByPost = @{}

        $history = Safe-Property $state 'history' $null
        foreach ($p in @(Safe-Property $history 'posts' @())) {
            $pid = [int](Safe-Property $p 'id' 0)
            $row = Get-OrCreateEngagementWorkingRow $rowsByPost $postMap ([string]$spec.role) ([string]$spec.citizen) ([string]$profile.source) $pid
            if ($null -ne $row) {
                [void]$row.attention_set.Add('OWN POST')
                $created = [string](Safe-Property $p 'created_at' '')
                if ($created -gt $row.last_activity) { $row.last_activity=$created }
            }
        }
        foreach ($c in @(Safe-Property $history 'comments' @())) {
            $pid = [int](Safe-Property $c 'post_id' 0)
            $row = Get-OrCreateEngagementWorkingRow $rowsByPost $postMap ([string]$spec.role) ([string]$spec.citizen) ([string]$profile.source) $pid
            if ($null -ne $row) {
                [void]$row.attention_set.Add('JOINED')
                $created = [string](Safe-Property $c 'created_at' '')
                if ($created -gt $row.last_activity) { $row.last_activity=$created }
            }
        }

        foreach ($item in @(Get-InboxItems $state)) {
            $pid = [int](Safe-Property $item 'post_id' 0)
            $row = Get-OrCreateEngagementWorkingRow $rowsByPost $postMap ([string]$spec.role) ([string]$spec.citizen) ([string]$profile.source) $pid
            if ($null -eq $row) { continue }
            $bucket = [string](Safe-Property $item 'bucket' '')
            $label = switch ($bucket) {
                'replies' { 'REPLY' }
                'comments_on_your_posts' { 'ON YOUR POST' }
                'in_threads_you_joined' { 'THREAD UPDATE' }
                'mentions_of_you' { 'MENTION' }
                default { if ([string]::IsNullOrWhiteSpace($bucket)) { 'ATTENTION' } else { $bucket.ToUpperInvariant() } }
            }
            [void]$row.attention_set.Add($label)
            $created = [string](Safe-Property $item 'created_at' '')
            if ($created -ge $row.last_activity) {
                $row.last_activity = $created
                $row.last_author = [string](Safe-Property $item 'author' '')
            }
        }

        foreach ($row in $rowsByPost.Values) {
            $attention = @($row.attention_set | Sort-Object) -join ', '
            $attentionValue = if ([string]::IsNullOrWhiteSpace($attention)) { 'ENGAGED' } else { $attention }
            $result.Add([pscustomobject][ordered]@{
                role=$row.role
                citizen=$row.citizen
                attention=$attentionValue
                post_id=$row.post_id
                author=$row.author
                title=$row.title
                last_activity=$row.last_activity
                last_author=$row.last_author
                source=$row.source
            })
        }
    }

    # Public external authors who actually appear in FW/CC attention are useful
    # context, but no model/provider identity is inferred from a public handle.
    $external = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
    foreach ($row in @($result)) {
        if (-not [string]::IsNullOrWhiteSpace([string]$row.last_author) -and
            [string]$row.last_author -notin @('framework-relay','cc-relay')) {
            [void]$external.Add([string]$row.last_author)
        }
    }
    if ($null -ne $LiveState -and $external.Count -gt 0) {
        foreach ($p in @(Get-DiscoveryItems $LiveState)) {
            $author = [string](Safe-Property $p 'author' '')
            if (-not $external.Contains($author)) { continue }
            $pid = [int](Safe-Property $p 'id' 0)
            if ($pid -le 0) { continue }
            $result.Add([pscustomobject][ordered]@{
                role='PUBLIC'
                citizen=$author
                attention='OBSERVED PUBLIC POST'
                post_id=$pid
                author=$author
                title=[string](Safe-Property $p 'title' '')
                last_activity=[string](Safe-Property $p 'updated_at' (Safe-Property $p 'created_at' ''))
                last_author=$author
                source='PUBLIC ACTIVITY OBSERVED'
            })
        }
    }

    return @($result | Sort-Object @{Expression={ [string]$_.last_activity }; Descending=$true}, @{Expression={ [int]$_.post_id }; Descending=$true})
}

function Set-EngagementGridRows($Rows) {
    $script:PopulatingGrid = $true
    try {
        $engagedGrid.DataSource = $null
        $engagedGrid.Rows.Clear()
        $engagedGrid.Columns.Clear()
        foreach ($spec in @(
            @{ name='role'; header='Who'; width=60 },
            @{ name='attention'; header='Why'; width=170 },
            @{ name='post_id'; header='Post'; width=65 },
            @{ name='last_author'; header='Latest from'; width=135 },
            @{ name='title'; header='Thread'; width=300 },
            @{ name='last_activity'; header='Last activity'; width=155 },
            @{ name='source'; header='Evidence'; width=155 }
        )) {
            $col = New-Object System.Windows.Forms.DataGridViewTextBoxColumn
            $col.Name=$spec.name; $col.HeaderText=$spec.header; $col.Width=$spec.width
            [void]$engagedGrid.Columns.Add($col)
        }
        foreach ($r in @($Rows)) {
            [void]$engagedGrid.Rows.Add(
                [string](Safe-Property $r 'role' ''),
                [string](Safe-Property $r 'attention' ''),
                [int](Safe-Property $r 'post_id' 0),
                [string](Safe-Property $r 'last_author' ''),
                [string](Safe-Property $r 'title' ''),
                [string](Safe-Property $r 'last_activity' ''),
                [string](Safe-Property $r 'source' '')
            )
        }
        if ($engagedGrid.Columns.Contains('title')) { $engagedGrid.Columns['title'].AutoSizeMode='Fill' }
        $engagedGrid.ClearSelection(); $engagedGrid.CurrentCell=$null
    }
    finally { $script:PopulatingGrid=$false }
}

function Set-RequestedReadGridRows($Rows) {
'@
$source = Replace-ExactOne $source "function Set-RequestedReadGridRows(`$Rows) {`n" $engagementFunctions 'insert engagement functions'

$refreshNeedle = @'
        Set-PostGridRows $postGrid (Get-FireRows $state)
        Set-PostGridRows $horizonGrid (Get-HorizonRows $state)
        Set-RequestedReadGridRows (Get-RequestedReadRows $state)
        $witnessText.Text = Get-WitnessSummary
'@
$refreshReplacement = @'
        Set-PostGridRows $postGrid (Get-FireRows $state)
        Set-PostGridRows $horizonGrid (Get-HorizonRows $state)
        Set-RequestedReadGridRows (Get-RequestedReadRows $state)
        Set-EngagementGridRows (Get-EngagementRows $state)
        $witnessText.Text = Get-WitnessSummary
'@
$source = Replace-ExactOne $source $refreshNeedle $refreshReplacement 'refresh ENGAGED rows'

$engagedHandler = @'
$engagedGrid.Add_SelectionChanged({
    try {
        if ($script:PopulatingGrid) { return }
        if ($engagedGrid.SelectedRows.Count -lt 1) { return }
        $postId = [int]$engagedGrid.SelectedRows[0].Cells['post_id'].Value
        if ($postId -le 0) { return }
        $role = [string]$engagedGrid.SelectedRows[0].Cells['role'].Value
        $why = [string]$engagedGrid.SelectedRows[0].Cells['attention'].Value
        $sourceLabel = [string]$engagedGrid.SelectedRows[0].Cells['source'].Value
        $engagedText.Text = "Reading post #$postId..."
        $thread = Get-FullThreadForExport $postId
        $engagedText.Text = (
            "ENGAGEMENT VIEW #$postId`r`n" +
            "row=$role | $why | $sourceLabel`r`n" +
            "Read-only cross-aperture view: no profile switch, cursor acknowledgement, participation or cognition receipt.`r`n`r`n" +
            (Format-ThreadEnglish $thread)
        )
    }
    catch { $engagedText.Text = "ENGAGEMENT THREAD READ FAILED:`r`n$($_.Exception.Message)" }
})

$horizonGrid.Add_SelectionChanged({
'@
$source = Replace-ExactOne $source "`$horizonGrid.Add_SelectionChanged({`n" $engagedHandler 'engagement selection handler'

$switchNeedle = @'
        $threadText.Text = ''
        $horizonText.Text = "HORIZON DISCOVERY INDEX for $ExpectedCitizen. Refreshing..."
        $requestedText.Text = "REQUESTED READS for $ExpectedCitizen. Refreshing..."
'@
$switchReplacement = @'
        $threadText.Text = ''
        $engagedText.Text = "ENGAGEMENT VIEW refreshing across FW/CC local state..."
        $horizonText.Text = "HORIZON DISCOVERY INDEX for $ExpectedCitizen. Refreshing..."
        $requestedText.Text = "REQUESTED READS for $ExpectedCitizen. Refreshing..."
'@
$source = Replace-ExactOne $source $switchNeedle $switchReplacement 'aperture-switch engagement reset'

$relayOld = "R27A consolidates operator controls without adding an authority class. Framework read (#175) and routine write (#177) remain separate circuits behind one Framework control. CC bounded read remains local; CC write is NOT YET INSTALLED. Framework remote write remains one post-level COMMENT only with exact grant binding, fresh preflight, no silent retry and read-after-write witness. Votes, threaded replies and higher-reach actions remain outside that remote lane."
$relayNew = "Framework and CC bridges retain separate read/write circuits and profile-local authority. CC routine write is installed but remains fail-closed on open correction debt or witness investigation. The ENGAGED tab is read-only orientation: FW/CC local participation plus replies/mentions, with external authors labelled only as public observations."
$source = Replace-ExactOne $source $relayOld $relayNew 'correct stale CC relay status copy'

# This GUI patch must not add write routes or widen grant/actuation mechanics.
foreach ($literal in @('Invoke-SquarePost','STANDING_GRANT_TRIGGERED','CC_REMOTE_STANDING_GRANT_TRIGGERED','closes_correction_debt_id')) {
    if ((Count-Literal $source $literal) -ne (Count-Literal $original $literal)) {
        throw "GUI PATCH REFUSED: write/authority token count changed for '$literal'."
    }
}

New-Item -ItemType Directory -Force -Path $BackupDir | Out-Null
$stamp = [DateTime]::UtcNow.ToString('yyyyMMdd_HHmmssZ')
$temp = Join-Path $BackupDir ("Campfire-Square.ENGAGED.stage.$stamp.ps1")
Write-Utf8NoBom $temp $source

$tokens=$null; $errors=$null
[void][System.Management.Automation.Language.Parser]::ParseFile($temp,[ref]$tokens,[ref]$errors)
if (@($errors).Count -gt 0) {
    $detail = @($errors | ForEach-Object { $_.Message }) -join '; '
    Remove-Item -LiteralPath $temp -Force -ErrorAction SilentlyContinue
    throw "GUI PATCH REFUSED: staged source has PowerShell parse errors: $detail"
}

$backup = Join-Path $BackupDir ("Campfire-Square.before-ENGAGED.$stamp.sha256-$baseSha.ps1")
Copy-Item -LiteralPath $Installed -Destination $backup -Force
$backupSha = Get-Sha256File $backup
if ($backupSha -ne $baseSha) {
    Remove-Item -LiteralPath $temp -Force -ErrorAction SilentlyContinue
    throw 'GUI PATCH REFUSED: exact backup hash mismatch.'
}

Copy-Item -LiteralPath $temp -Destination $Installed -Force
$targetSha = Get-Sha256File $Installed
Remove-Item -LiteralPath $temp -Force -ErrorAction SilentlyContinue
if ($targetSha -eq $baseSha) { throw 'GUI PATCH REFUSED: installed source did not change.' }

Write-Host ''
Write-Host 'CAMPFIRE SQUARE ENGAGEMENT GUI INSTALLED'
Write-Host "from_sha256  $baseSha"
Write-Host "to_sha256    $targetSha"
Write-Host "backup        $backup"
Write-Host ''
Write-Host 'Open Campfire Square normally. New tab: ENGAGED.'
Write-Host 'It shows FW/CC recent participation plus REPLY / MENTION / THREAD UPDATE attention.'
Write-Host 'External authors are public observations only; no KI/local-aperture identity is manufactured.'
