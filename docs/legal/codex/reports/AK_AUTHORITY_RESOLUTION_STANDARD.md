# AK AUTHORITY RESOLUTION STANDARD

Version: v1.0
Status: ACTIVE
Authority: Hung Vuong
Owner: Lang Lieu
Reviewer: Sage

## Resolution Framework

```
Document
→ Authority Level (from REG-02_AUTHORITY.yaml)
→ Required Reviewer
→ Required Approval Authority
```

## Resolution Order

1. Document owner claims authority
2. Check REG-01_LEGAL.yaml for classification
3. Check REG-02_AUTHORITY.yaml for approval level
4. Route to appropriate reviewer
5. Escalate to Hung Vuong if LEVEL 4

## Conflict Resolution

| Conflict Type | Resolution |
|---|---|
| Authority overlap | Higher level wins |
| Classification conflict | Sage determination |
| Registry conflict | Hung Vuong decision |

## Escalation Rules

| Level | Escalation Target |
|---|---|
| 0 | None |
| 1 | Lang Lieu |
| 2 | Janus + Sage |
| 3 | Sage + Hung Vuong |
| 4 | Hung Vuong only |