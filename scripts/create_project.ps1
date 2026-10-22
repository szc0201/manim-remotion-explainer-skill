param(
  [Parameter(Mandatory = $true)]
  [string]$Destination,

  [string]$ManimExe = $(if ($env:MANIM_EXE) { $env:MANIM_EXE } else { "D:\Manim\manim.cmd" }),

  [switch]$Install,
  [switch]$GenerateAssets
)

$ErrorActionPreference = "Stop"
$skillRoot = Split-Path -Parent $PSScriptRoot
$template = Join-Path $skillRoot "assets\project-template"

if (-not (Test-Path -LiteralPath $template)) {
  throw "Project template not found: $template"
}

if (Test-Path -LiteralPath $Destination) {
  if (Get-ChildItem -LiteralPath $Destination -Force -ErrorAction SilentlyContinue) {
    throw "Destination is not empty: $Destination"
  }
}
else {
  New-Item -ItemType Directory -Path $Destination | Out-Null
}

Get-ChildItem -LiteralPath $template -Force | Copy-Item -Destination $Destination -Recurse -Force

if ($Install -or $GenerateAssets) {
  Push-Location $Destination
  try {
    npm install --no-audit --no-fund
    if ($GenerateAssets) {
      npm run audio
      $env:MANIM_EXE = $ManimExe
      npm run manim
    }
  }
  finally {
    Pop-Location
  }
}

Write-Host "Project created: $Destination"
Write-Host "Preview: cd `"$Destination`"; npm run dev"
Write-Host "Render:  cd `"$Destination`"; npm run render"
