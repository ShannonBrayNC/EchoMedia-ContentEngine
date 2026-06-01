#requires -Version 7.0
<#
.SYNOPSIS
Verifies an EchoMedia Ad Studio append-only audit log.

.EXAMPLE
pwsh ./tools/Test-EmasAudit.ps1 -LogPath ./projects/Vanessa/metadata/audit-log.jsonl
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$LogPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if (-not (Test-Path -LiteralPath $LogPath)) {
    throw "Audit log not found: $LogPath"
}

$lines = Get-Content -LiteralPath $LogPath | Where-Object { -not [string]::IsNullOrWhiteSpace($_) }
$previousHash = $null
$index = 0

foreach ($line in $lines) {
    $index++
    $event = $line | ConvertFrom-Json -AsHashtable

    if ($event.previousHash -ne $previousHash) {
        throw "Hash chain break at line $index. Expected previousHash '$previousHash' but found '$($event.previousHash)'."
    }

    if (-not $event.eventHash) {
        throw "Missing eventHash at line $index."
    }

    # Full canonical Python-equivalent verification should run through services.emas.audit.
    # This PowerShell tool performs fast structural checks and chain continuity checks.
    $previousHash = $event.eventHash
}

Write-Host "Audit log structural chain verified: $LogPath ($($lines.Count) events)"
