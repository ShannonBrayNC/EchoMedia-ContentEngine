<#
.SYNOPSIS
Audits Silver Bullet Book 1 and Book 2 manuscript chapter folders and compiles ElevenReader proof-listening text files.

.DESCRIPTION
Run this locally from the repository root with PowerShell 7+.
It checks the known Book 1 and Book 2 manuscript paths, reports missing chapter numbers, flags scaffold-only files, and emits ElevenReader-ready TXT files.

USAGE
pwsh .\projects\lantern-protocol\case-files\silver-bullet\tools\Invoke-SilverBulletAudioAudit.ps1 -RepoRoot C:\workspace\GitHub\EchoMedia-ContentEngine-pr112
#>

[CmdletBinding()]
param(
    [string]$RepoRoot = (Get-Location).Path,
    [int]$ExpectedBook1Start = 0,
    [int]$ExpectedBook1End = 40,
    [int]$ExpectedBook2Start = 1,
    [int]$ExpectedBook2End = 40
)

$ErrorActionPreference = 'Stop'

$SilverRoot = Join-Path $RepoRoot 'projects\lantern-protocol\case-files\silver-bullet'
$Book1Path = Join-Path $SilverRoot 'manuscript\chapters'
$Book2Path = Join-Path $SilverRoot 'book-ii\manuscript\chapters'
$OutRoot = Join-Path $SilverRoot 'compiled\elevenreader'
$ReportPath = Join-Path $OutRoot 'SilverBullet-AudioAudit.md'

New-Item -ItemType Directory -Force -Path $OutRoot | Out-Null

function Get-ChapterNumber {
    param([string]$Name)
    if ($Name -match 'chapter[-_ ]0*(\d+)') { return [int]$Matches[1] }
    return $null
}

function Get-ChapterFiles {
    param([string]$Path)
    if (!(Test-Path $Path)) { return @() }
    return Get-ChildItem -Path $Path -Filter '*.md' | Sort-Object Name
}

function Test-ScaffoldOnly {
    param([string]$File)
    $raw = Get-Content $File -Raw
    $plain = $raw -replace '(?s)```.*?```',' ' -replace '#+\s*','' -replace '\*\*',''
    $wordCount = ($plain -split '\s+' | Where-Object { $_.Trim().Length -gt 0 }).Count
    $hasCanonSources = $raw -match '##\s*Canon Sources'
    $hasNarrativeSignals = $raw -match '"|Jack|Maggie|Christina|Lantern|Silver Bullet|house|phone|door|said'
    return [pscustomobject]@{
        WordCount = $wordCount
        ScaffoldOnly = ($hasCanonSources -and $wordCount -lt 500 -and -not $hasNarrativeSignals)
    }
}

function Convert-ToNarrationText {
    param([string]$Raw)
    $text = $Raw
    $text = $text -replace '(?m)^##\s*Canon Sources\s*$[\s\S]*?(?=^#\s|\z)', ''
    $text = $text -replace '(?m)^##\s*(Sprint|QA|Audiobook|Production|Canon Sources).*$', ''
    $text = $text -replace '(?m)^- Parent epic:.*$', ''
    $text = $text -replace '```text', ''
    $text = $text -replace '```', ''
    $text = $text -replace '\*\*(.*?)\*\*', '$1'
    $text = $text -replace '(?m)^---\s*$', '[Scene Break]'
    $text = $text -replace '(?m)^#+\s*', ''
    $text = $text -replace "`r?`n{3,}", "`r`n`r`n"
    return $text.Trim()
}

function Audit-Book {
    param(
        [string]$BookName,
        [string]$Path,
        [int]$Start,
        [int]$End
    )

    $files = Get-ChapterFiles $Path
    $numbers = @{}
    $fileRows = @()

    foreach ($file in $files) {
        $n = Get-ChapterNumber $file.Name
        if ($null -ne $n) { $numbers[$n] = $file.Name }
        $scaffold = Test-ScaffoldOnly $file.FullName
        $fileRows += [pscustomobject]@{
            Number = $n
            File = $file.Name
            WordCount = $scaffold.WordCount
            ScaffoldOnly = $scaffold.ScaffoldOnly
        }
    }

    $missing = @()
    foreach ($i in $Start..$End) {
        if (-not $numbers.ContainsKey($i)) { $missing += $i }
    }

    return [pscustomobject]@{
        BookName = $BookName
        Path = $Path
        Exists = (Test-Path $Path)
        Files = $fileRows
        Missing = $missing
        ScaffoldOnly = @($fileRows | Where-Object { $_.ScaffoldOnly })
    }
}

