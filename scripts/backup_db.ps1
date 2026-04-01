Param(
    [string]$ProjectRoot = "$(Split-Path -Parent $PSScriptRoot)"
)

$PythonExe = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
$BackupScript = Join-Path $ProjectRoot "scripts\backup_db.py"

if (-not (Test-Path $PythonExe)) {
    Write-Error "Python executable not found: $PythonExe"
    exit 1
}

if (-not (Test-Path $BackupScript)) {
    Write-Error "Backup script not found: $BackupScript"
    exit 1
}

& $PythonExe $BackupScript
exit $LASTEXITCODE
