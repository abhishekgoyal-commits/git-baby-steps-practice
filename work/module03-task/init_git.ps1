# Helper script to initialize git repo locally
# Run this from PowerShell in the project folder.

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Error "git is not installed or not on PATH. Install Git and retry."
    exit 1
}

git init
git add .
git commit -m "Initial commit: add calculator project"
Write-Output "Repository initialized and initial commit created."
