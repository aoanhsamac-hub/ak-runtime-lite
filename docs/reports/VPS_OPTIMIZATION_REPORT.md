# VPS Optimization Report

## Target System
- **RAM**: 2 GB total, ~333 MB available after base processes
- **CPU**: 4 cores
- **OS**: Windows Server / Windows VPS
- **Role**: AK-RUNTIME-LITE deployment

## Baseline RAM Usage
| Component | RAM (MB) | Priority | Notes |
|-----------|----------|----------|-------|
| Windows Search Indexer | ~200-500 | **Disable** | High CPU/RAM cost, not needed on VPS |
| Cortana / Search UI | ~50-100 | **Disable** | Not needed on headless VPS |
| Windows Defender Real-time | ~150-300 | **Keep but exclude** | Security critical; exclude AK paths |
| Windows Update | ~50-200 | **Schedule** | Manual check only |
| Explorer Shell | ~30-60 | **Keep** | System required |
| Third-party services | varies | **Audit** | Disable non-essential |
| MT5 Terminal | ~200-400 | **Keep** | Required for trading observer |
| Tailscale | ~30-60 | **Keep** | Required for remote access |
| Firewall (Defender) | ~30-50 | **Keep** | Security critical on VPS |

## Optimization Actions

### 1. Disable Search Indexing (Save: ~200-500 MB)
```
Stop-Service -Name WSearch -Force
Set-Service -Name WSearch -StartupType Disabled
```

### 2. Disable SysMain (Superfetch) (Save: ~50-150 MB)
```
Stop-Service -Name SysMain -Force
Set-Service -Name SysMain -StartupType Disabled
```

### 3. Disable Diagnostic Services (Save: ~30-80 MB)
```
Stop-Service -Name DiagTrack -Force
Stop-Service -Name dmwappushservice -Force
Set-Service -Name DiagTrack -StartupType Disabled
Set-Service -Name dmwappushservice -StartupType Disabled
```

### 4. Optimize Visual Effects (Save: ~30-50 MB)
```
Set-ItemProperty -Path "HKCU:\Software\Microsoft\Windows\CurrentVersion\Explorer\VisualEffects" -Name "VisualFXSetting" -Value 2
```

### 5. Defender Path Exclusions (No RAM savings, reduces CPU)
```
Add-MpPreference -ExclusionPath "D:\AK"
Add-MpPreference -ExclusionPath "D:\MT5"
```

### 6. Disable Scheduled Disk Defrag (Save: ~20-40 MB occasional)
```
Disable-MMAgent -MemoryCompression  # No - only on some OS
```

### 7. Power Plan to High Performance (CPU optimization)
```
powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c
```

## Expected RAM After Optimization
| Metric | Before | After |
|--------|--------|-------|
| OS + Background | ~1,400 MB | ~950 MB |
| MT5 Terminal | ~300 MB | ~300 MB |
| AK Runtime | ~150 MB | ~150 MB |
| **Total Used** | **~1,850 MB** | **~1,400 MB** |
| **Available** | **~150 MB** | **~600 MB** |

## Recommendations
1. Apply optimizations via PowerShell script at deployment
2. Monitor RAM hourly via RuntimeGuard (threshold: 200 MB)
3. If RAM consistently < 200 MB, trigger stop condition
4. Do NOT disable Defender, Firewall, Tailscale, or MT5
5. Do NOT disable Windows Update service entirely - set to manual check only

## Risk Assessment
| Change | Risk | Mitigation |
|--------|------|------------|
| Disable Search Indexing | Low | No functional impact on AK |
| Disable SysMain | Low | May affect app load times slightly |
| Disable Diagnostics | Low | No functional impact |
| Visual Effects | Low | No functional impact on headless VPS |
| Defender Exclusions | Medium | Only exclude D:\AK and MT5 paths |
