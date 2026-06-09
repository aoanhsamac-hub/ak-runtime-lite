# pull_from_github.ps1 - PC git pull reports tu GitHub
$ErrorActionPreference = "Continue"
$logFile = "D:\AK\logs\github_pull.log"
$startTime = Get-Date

Write-Host "=== GIT PULL: GitHub -> PC ===" -ForegroundColor Cyan

cd D:\AK
try {
    git fetch origin main 2>&1 | Out-Null
    $localHash = git rev-parse HEAD
    $remoteHash = git rev-parse origin/main
    
    if ($localHash -ne $remoteHash) {
        Write-Host "Co cap nhat moi. Dang pull..." -ForegroundColor Yellow
        git pull origin main 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "PULL THANH CONG" -ForegroundColor Green
            "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') | PULL OK | $remoteHash" | Out-File $logFile -Append
            & "D:\AK\deploy\sync\send_telegram.ps1" -Message "PC: Pull reports thanh cong - commit $remoteHash" -Status success
        } else {
            Write-Host "PULL THAT BAI" -ForegroundColor Red
            "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') | PULL FAIL" | Out-File $logFile -Append
            & "D:\AK\deploy\sync\send_telegram.ps1" -Message "PC: Pull reports that bai" -Status error
        }
    } else {
        Write-Host "Da o commit moi nhat ($localHash)" -ForegroundColor Green
    }
} catch {
    Write-Host "LOI: $_" -ForegroundColor Red
    "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') | PULL ERROR | $_" | Out-File $logFile -Append
}

$duration = ((Get-Date) - $startTime).TotalSeconds
Write-Host "($duration giay)" -ForegroundColor Cyan