function Compile-Book {
    param(
        [string]$Title,
        [string]$Path,
        [string]$OutputFile
    )

    $files = Get-ChapterFiles $Path
    $parts = New-Object System.Collections.Generic.List[string]
    $parts.Add($Title)
    $parts.Add('Proof-listening edition for ElevenReader')
    $parts.Add('')

    foreach ($file in $files) {
        $raw = Get-Content $file.FullName -Raw
        $clean = Convert-ToNarrationText $raw
        if ([string]::IsNullOrWhiteSpace($clean)) { continue }
        $parts.Add('')
        $parts.Add('========================================')
        $parts.Add('')
        $parts.Add($clean)
        $parts.Add('')
    }

    $parts -join "`r`n" | Set-Content -Path $OutputFile -Encoding UTF8
}

$book1 = Audit-Book -BookName 'Silver Bullet Book 1' -Path $Book1Path -Start $ExpectedBook1Start -End $ExpectedBook1End
$book2 = Audit-Book -BookName 'Silver Bullet Book 2' -Path $Book2Path -Start $ExpectedBook2Start -End $ExpectedBook2End

Compile-Book -Title 'Silver Bullet Book 1 - Proof Listening Edition' -Path $Book1Path -OutputFile (Join-Path $OutRoot 'SilverBullet-Book1-ElevenReader.txt')
Compile-Book -Title 'Silver Bullet Book 2 - The Null Pattern - Proof Listening Edition' -Path $Book2Path -OutputFile (Join-Path $OutRoot 'SilverBullet-Book2-ElevenReader.txt')

$combined = Join-Path $OutRoot 'SilverBullet-Books1-2-ElevenReader.txt'
Get-Content (Join-Path $OutRoot 'SilverBullet-Book1-ElevenReader.txt') -Raw | Set-Content $combined -Encoding UTF8
Add-Content $combined "`r`n`r`n========================================`r`n`r`n"
Get-Content (Join-Path $OutRoot 'SilverBullet-Book2-ElevenReader.txt') -Raw | Add-Content $combined -Encoding UTF8

$report = New-Object System.Collections.Generic.List[string]
$report.Add('# Silver Bullet Audio Audit')
$report.Add('')
$report.Add("Generated: $(Get-Date -Format s)")
$report.Add('')
foreach ($book in @($book1, $book2)) {
    $report.Add("## $($book.BookName)")
    $report.Add('')
    $report.Add("Path: `$($book.Path)`")
    $report.Add("Exists: $($book.Exists)")
    $report.Add("Chapter files found: $(@($book.Files).Count)")
    $report.Add("Missing expected chapter numbers: $(@($book.Missing) -join ', ')")
    $report.Add("Scaffold-only candidates: $(@($book.ScaffoldOnly).Count)")
    $report.Add('')
    $report.Add('| Chapter | File | Words | ScaffoldOnly |')
    $report.Add('|---:|---|---:|---|')
    foreach ($row in $book.Files | Sort-Object Number, File) {
        $report.Add("| $($row.Number) | $($row.File) | $($row.WordCount) | $($row.ScaffoldOnly) |")
    }
    $report.Add('')
}
$report.Add('## Outputs')
$report.Add('')
$report.Add('- `compiled\elevenreader\SilverBullet-Book1-ElevenReader.txt`')
$report.Add('- `compiled\elevenreader\SilverBullet-Book2-ElevenReader.txt`')
$report.Add('- `compiled\elevenreader\SilverBullet-Books1-2-ElevenReader.txt`')

$report -join "`r`n" | Set-Content -Path $ReportPath -Encoding UTF8

Write-Host "Audit complete: $ReportPath"
Write-Host "ElevenReader files written to: $OutRoot"
