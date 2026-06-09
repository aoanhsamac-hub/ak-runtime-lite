# health_check.ps1 - Kiem tra system health tren PC
$proc = Get-Process python* -ErrorAction SilentlyContinue
$ram = Get-CimInstance Win32_OperatingSystem -ErrorAction SilentlyContinue
$freeRAM = [math]::Round($ram.FreePhysicalMemory/1MB, 1)
$totalRAM = [math]::Round($ram.TotalVisibleMemorySize/1MB, 1)
Write-Host "Python processes: $($proc.Count)"
Write-Host "Free RAM: $freeRAM GB / $totalRAM GB"
