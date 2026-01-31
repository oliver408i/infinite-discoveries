$ErrorActionPreference = "Stop"

# Build a standalone Windows GUI app with Nuitka.
# Usage: powershell -ExecutionPolicy Bypass -File .\build_nuitka.ps1

$RootDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $RootDir

python -m nuitka `
  --standalone `
  --enable-plugin=tk-inter `
  --enable-plugin=matplotlib `
  --include-package-data=infinite_discoveries `
  --include-data-file=ID_CE-banner.png=ID_CE-banner.png `
  --output-dir=dist\nuitka `
  infinite_discoveries\__main__.py
