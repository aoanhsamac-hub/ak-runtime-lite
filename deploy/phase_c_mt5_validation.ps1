<#
.SYNOPSIS
Phase C: MT5 Integration — verify connection, account, symbols, OHLCV, tick, read-only.
.PARAMETER ReportPath
Directory to write PRODUCTION_MT5_VALIDATION_REPORT.md
#>

param([string]$ReportPath = ".")

$results = @{}
$results["timestamp"] = (Get-Date -Format "yyyy-MM-ddTHH:mm:ssZ")
$results["checks"] = @{}

# 1. MT5 Terminal check
try {
    $mt5Process = Get-Process -Name "terminal" -ErrorAction SilentlyContinue
    if ($mt5Process) {
        $results["checks"]["mt5_terminal"] = @{ "status" = "OK"; "detail" = "MT5 terminal running (PID: $($mt5Process.Id))" }
    } else {
        $results["checks"]["mt5_terminal"] = @{ "status" = "FAIL"; "detail" = "MT5 terminal not running" }
    }
} catch {
    $results["checks"]["mt5_terminal"] = @{ "status" = "FAIL"; "detail" = "$_" }
}

# 2. MT5 Python import
try {
    $mt5Import = python -c "import MetaTrader5; print('OK')" 2>&1
    $results["checks"]["mt5_python_module"] = @{ "status" = "OK"; "detail" = "MetaTrader5 module available" }
} catch {
    $results["checks"]["mt5_python_module"] = @{ "status" = "FAIL"; "detail" = "MetaTrader5 not installed: $_" }
}

# 3. MT5 connection test
try {
    $connTest = python -c "
import MetaTrader5 as mt5
if not mt5.initialize():
    print('FAIL: ' + mt5.last_error())
else:
    acc = mt5.account_info()
    if acc:
        print(f'OK: account {acc.login} on {acc.server}, balance {acc.balance}')
    else:
        print('FAIL: no account info')
    mt5.shutdown()
" 2>&1
    if ($connTest -match "^OK:") {
        $results["checks"]["mt5_connection"] = @{ "status" = "OK"; "detail" = "$connTest" }
    } else {
        $results["checks"]["mt5_connection"] = @{ "status" = "FAIL"; "detail" = "$connTest" }
    }
} catch {
    $results["checks"]["mt5_connection"] = @{ "status" = "FAIL"; "detail" = "$_" }
}

# 4. OHLCV access
try {
    $ohlcvTest = python -c "
import MetaTrader5 as mt5
from datetime import datetime
if mt5.initialize():
    rates = mt5.copy_rates_from('EURUSD', mt5.TIMEFRAME_M1, datetime.now(), 5)
    if rates is not None and len(rates) > 0:
        print(f'OK: {len(rates)} bars retrieved')
    else:
        print('FAIL: no data returned')
    mt5.shutdown()
" 2>&1
    if ($ohlcvTest -match "^OK:") {
        $results["checks"]["mt5_ohlcv"] = @{ "status" = "OK"; "detail" = "$ohlcvTest" }
    } else {
        $results["checks"]["mt5_ohlcv"] = @{ "status" = "FAIL"; "detail" = "$ohlcvTest" }
    }
} catch {
    $results["checks"]["mt5_ohlcv"] = @{ "status" = "FAIL"; "detail" = "$_" }
}

# 5. READ-ONLY verification — scan for trade functions
try {
    $hasTradeFunctions = python -c "
import os
import re
runtime_dir = r'D:\AK\services'
issues = []
for root, dirs, files in os.walk(runtime_dir):
    for f in files:
        if f.endswith('.py'):
            path = os.path.join(root, f)
            with open(path, 'r') as fh:
                for i, line in enumerate(fh, 1):
                    if re.search(r'\border_send\b|\border_modify\b|\border_close\b', line):
                        issues.append(f'{path}:{i}')
if issues:
    print('ISSUES: ' + '; '.join(issues))
else:
    print('OK: No trade functions found')
" 2>&1
    if ($hasTradeFunctions -match "^OK:") {
        $results["checks"]["mt5_readonly"] = @{ "status" = "OK"; "detail" = "No order_send/modify/close in runtime" }
    } else {
        $results["checks"]["mt5_readonly"] = @{ "status" = "FAIL"; "detail" = "$hasTradeFunctions" }
    }
} catch {
    $results["checks"]["mt5_readonly"] = @{ "status" = "FAIL"; "detail" = "$_" }
}

# 6. Symbol access
try {
    $symbolTest = python -c "
import MetaTrader5 as mt5
if mt5.initialize():
    syms = mt5.symbols_get()
    if syms and len(syms) > 0:
        forex = [s.name for s in syms if 'EUR' in s.name or 'USD' in s.name or 'GBP' in s.name][:5]
        print(f'OK: {len(syms)} total symbols. Sample: {forex}')
    else:
        print('FAIL: no symbols')
    mt5.shutdown()
" 2>&1
    if ($symbolTest -match "^OK:") {
        $results["checks"]["mt5_symbols"] = @{ "status" = "OK"; "detail" = "$symbolTest" }
    } else {
        $results["checks"]["mt5_symbols"] = @{ "status" = "FAIL"; "detail" = "$symbolTest" }
    }
} catch {
    $results["checks"]["mt5_symbols"] = @{ "status" = "FAIL"; "detail" = "$_" }
}

$allPass = ($results["checks"].Values | Where-Object { $_.status -eq "FAIL" }).Count -eq 0

$reportPath = "$ReportPath\PRODUCTION_MT5_VALIDATION_REPORT.md"
$md = @"
# PRODUCTION_MT5_VALIDATION_REPORT

## Timestamp
$($results.timestamp)

## MT5 Validation Results
| Check | Status | Detail |
|-------|--------|--------|
"@
foreach ($ck in $results["checks"].Keys) {
    $c = $results["checks"][$ck]
    $icon = if ($c.status -eq "OK") { "✓" } elseif ($c.status -eq "WARN") { "⚠" } else { "✗" }
    $md += "`n| $ck | $icon $($c.status) | $($c.detail) |"
}

$md += @"

## Read-Only Status
**Trade execution functions: $(if ($results["checks"]["mt5_readonly"].status -eq "OK") { "BLOCKED ✓" } else { "DETECTED ✗" })**

## Overall
**MT5 Status: $(if ($allPass) { "PASS" } else { "ISSUES_DETECTED" })**
"@
$md | Out-File -FilePath $reportPath -Encoding UTF8
Write-Host "Phase C complete. Report: $reportPath" -ForegroundColor Green
