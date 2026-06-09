<#
.SYNOPSIS
Phase A: VPS Precheck — verify Tailscale, MT5, Python, repo, secrets vault, Telegram config.
.PARAMETER ReportPath
Directory to write PRODUCTION_DEPLOYMENT_PRECHECK_REPORT.md
#>

param([string]$ReportPath = ".")

$results = @{}
$results["timestamp"] = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
$results["hostname"] = hostname
$results["checks"] = @{}

# 1. Tailscale
try {
    $ts = tailscale status --self 2>&1
    $results["checks"]["tailscale"] = @{ "status" = "OK"; "detail" = "$ts" }
} catch { $results["checks"]["tailscale"] = @{ "status" = "FAIL"; "detail" = "$_" } }

# 2. Python
try {
    $pyVer = python --version 2>&1
    $results["checks"]["python"] = @{ "status" = "OK"; "detail" = "$pyVer" }
    # Check packages
    $pkgs = python -c "import cryptography, psutil, requests; print('All packages OK')" 2>&1
    $results["checks"]["python_packages"] = @{ "status" = "OK"; "detail" = "$pkgs" }
} catch { $results["checks"]["python"] = @{ "status" = "FAIL"; "detail" = "$_" } }

# 3. MT5
try {
    $mt5Dir = Test-Path "C:\Program Files\MetaTrader 5"
    if ($mt5Dir) { $results["checks"]["mt5_installed"] = @{ "status" = "OK"; "detail" = "MT5 directory exists" } }
    else { $results["checks"]["mt5_installed"] = @{ "status" = "WARN"; "detail" = "MT5 not found at default path" } }
} catch { $results["checks"]["mt5_installed"] = @{ "status" = "WARN"; "detail" = "$_" } }

# 4. Runtime repo
$akPath = "D:\AK"
try {
    $akExists = Test-Path $akPath
    if ($akExists) {
        $services = @(Get-ChildItem "$akPath\services\*.py" -ErrorAction SilentlyContinue).Count
        $results["checks"]["runtime_repo"] = @{ "status" = "OK"; "detail" = "Found $services service files in $akPath" }
    } else {
        $results["checks"]["runtime_repo"] = @{ "status" = "FAIL"; "detail" = "$akPath not found" }
    }
} catch { $results["checks"]["runtime_repo"] = @{ "status" = "FAIL"; "detail" = "$_" } }

# 5. Secrets vault
try {
    $vaultExists = Test-Path "$akPath\data\secrets\secrets.enc"
    $saltExists = Test-Path "$akPath\data\secrets\.salt"
    if ($vaultExists -and $saltExists) {
        $results["checks"]["secrets_vault"] = @{ "status" = "OK"; "detail" = "Vault and salt files present" }
    } else {
        $results["checks"]["secrets_vault"] = @{ "status" = "WARN"; "detail" = "Vault not initialized. Run phase_b first." }
    }
} catch { $results["checks"]["secrets_vault"] = @{ "status" = "FAIL"; "detail" = "$_" } }

# 6. Telegram token
try {
    $token = [Environment]::GetEnvironmentVariable("TELEGRAM_BOT_TOKEN", "User")
    if ($token) {
        $parts = $token -split ":"
        if ($parts.Count -eq 2 -and $parts[0] -match "^\d+$" -and $parts[1].Length -ge 30) {
            $results["checks"]["telegram_token"] = @{ "status" = "OK"; "detail" = "Token format valid" }
        } else {
            $results["checks"]["telegram_token"] = @{ "status" = "FAIL"; "detail" = "Token format invalid" }
        }
    } else {
        $results["checks"]["telegram_token"] = @{ "status" = "FAIL"; "detail" = "TELEGRAM_BOT_TOKEN not set" }
    }
} catch { $results["checks"]["telegram_token"] = @{ "status" = "FAIL"; "detail" = "$_" } }

# 7. Whitelist
try {
    $wl = [Environment]::GetEnvironmentVariable("TELEGRAM_WHITELIST", "User")
    if ($wl) { $results["checks"]["telegram_whitelist"] = @{ "status" = "OK"; "detail" = "Whitelist: $wl" } }
    else { $results["checks"]["telegram_whitelist"] = @{ "status" = "FAIL"; "detail" = "TELEGRAM_WHITELIST not set" } }
} catch { $results["checks"]["telegram_whitelist"] = @{ "status" = "FAIL"; "detail" = "$_" } }

# 8. Master password
try {
    $mp = [Environment]::GetEnvironmentVariable("AK_MASTER_SECRET", "User")
    if ($mp) { $results["checks"]["master_password"] = @{ "status" = "OK"; "detail" = "AK_MASTER_SECRET configured" } }
    else { $results["checks"]["master_password"] = @{ "status" = "FAIL"; "detail" = "AK_MASTER_SECRET not set" } }
} catch { $results["checks"]["master_password"] = @{ "status" = "FAIL"; "detail" = "$_" } }

# Write report
$reportPath = "$ReportPath\PRODUCTION_DEPLOYMENT_PRECHECK_REPORT.md"
$allPass = ($results["checks"].Values | Where-Object { $_.status -eq "FAIL" }).Count -eq 0
$md = @"
# PRODUCTION_DEPLOYMENT_PRECHECK_REPORT

## Timestamp
$($results.timestamp)

## Hostname
$($results.hostname)

## Precheck Results
"@
foreach ($check in $results["checks"].Keys) {
    $c = $results["checks"][$check]
    $icon = if ($c.status -eq "OK") { "✓" } elseif ($c.status -eq "WARN") { "⚠" } else { "✗" }
    $md += "`n| $check | $icon $($c.status) | $($c.detail) |"
}

$md += @"

## Overall
**Precheck Status: $(if ($allPass) { "PASS" } else { "ISSUES_DETECTED" })**
"@
$md | Out-File -FilePath $reportPath -Encoding UTF8
Write-Host "Phase A complete. Report: $reportPath" -ForegroundColor Green
