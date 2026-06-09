# Them Git usr/bin vao PATH de tim ssh, tar, etc.
$gitBins = @("C:\Program Files\Git\usr\bin","C:\Program Files (x86)\Git\usr\bin","$env:LOCALAPPDATA\Programs\Git\usr\bin")
foreach ($p in $gitBins) { if (Test-Path "$p\ssh.exe") { $env:Path = "$p;$env:Path"; break } }

$ErrorActionPreference = "Continue"
$logFile = "D:\AK\logs\sync_push.log"
$sourceDir = "D:/AK"
$targetDir = "C:/AK"
$excludeFile = "D:\AK\deploy\sync\exclude_list.txt"
$startTime = Get-Date

Write-Host "=== PUSH SOURCE: PC -> VPS ===" -ForegroundColor Cyan
Write-Host "Bat dau: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"

# Kiem tra SSH
if (-not (Test-Path "D:\AK\logs\.ssh_done")) {
    Write-Host "LOI: Chua chay setup_ssh.ps1. Chay truoc." -ForegroundColor Red
    exit 1
}

# Kiem tra SSH connection
$test = ssh -o BatchMode=yes -o ConnectTimeout=5 ak-vps "echo OK" 2>$null
if ($test -ne "OK") {
    Write-Host "LOI: Khong SSH duoc vao VPS. Kiem tra ket noi." -ForegroundColor Red
    & "D:\AK\deploy\sync\send_telegram.ps1" -Message "PUSH SOURCE THAT BAI: Khong SSH duoc vao VPS" -Status error
    exit 1
}

# Build exclude flags cho tar
$excludes = @()
if (Test-Path $excludeFile) {
    Get-Content $excludeFile | ForEach-Object {
        $pattern = $_.Trim()
        if ($pattern -and $pattern -notmatch '^#') {
            $excludes += "--exclude"
            $excludes += $pattern
        }
    }
}

# Tim tar.exe tu Git Bash
$tarPaths = @(
    "C:\Program Files\Git\usr\bin\tar.exe",
    "C:\Program Files (x86)\Git\usr\bin\tar.exe",
    "$env:LOCALAPPDATA\Programs\Git\usr\bin\tar.exe"
)
$tarExe = $null
foreach ($p in $tarPaths) {
    if (Test-Path $p) { $tarExe = $p; break }
}
if (-not $tarExe) {
    Write-Host "LOI: Khong tim thay tar.exe tu Git Bash" -ForegroundColor Red
    exit 1
}

Write-Host "Dang nen va gui source tu $sourceDir len VPS:$targetDir ..." -ForegroundColor Yellow

# Tar & pipe qua SSH
& $tarExe -c $excludes -C $sourceDir . 2>&1 | ssh ak-vps "mkdir -p $targetDir 2>nul && cd $targetDir && tar -x" 2>&1

$exitCode = $LASTEXITCODE
$endTime = Get-Date
$duration = ($endTime - $startTime).TotalSeconds

if ($exitCode -eq 0) {
    Write-Host "THANH CONG! ($duration giay)" -ForegroundColor Green
    "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') | PUSH OK | ${duration}s" | Out-File -FilePath $logFile -Encoding UTF8 -Append
    & "D:\AK\deploy\sync\send_telegram.ps1" -Message "PUSH SOURCE THANH CONG ($duration giay)" -Status success
} else {
    Write-Host "THAT BAI! (exit code: $exitCode)" -ForegroundColor Red
    "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') | PUSH FAIL | exit=$exitCode" | Out-File -FilePath $logFile -Encoding UTF8 -Append
    & "D:\AK\deploy\sync\send_telegram.ps1" -Message "PUSH SOURCE THAT BAI (exit code: $exitCode)" -Status error
    exit 1
}
