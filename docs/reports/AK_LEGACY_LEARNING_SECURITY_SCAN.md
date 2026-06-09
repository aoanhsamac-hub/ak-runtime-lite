# AK Legacy Learning Security Scan

Date: 2026-06-07 | Authority: Janus Directive — AK-SANDBOX-READINESS & LEGACY LEARNING MIGRATION AUDIT v1.0

## Scan Summary

| Check | Result |
|---|---|
| Files scanned | 67 |
| Secret patterns detected | 0 |
| API key patterns | 0 |
| Private key patterns | 0 |
| Credential patterns | 0 |
| Code files with secrets | 0/27 |
| Markdown files with secrets | 0/40 |

## Patterns Checked

- Generic API keys/secrets/tokens/passwords
- OpenAI-style `sk-*` keys
- Private key headers (`-----BEGIN ... PRIVATE KEY`)
- Credential assignments

## Risk Assessment

No legacy learning file contains detectable secret patterns. All 67 files are safe for migration review.

## Note

Secrets may exist in `.env`, broker configs, or `__pycache__` bytecode — these directories are excluded by `scripts/audit_legacy_learning.py` (blocked directory list includes `__pycache__`, `.env`).
