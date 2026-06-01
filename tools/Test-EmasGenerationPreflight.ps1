#requires -Version 7.0
<#
.SYNOPSIS
Runs EMAS generation preflight checks before provider calls.

.EXAMPLE
pwsh ./tools/Test-EmasGenerationPreflight.ps1 -ProjectName Vanessa -AdName Vanessa-Christina-Outfit-Update-Ad -IntendedUse social_media -Platform instagram -Prompt "Create the Christina outfit update scene"
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$ProjectName,

    [string]$SubjectId,

    [string]$AdName,

    [Parameter(Mandatory = $true)]
    [string]$IntendedUse,

    [string]$Platform,

    [string]$Actor = "local-cli",

    [Parameter(Mandatory = $true)]
    [string]$Prompt,

    [string[]]$Reference = @(),

    [int]$OutputCount = 1,

    [string]$RootPath = "."
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$argsList = @(
    "scripts/emas_generation_preflight.py",
    "--project-name", $ProjectName,
    "--intended-use", $IntendedUse,
    "--actor", $Actor,
    "--prompt", $Prompt,
    "--output-count", $OutputCount,
    "--root-path", $RootPath
)

if ($SubjectId) { $argsList += @("--subject-id", $SubjectId) }
if ($AdName) { $argsList += @("--ad-name", $AdName) }
if ($Platform) { $argsList += @("--platform", $Platform) }
foreach ($item in $Reference) { $argsList += @("--reference", $item) }

python @argsList
