# PC_GITHUB_MINIMUM_CLEANUP_REPORT

Generated: 2026-06-10 16:30
PC: DESKTOP-IQB9870
User: GiangKhoi
Audit: PC-GITHUB-WINDOWS-SECURITY-AUDIT-01 | Phase H

---

## Actions Performed

### H1 — SSH Config Hardening

| Field | Before | After |
|-------|--------|-------|
| File | `C:\Users\GiangKhoi\.ssh\config` | Same |
| Host `github.com` line 11 | `StrictHostKeyChecking no` | `StrictHostKeyChecking accept-new` |
| Host `ak-vps` | Unchanged | Unchanged (preserved) |

**Result:** ✅ Applied. Only `github.com` block changed. `ak-vps` remains at `no` for remote-control convenience.

---

### H2 — Git Safe Directory

```powershell
git config --global --add safe.directory D:/AK
```

| Entry | Status |
|-------|--------|
| `D:/Alkasik` | Kept (pre-existing) |
| `D:/AK` | Added |

**Result:** ✅ Applied. Both entries present.

---

### H3 — Recycle Bin Inventory

Checked `D:\$Recycle.Bin\S-1-5-21-3432697636-3353394745-1738757603-1001`.

**Finding:** Contains mixed content — not only AK/Alkasik remnants:

| Item | Type | Size | AK-related? |
|------|------|------|-------------|
| `$RL3C2N6` | Directory with `.git` | — | Yes (old D:\Alkasik repo) |
| `$R0U1DZ7.txt` | Text file | 15 MB | No |
| `$R4H1YE3.exe` | Executable | 196 MB | No |
| `$RCK5ZD5.zip` | Archive | 114 MB | No |
| Various .7z/.zip/.md | Files | Various | No |

**Decision:** **NOT CLEARED.** Per plan constraint: "If uncertain, do not clear. Report only." The recycle bin contains user files unrelated to AK.

**Recommendation:** Manual review and selective cleanup by operator.

---

### H4 — Empty Git Init Directories

| Directory | Remote? | Files? | Action | Status |
|-----------|---------|--------|--------|--------|
| `C:\Users\GiangKhoi\Documents\BTCUSD` | None | 4 items (Alkasik.7z, Ethelton.7z, dirs) | Archived → Deleted | ✅ |
| `C:\Users\GiangKhoi\Documents\SMC` | None | 1 item (forex_bot/) | Archived → Deleted | ✅ |
| `C:\Users\GiangKhoi\Documents\Alkasik Kingdom (AK)` | None | 3 dirs (_lancedb_runtime_smoke, _pytest_tmp, _source_review) | Archived (2 of 3) | ⚠️ Partial |
| `D:\AI\Project` | None | 17 items (trading bots, configs, MT5) | Archived → Deleted | ✅ |

**Partial note:** `_pytest_tmp` in `Alkasik Kingdom (AK)` could not be moved due to permission denied. Only `_lancedb_runtime_smoke` and `_source_review` were moved. `.git` removed.

**Residual:** `C:\Users\GiangKhoi\Documents\Alkasik Kingdom (AK)\_pytest_tmp` (empty, permission-locked — harmless).

---

### H5 — SSH Key Passphrase (Deferred)

| Item | Status |
|------|--------|
| `~/.ssh/github` | No passphrase — **deferred** |
| Future work item | `AK-PC-SSH-HARDENING-02` |

---

### H6 — ssh-agent (Deferred)

| Item | Status |
|------|--------|
| ssh-agent | Disabled — **deferred** |
| Reason | Not required for automation (direct key access works) |

---

## Files Changed

| File | Change |
|------|--------|
| `C:\Users\GiangKhoi\.ssh\config` | Line 11: `no` → `accept-new` for github.com |
| `C:\Users\GiangKhoi\.gitconfig` | Added `safe.directory = D:/AK` |

## Directories Archived

| Archive | Size | Location |
|---------|------|----------|
| `BTCUSD.zip` | 83 KB | `D:\AK\archive\empty_repos\` |
| `SMC.zip` | 41 KB | `D:\AK\archive\empty_repos\` |
| `Alkasik_Kingdom_AK/` | ~1 MB | `D:\AK\archive\empty_repos\` |
| `AI_Project/` | ~300 MB | `D:\AK\archive\empty_repos\` |

## Directories Deleted

- `C:\Users\GiangKhoi\Documents\BTCUSD`
- `C:\Users\GiangKhoi\Documents\SMC`
- `C:\Users\GiangKhoi\Documents\Alkasik Kingdom (AK)` (partial — _pytest_tmp remains)
- `D:\AI\Project`

---

## Remaining Items

1. `C:\Users\GiangKhoi\Documents\Alkasik Kingdom (AK)\_pytest_tmp` — permission-locked, empty
2. `D:\$Recycle.Bin\...\$RL3C2N6` — old D:\Alkasik repo (deleted, in bin)
3. `D:\$Recycle.Bin\...\$RL3C2N6\Open source\agents-towards-production` — upstream fork clone

## Deferred Hardening

- `AK-PC-SSH-HARDENING-02` — Add passphrase to GitHub SSH key + enable ssh-agent
