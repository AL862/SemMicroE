param(
    [string]$SourcePath = 'H:\Gdisk\ASEM\Seminare la Microeconomie'
)
$ErrorActionPreference = 'Stop'
$RepoRoot = Split-Path -Parent $PSScriptRoot
$PlanPath = Join-Path $PSScriptRoot 'course-files.json'

function Assert-GitSuccess([string]$Operation) {
    if ($LASTEXITCODE -ne 0) { throw "Git failed: $Operation" }
}
function Get-BlobHash([string]$Path) {
    $stream = [System.IO.File]::OpenRead($Path)
    $sha = [System.Security.Cryptography.SHA1]::Create()
    try {
        $header = [System.Text.Encoding]::ASCII.GetBytes("blob $($stream.Length)" + [char]0)
        [void]$sha.TransformBlock($header, 0, $header.Length, $header, 0)
        $buffer = New-Object byte[] 1048576
        while (($count = $stream.Read($buffer, 0, $buffer.Length)) -gt 0) {
            [void]$sha.TransformBlock($buffer, 0, $count, $buffer, 0)
        }
        [void]$sha.TransformFinalBlock([byte[]]@(), 0, 0)
        return ([System.BitConverter]::ToString($sha.Hash)).Replace('-', '').ToLowerInvariant()
    } finally {
        $stream.Dispose()
        $sha.Dispose()
    }
}

Get-Command git -ErrorAction Stop | Out-Null
if (-not (Test-Path -LiteralPath (Join-Path $RepoRoot '.git'))) {
    throw 'Run this script from a Git clone of AL862/SemMicroE.'
}
$branch = & git -C $RepoRoot branch --show-current
Assert-GitSuccess 'read branch'
if ($branch -ne 'main') { throw 'Switch to main before importing.' }
& git -C $RepoRoot diff --cached --quiet
if ($LASTEXITCODE -ne 0) { throw 'The Git index must be empty before importing.' }

$plan = Get-Content -LiteralPath $PlanPath -Raw -Encoding UTF8 | ConvertFrom-Json
$sourceRoot = (Resolve-Path -LiteralPath $SourcePath).Path

# Check every source before changing the clone.
foreach ($file in $plan.files) {
    $relative = $file.path.Replace('/', [System.IO.Path]::DirectorySeparatorChar)
    $sourceRelative = $relative
    if ($file.source_path) { $sourceRelative = $file.source_path.Replace('/', [System.IO.Path]::DirectorySeparatorChar) }
    $source = Join-Path $sourceRoot $sourceRelative
    if (-not (Test-Path -LiteralPath $source -PathType Leaf)) {
        throw "Missing source file: $source"
    }
    if ((Get-Item -LiteralPath $source).Length -ne [int64]$file.bytes) {
        throw "Source size differs from the Google Drive snapshot: $source"
    }
    if ((Get-BlobHash $source) -ne $file.sha) {
        throw "Source content differs from the Google Drive snapshot: $source"
    }
}
foreach ($file in $plan.files) {
    $relative = $file.path.Replace('/', [System.IO.Path]::DirectorySeparatorChar)
    $sourceRelative = $relative
    if ($file.source_path) { $sourceRelative = $file.source_path.Replace('/', [System.IO.Path]::DirectorySeparatorChar) }
    $source = Join-Path $sourceRoot $sourceRelative
    $destination = Join-Path $RepoRoot $relative
    $alreadyCorrect = (Test-Path -LiteralPath $destination -PathType Leaf) -and ((Get-BlobHash $destination) -eq $file.sha)
    if (-not $alreadyCorrect) {
        $parent = Split-Path -Parent $destination
        [void][System.IO.Directory]::CreateDirectory($parent)
        Copy-Item -LiteralPath $source -Destination $destination
        if ((Get-BlobHash $destination) -ne $file.sha) { throw "Copy verification failed: $destination" }
    }
    & git -C $RepoRoot add -- $file.path
    Assert-GitSuccess "stage $($file.path)"
}
& git -C $RepoRoot diff --cached --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Host 'All 62 course files already match the verified snapshot.'
} else {
    & git -C $RepoRoot commit -m 'Complete import of all 62 original Microeconomics seminar files'
    Assert-GitSuccess 'commit course files'
}
& git -C $RepoRoot push origin main
Assert-GitSuccess 'push main'
Write-Host 'All 62 original files have been verified and pushed to GitHub.'
