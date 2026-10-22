param(
  [string]$ManimExe = $(if ($env:MANIM_EXE) { $env:MANIM_EXE } else { "D:\Manim\manim.cmd" })
)

$ErrorActionPreference = "Stop"
node --version
npm --version
python --version
python -c "import PIL; print('Pillow', PIL.__version__)"

if (-not (Test-Path -LiteralPath $ManimExe)) {
  throw "Manim entrypoint not found: $ManimExe"
}
& $ManimExe --version

Write-Host "Environment checks completed."
