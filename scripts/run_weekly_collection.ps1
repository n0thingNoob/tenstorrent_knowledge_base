$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$python = "C:\Users\97368\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
$script = Join-Path $PSScriptRoot "weekly_source_collect.py"

if (-not (Test-Path $python)) {
    throw "Bundled Python not found: $python"
}

& $python $script @args
