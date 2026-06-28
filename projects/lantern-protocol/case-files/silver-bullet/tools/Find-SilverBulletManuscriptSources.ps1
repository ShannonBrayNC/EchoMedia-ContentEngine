<#
.SYNOPSIS
Finds likely Silver Bullet manuscript chapter sources across the local repo.

.DESCRIPTION
This script scans the repository for Markdown files that look like Silver Bullet chapters, ranks them by word count, and writes a source discovery report. Use it when the expected manuscript folder compiles as chapter headings only.

USAGE
pwsh .\projects\lantern-protocol\case-files\silver-bullet\tools\Find-SilverBulletManuscriptSources.ps1 -RepoRoot C:\workspace\GitHub\EchoMedia-ContentEngine
#>

[CmdletBinding()]
param(
    [string]$RepoRoot = (Get-Location).Path,
    [string]$OutputPath = ''
)

$ErrorActionPreference = 'Stop'

if ([string]::IsNullOrWhiteSpace($OutputPath)) {
    $OutputPath = Join-Path $RepoRoot 'projects\lantern-protocol\case-files\silver-bullet\compiled\elevenreader\SilverBullet-SourceDiscovery.md'
}

$OutDir = Split-Path $OutputPath -Parent
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

function Get-ChapterNumber {
    param([string]$Name)
    if ($Name -match 'chapter[-_ ]0*(\d+)') { return [int]$Matches[1] }
    return $null
}

function Get-WordCount {
    param([string]$Text)
    $plain = $Text -replace '(?s)```.*?```',' ' -replace '#+\s*','' -replace '\*\*',''
    return @($plain -split '\s+' | Where-Object { $_.Trim().Length -gt 0 }).Count
}

$files = Get-ChildItem -Path $RepoRoot -Recurse -File -Include '*.md','*.txt' -ErrorAction SilentlyContinue |
    Where-Object {
        $_.FullName -match 'silver-bullet|SilverBullet|silver bullet|Silver Bullet' -or
        $_.Name -match '^chapter[-_ ]0*\d+|silverbullet|silver-bullet'
    }

$rows = foreach ($file in $files) {
    $raw = Get-Content $file.FullName -Raw -ErrorAction SilentlyContinue
    if ([string]::IsNullOrWhiteSpace($raw)) { continue }

    $looksLikeChapter = ($file.Name -match '^chapter[-_ ]0*\d+') -or ($raw -match '(?m)^#\s*Chapter\s+\d+')
    $mentionsSilver = $raw -match 'Silver Bullet|Jack Mercer|Maggie|Christina|Lantern|Room 414|Black Lantern'

    if (-not ($looksLikeChapter -or $mentionsSilver)) { continue }

    $relative = $file.FullName.Substring($RepoRoot.Length).TrimStart('\','/')
    $chapter = Get-ChapterNumber $file.Name
    $wordCount = Get-WordCount $raw
    $hasCanonSources = $raw -match '##\s*Canon Sources'
    $hasDialogue = $raw -match '".+"'
    $bookGuess = if ($relative -match 'book-ii') { 'Book 2' } elseif ($relative -match 'book-i') { 'Book 1' } elseif ($relative -match 'manuscript\\chapters|manuscript/chapters') { 'Book 1 candidate' } else { 'Unknown' }

    [pscustomobject]@{
        BookGuess = $bookGuess
        Chapter = $chapter
        Words = $wordCount
        HasDialogue = $hasDialogue
        HasCanonSources = $hasCanonSources
        Path = $relative
    }
}

$rows = @($rows | Sort-Object @{Expression='BookGuess';Ascending=$true}, @{Expression='Chapter';Ascending=$true}, @{Expression='Words';Descending=$true})

$report = New-Object System.Collections.Generic.List[string]
$report.Add('# Silver Bullet Source Discovery')
$report.Add('')
$report.Add("Generated: $(Get-Date -Format s)")
$report.Add('')
$report.Add('## Summary')
$report.Add('')
$report.Add("Candidate files found: $($rows.Count)")
$report.Add('')
$report.Add('## Top candidates by word count')
$report.Add('')
$report.Add('| Words | Chapter | BookGuess | Dialogue | CanonSources | Path |')
$report.Add('|---:|---:|---|---|---|---|')
foreach ($row in ($rows | Sort-Object Words -Descending | Select-Object -First 80)) {
    $report.Add("| $($row.Words) | $($row.Chapter) | $($row.BookGuess) | $($row.HasDialogue) | $($row.HasCanonSources) | `$($row.Path)` |")
}

$report.Add('')
$report.Add('## Book 1 chapter candidates')
$report.Add('')
$report.Add('| Chapter | Words | Dialogue | CanonSources | Path |')
$report.Add('|---:|---:|---|---|---|')
foreach ($row in ($rows | Where-Object { $_.BookGuess -match 'Book 1' } | Sort-Object Chapter, @{Expression='Words';Descending=$true})) {
    $report.Add("| $($row.Chapter) | $($row.Words) | $($row.HasDialogue) | $($row.HasCanonSources) | `$($row.Path)` |")
}

$report.Add('')
$report.Add('## Book 2 chapter candidates')
$report.Add('')
$report.Add('| Chapter | Words | Dialogue | CanonSources | Path |')
$report.Add('|---:|---:|---|---|---|')
foreach ($row in ($rows | Where-Object { $_.BookGuess -eq 'Book 2' } | Sort-Object Chapter, @{Expression='Words';Descending=$true})) {
    $report.Add("| $($row.Chapter) | $($row.Words) | $($row.HasDialogue) | $($row.HasCanonSources) | `$($row.Path)` |")
}

$report -join "`r`n" | Set-Content -Path $OutputPath -Encoding UTF8

Write-Host "Source discovery complete: $OutputPath"
Write-Host "Open this report and look for high-word-count Book 1 candidates."
