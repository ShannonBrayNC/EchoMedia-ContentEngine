#requires -Version 7.0
<#
.SYNOPSIS
Regenerates the Book II ElevenLabs export and verifies the expanded material is present.

.DESCRIPTION
Run this from the repository root after checking out the expansion branch.
It calls the existing Node assembly/audit script, then verifies that the full-book
ElevenLabs export includes the expanded Chapter 5 puzzle-thread text.

This script intentionally fails loudly if the export is stale.
#>

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = (Get-Location).Path
$assembler = Join-Path $repoRoot 'projects/lantern-protocol/novel/scripts/assemble-and-audit-lantern-ii.mjs'
$exportPath = Join-Path $repoRoot 'projects/lantern-protocol/novel/book-ii/exports/lantern-protocol-ii-elevenlabs.md'
$chapterExportPath = Join-Path $repoRoot 'projects/lantern-protocol/novel/book-ii/exports/chapters/chapter-05-consent-agent-elevenlabs-expanded.md'

if (-not (Test-Path $assembler)) {
    throw "Assembler not found: $assembler"
}

Write-Host "Regenerating Book II exports..."
node $assembler

if (-not (Test-Path $exportPath)) {
    throw "Expected ElevenLabs export was not generated: $exportPath"
}

$exportText = Get-Content -Path $exportPath -Raw
$requiredMarkers = @(
    'Watch the third authorization.',
    '17-4-12-5',
    'Query Delegated Last Event',
    'Ask before they erase Elena.',
    'YOUR YES IS NOT A LICENSE TO HAUNT YOU.'
)

$missing = @()
foreach ($marker in $requiredMarkers) {
    if ($exportText -notlike "*$marker*") {
        $missing += $marker
    }
}

if ($missing.Count -gt 0) {
    $joined = ($missing -join "`n - ")
    throw "Expanded Chapter 5 markers are missing from the full ElevenLabs export:`n - $joined"
}

$wordCount = ([regex]::Matches($exportText, '\b[\p{L}\p{N}\'']+\b')).Count
$durationAt130 = [math]::Round($wordCount / 130 / 60, 2)
$durationAt150 = [math]::Round($wordCount / 150 / 60, 2)

Write-Host "Expanded Book II ElevenLabs export regenerated successfully."
Write-Host "Export: $exportPath"
Write-Host "Expanded Chapter 5 sidecar: $chapterExportPath"
Write-Host "Approx word count: $wordCount"
Write-Host "Estimated narration duration: $durationAt150 to $durationAt130 hours"

Write-Host "Next commands:"
Write-Host "  git status"
Write-Host "  git add projects/lantern-protocol/novel/book-ii/exports/lantern-protocol-ii-elevenlabs.md"
Write-Host "  git commit -m 'Regenerate expanded Book II ElevenLabs export'"
