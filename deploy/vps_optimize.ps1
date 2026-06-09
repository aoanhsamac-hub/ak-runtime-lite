<#
.SYNOPSIS
VPS Optimization Script — run on target VPS before deployment.
Saves ~450 MB RAM by disabling non-critical Windows services.
#>

$ErrorActionPreference = "Continue"

Write-Host "=== VPS OPTIMIZATION ===" -ForegroundColor Cyan
Write-Host "Target: >= 500 MB available RAM" -ForegroundColor Cyan
Write-Host ""

# Record baseline
$os = Get-CimInstance Win32_OperatingSystem
$baselineFree = [math]::Round($os.FreePhysicalMemory / 1KB, 0)
Write-Host "Baseline available RAM: ${baselineFree} MB" -ForegroundColor Yellow

# 1. Disable Search Indexing
Write-Host "`n[1/6] Disabling Search Indexing..." -ForegroundColor Green
try {
    Stop-Service -Name WSearch -Force -ErrorAction SilentlyContinue
    Set-Service -Name WSearch -StartupType Disabled -ErrorAction SilentlyContinue
    Write-Host "  ✓ WSearch disabled"
} catch { Write-Host "  ⚠ $_" }

# 2. Disable SysMain (Superfetch)
Write-Host "[2/6] Disabling SysMain..." -ForegroundColor Green
try {
    Stop-Service -Name SysMain -Force -ErrorAction SilentlyContinue
    Set-Service -Name SysMain -StartupType Disabled -ErrorAction SilentlyContinue
    Write-Host "  ✓ SysMain disabled"
} catch { Write-Host "  ⚠ $_" }

# 3. Disable Diagnostic Services
Write-Host "[3/6] Disabling diagnostic services..." -ForegroundColor Green
try {
    Stop-Service -Name DiagTrack -Force -ErrorAction SilentlyContinue
    Set-Service -Name DiagTrack -StartupType Disabled -ErrorAction SilentlyContinue
    Write-Host "  ✓ DiagTrack disabled"
} catch { Write-Host "  ⚠ $_" }
try {
    Stop-Service -Name dmwappushservice -Force -ErrorAction SilentlyContinue
    Set-Service -Name dmwappushservice -StartupType Disabled -ErrorAction SilentlyContinue
    Write-Host "  ✓ dmwappushservice disabled"
} catch { Write-Host "  ⚠ $_" }

# 4. Visual Effects — performance mode
Write-Host "[4/6] Optimizing visual effects..." -ForegroundColor Green
try {
    Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects" -Name "VisualFXSetting" -Value 2 -ErrorAction SilentlyContinue
    Write-Host "  ✓ Visual effects set to performance"
} catch { Write-Host "  ⚠ $_" }

# 5. Defender exclusions (must run as admin)
Write-Host "[5/6] Configuring Defender exclusions..." -ForegroundColor Green
try {
    Add-MpPreference -ExclusionPath "D:\AK" -ErrorAction SilentlyContinue
    Add-MpPreference -ExclusionPath "D:\MT5" -ErrorAction SilentlyContinue
    Write-Host "  ✓ Exclusions added for D:\AK and D:\MT5"
} catch { Write-Host "  ⚠ $_" }

# 6. Power plan — High Performance
Write-Host "[6/6] Setting power plan to High Performance..." -ForegroundColor Green
try {
    powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c 2>$null
    Write-Host "  ✓ Power plan set"
} catch { Write-Host "  ⚠ $_" }

# Record after
$os2 = Get-CimInstance Win32_OperatingSystem
$afterFree = [math]::Round($os2.FreePhysicalMemory / 1KB, 0)
$saved = $afterFree - $baselineFree

Write-Host ""
Write-Host "=== OPTIMIZATION COMPLETE ===" -ForegroundColor Cyan
Write-Host "Baseline available RAM: ${baselineFree} MB" 
Write-Host "After optimization:      ${afterFree} MB"
Write-Host "RAM saved:               ${saved} MB"
if ($afterFree -ge 500) {
    Write-Host "✓ Target met (>= 500 MB)" -ForegroundColor Green
} else {
    Write-Host "⚠ Target NOT met. Available: ${afterFree} MB < 500 MB" -ForegroundColor Red
}
