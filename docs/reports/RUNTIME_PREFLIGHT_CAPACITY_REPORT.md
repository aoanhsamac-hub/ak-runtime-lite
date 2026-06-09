# RUNTIME PREFLIGHT CAPACITY REPORT

## Authority
Yết Kiêu

## Measured Resources

| Resource | Current Usage | Available | Total | Threshold | Status |
|----------|--------------|-----------|-------|-----------|--------|
| **RAM** | 6.7 GB (41.2%) | 9.6 GB | 16 GB | Min 500 MB free | PASS |
| **CPU** | Low | ~95% idle | 4 cores | Min 1 core | PASS |
| **Disk C:** | 68.2 GB (59.5%) | 46.4 GB | 114.6 GB | Min 10 GB free | PASS |
| **Disk D:** | 54.6 GB (44.4%) | 68.5 GB | 123.1 GB | Min 10 GB free | PASS |
| **Network** | Low utilization | Full bandwidth | Wi-Fi | N/A | PASS |

## Top Memory Consumers (Development Environment)

| Process | Memory (MB) |
|---------|-------------|
| Browser (Edge/Chrome) | ~486 |
| MSTSC (Remote Desktop) | ~287 |
| OpenCode (x3) | ~716 (total) |
| SearchHost | ~190 |
| Explorer | ~158 |
| PhoneExperienceHost | ~156 |
| Tailscale (x3) | ~104 (total) |

## Maximum Safe Runtime Capacity

| Component | Estimated Safe Limit | Notes |
|-----------|--------------------|-------|
| **AK-RUNTIME-LITE** | 200 MB | Base runtime memory estimate |
| **MT5 Observer** | 150 MB | Demo observer, read-only |
| **Python Runtime** | 100 MB | Script execution overhead |
| **Telegram Bot** | 50 MB | Message processing |
| **Scheduler** | 30 MB | Task scheduling overhead |
| **Total AK Runtime** | ~530 MB | Safe within available 9.6 GB |

## Recommendation

```
APPROVED - CAPACITY SUFFICIENT
```

Available capacity is approximately 18x the estimated AK-RUNTIME-LITE requirement.

## VPS Capacity Warning
If deploying to VPS with 2 GB RAM / 333 MB available:
- AK-RUNTIME-LITE (530 MB estimate) will NOT fit.
- VPS requires resource reduction or RAM upgrade before deployment.
- **VPS would trigger STOP CONDITION (RAM < 200MB) immediately.**

## Final Vote
**APPROVED** for PC development deployment. **NOT_APPROVED** for 2GB/333MB VPS target.
