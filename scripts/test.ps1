# Runs every check of the website (Windows). Same as scripts/test.sh.
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
$env:PYTHONIOENCODING = "utf-8"
$python = if (Get-Command python -ErrorAction SilentlyContinue) { "python" } else { "py" }
& $python -I (Join-Path $root "scripts\check_site.py")
exit $LASTEXITCODE
