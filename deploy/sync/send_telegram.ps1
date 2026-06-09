# Them Git usr/bin vao PATH de tim ssh, tar, etc.
$gitBins = @("C:\Program Files\Git\usr\bin","C:\Program Files (x86)\Git\usr\bin","$env:LOCALAPPDATA\Programs\Git\usr\bin")
foreach ($p in $gitBins) { if (Test-Path "$p\ssh.exe") { $env:Path = "$p;$env:Path"; break } }

param(
    [Parameter(Mandatory=$true)]
    [string]$Message,
    [ValidateSet("info","success","warning","error")]
    [string]$Status = "info"
)

$botToken = [Environment]::GetEnvironmentVariable("TELEGRAM_BOT_TOKEN","User")
$chatId = [Environment]::GetEnvironmentVariable("TELEGRAM_WHITELIST","User")

if (-not $botToken -or -not $chatId) {
    Write-Host "TELEGRAM_BOT_TOKEN hoac TELEGRAM_WHITELIST chua duoc set. Bo qua Telegram." -ForegroundColor Yellow
    exit 0
}

$icons = @{ "info"="ℹ️"; "success"="✅"; "warning"="⚠️"; "error"="❌" }
$icon = $icons[$Status]
$hostname = $env:COMPUTERNAME
$text = "$icon [$hostname] $Message"

$body = @{
    chat_id = $chatId
    text = $text
    parse_mode = "HTML"
} | ConvertTo-Json -Compress

try {
    $url = "https://api.telegram.org/bot$botToken/sendMessage"
    $response = Invoke-RestMethod -Uri $url -Method Post -Body $body -ContentType "application/json" -TimeoutSec 10
    Write-Host "Telegram da gui: $text" -ForegroundColor Green
} catch {
    Write-Host "Loi gui Telegram: $_" -ForegroundColor Red
}
