# National Knowledge Lifecycle Model

**Directive:** WP-KP-01 Phase 1
**Date:** 2026-06-07
**Status:** FINAL

---

## 1. Purpose

Define the single national knowledge lifecycle governing all knowledge artifacts in the Alkasik Kingdom. Every lesson, decision trace, dataset, skill, and capability follows the same lifecycle states and transitions.

---

## 2. Lifecycle States

```
    ┌─────────────────────────────────────────────────────────┐
    │                    EVIDENCE (raw)                       │
    │  Operational activity, task outcomes, agent decisions   │
    └────────────────────────┬────────────────────────────────┘
                             │ pipeline extracts
                             ▼
    ┌─────────────────────────────────────────────────────────┐
    │                 CANDIDATE (DRAFT)                       │
    │  Auto-extracted by pipeline. Not yet human-reviewed.    │
    │  Not promotable. Not referenceable by other artifacts.  │
    └────────────────────────┬────────────────────────────────┘
                             │ submit_for_review()
                             ▼
    ┌─────────────────────────────────────────────────────────┐
    │                  REVIEW (REVIEWED)                      │
    │  Under governance review. Sage evaluates quality,       │
    │  risk, completeness. Reject → QUARANTINE.               │
    │  Approve → APPROVED.                                    │
    └──────────┬──────────────────────────────┬───────────────┘
               │ reject                       │ approve
               ▼                              ▼
    ┌──────────────────────┐    ┌───────────────────────────────┐
    │    QUARANTINE        │    │        APPROVED              │
    │  Blocked. Requires   │    │  Governance-approved.        │
    │  investigation.      │    │  Referenceable by other      │
    │  May transition to   │    │  artifacts. May be promoted. │
    │  ARCHIVE or re-      │    └───────────┬───────────────────┘
    │  enter CANDIDATE.    │                │ activate (skills/
    └──────────────────────┘                │ capabilities only)
                                            ▼
                              ┌───────────────────────────────┐
                              │         ACTIVE                │
                              │  Operational use. Only        │
                              │  applies to skills and        │
                              │  capabilities.                │
                              └───────────┬───────────────────┘
                                          │ deprecate
                                          ▼
                              ┌───────────────────────────────┐
                              │       DEPRECATED              │
                              │  Superseded by newer version. │
                              │  Preserved for audit trail.   │
                              │  May transition to ARCHIVE.   │
                              └───────────┬───────────────────┘
                                          │ archive
                                          ▼
                              ┌───────────────────────────────┐
                              │        ARCHIVE                │
                              │  Cold storage. Not in active  │
                              │  working set. Retrievable     │
                              │  for audit or restoration.    │
                              └───────────────────────────────┘
```

---

## 3. State Definitions

| State | Definition | Governance Required | Referenceable |
|-------|------------|-------------------|---------------|
| EVIDENCE | Raw operational data. Not yet a knowledge artifact. | No | No |
| CANDIDATE | Pipeline-extracted draft. Not yet reviewed. | No | No |
| REVIEWED | Passed initial evaluation. Under governance review. | Yes (Sage) | No |
| APPROVED | Governance-approved. Fully referenceable. | Yes (Sage + Janus) | Yes |
| ACTIVE | Operational use (skills/capabilities only). | Yes (Janus) | Yes |
| DEPRECATED | Superseded. Preserved for audit. | Yes (Sage) | Yes (read-only) |
| QUARANTINE | Blocked. Under investigation. | Yes (Sage + Janus) | No |
| ARCHIVE | Cold storage. Not in active working set. | Yes (Janus) | Via archive index |

---

## 4. Allowed Transitions

| From | To | Authority | Trigger |
|------|----|-----------|---------|
| EVIDENCE | CANDIDATE | Pipeline (Hermes) | Auto-extraction |
| CANDIDATE | REVIEWED | Sage | submit_for_review() |
| REVIEWED | APPROVED | Sage + Janus | approve() |
| REVIEWED | QUARANTINE | Sage | reject() |
| APPROVED | ACTIVE | Janus | activate() (skills/capabilities only) |
| APPROVED | DEPRECATED | Sage | deprecate() |
| ACTIVE | DEPRECATED | Sage | deprecate() |
| DEPRECATED | ARCHIVE | Janus | archive() |
| QUARANTINE | CANDIDATE | Sage + Janus | re-evaluate() |
| QUARANTINE | ARCHIVE | Sage | archive() |
| Any | QUARANTINE | Sage + Janus | Policy violation |

---

## 5. Artifact-Specific Lifecycles

| Artifact | States Used | Max State | Promotion Path |
|----------|-------------|-----------|----------------|
| Decision Trace | EVIDENCE → CANDIDATE → REVIEWED → APPROVED → DEPRECATED → ARCHIVE | APPROVED | Not promotable |
| Lesson | EVIDENCE → CANDIDATE → REVIEWED → APPROVED → DEPRECATED → ARCHIVE | APPROVED | May contribute to skill |
| Dataset | EVIDENCE → CANDIDATE → REVIEWED → APPROVED → DEPRECATED → ARCHIVE | APPROVED | May contribute to training |
| Skill | CANDIDATE → REVIEWED → APPROVED → ACTIVE → DEPRECATED → ARCHIVE | ACTIVE | May contribute to capability |
| Capability | CANDIDATE → REVIEWED → APPROVED → ACTIVE → DEPRECATED → ARCHIVE | ACTIVE | Final evolution stage |

---

## 6. Lifecycle Compliance

| Requirement | Compliance |
|-------------|------------|
| Knowledge must emerge from evidence | EVIDENCE → CANDIDATE pipeline enforced |
| Knowledge must be governed | Every promotion requires Sage/Janus approval |
| Knowledge must be auditable | Full state transition history in audit log |
| Knowledge must be versioned | Each transition increments version |
| Knowledge must be traceable | source_hash links artifact to originating evidence |

---

*End of Knowledge Lifecycle Model.*
