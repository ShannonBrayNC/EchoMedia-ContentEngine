#requires -Version 7.0
<#
.SYNOPSIS
Creates an EchoMedia Ad Studio project scaffold.

.EXAMPLE
pwsh ./tools/New-EmasAdProject.ps1 -ProjectName Vanessa -AdName Vanessa-Christina-Outfit-Update-Ad -Actor ShannonBrayNC
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$ProjectName,

    [Parameter(Mandatory = $true)]
    [string]$AdName,

    [string]$Actor = "local-cli",

    [string]$RootPath = ".",

    [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$argsList = @(
    "scripts/emas_create_ad_project.py",
    "--project-name", $ProjectName,
    "--ad-name", $AdName,
    "--actor", $Actor,
    "--root-path", $RootPath
)

if ($Force) {
    $argsList += "--force"
}

python @argsList
