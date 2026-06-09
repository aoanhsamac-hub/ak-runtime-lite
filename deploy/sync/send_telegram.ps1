# send_telegram.ps1 — Gui thong bao Telegram (FIXED v2)
param(
    [string]$Message = "",
    [string]$Status = "info"
)

$botToken = if ($env:TELEGRAM_BOT_TOKEN) { $env:TELEGRAM_BOT_TOKEN } else { [Environment]::GetEnvironmentVariable("TELEGRAM_BOT_TOKEN","Machine") }
$chatId = if ($env:TELEGRAM_WHITELIST) { $env:TELEGRAM_WHITELIST } else { [Environment]::GetEnvironmentVariable("TELEGRAM_WHITELIST","Machine") }

if (-not $botToken -or -not $chatId) {
    Write-Host "TELEGRAM_BOT_TOKEN hoac TELEGRAM_WHITELIST chua duoc set. Bo qua Telegram." -ForegroundColor Yellow
    exit 0
}

if (-not $Message) {
    Write-Host "Message trong. Bo qua." -ForegroundColor Yellow
    exit 0
}

$icons = @{ "info"="ℹ️"; "success"="✅"; "warning"="⚠️"; "error"="❌" }
$icon = if ($icons.ContainsKey($Status)) { $icons[$Status] } else { "ℹ️" }
$text = "$icon [VPS] $Message"

try {
    $body = @{ chat_id = $chatId; text = $text; parse_mode = "HTML" } | ConvertTo-Json -Compress
    $url = "https://api.telegram.org/bot$botToken/sendMessage"
    Invoke-RestMethod -Uri $url -Method Post -Body $body -ContentType "application/json" -TimeoutSec 10 | Out-Null
    Write-Host "Telegram da gui" -ForegroundColor Green
} catch {
    Write-Host "Loi gui Telegram: $($_.Exception.Message)" -ForegroundColor Red
}
