Write-Host "=== RESTART RUNTIME ===" -ForegroundColor Cyan
& "D:\AK\deploy\sync\stop_runtime.ps1"
Start-Sleep -Seconds 2
& "D:\AK\deploy\sync\start_runtime.ps1"
