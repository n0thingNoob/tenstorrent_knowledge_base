$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot

function Write-Info {
    param([string]$Message)
    Write-Host "[backup] $Message"
}

$statusBefore = git status --short --untracked-files=all
if ($LASTEXITCODE -ne 0) {
    throw "git status failed"
}

if ($statusBefore) {
    Write-Info "Repository has changes. Staging tracked/untracked content."
} else {
    Write-Info "Repository is already clean. Checking remote sync."
}

git add -A
if ($LASTEXITCODE -ne 0) {
    throw "git add failed"
}

$cachedDiff = git diff --cached --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Info "No new changes to commit."
} elseif ($LASTEXITCODE -eq 1) {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz"
    $message = "Weekly vault backup: $timestamp"
    git commit -m $message
    if ($LASTEXITCODE -ne 0) {
        throw "git commit failed"
    }
    Write-Info "Created commit: $message"
} else {
    throw "git diff --cached failed"
}

git push origin main
if ($LASTEXITCODE -ne 0) {
    throw "git push failed"
}

Write-Info "Push to origin/main completed."
