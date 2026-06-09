# CAR: Law & Charter Review

**Date:** 2026-06-08
**Phase:** D
**Status:** GAPS_FOUND

---

## 1. Laws Reviewed

| # | Law/Decree | Source Location | Status |
|---|------------|-----------------|--------|
| 1 | ALKASIK_AGENT_LAW_v1.0_FINAL | `docs/legal/canon/` | **Binary-only** — original .docx not extractable; Key Requirements extracted |
| 2 | ALKASIK_MEMORY_LAW_v1.0_FINAL | `docs/legal/canon/` | **Binary-only** — original .docx not extractable; Key Requirements extracted |
| 3 | ALKASIK_INFORMATION_LAW_v1.0_FINAL | `docs/legal/canon/` | **Binary-only** — original .docx not extractable; I0-I9 classification extracted |
| 4 | ALKASIK_RISK_LAW_v1.0_FINAL | `docs/legal/canon/` | **Binary-only** — original .docx not extractable; risk levels extracted |
| 5 | ALKASIK_EXECUTION_LAW_v1.0_FINAL | `docs/legal/canon/` | **Binary-only** — original .docx not extractable; execution states extracted |
| 6 | ALKASIK_SECURITY_LAW_v1.0_FINAL | `docs/legal/canon/` | **Binary-only** — original .docx not extractable; data classes extracted |
| 7 | ALKASIK_ECONOMIC_LAW_v1.0_FINAL | `docs/legal/canon/` | **Binary-only** — original .docx not extractable; capability lifecycle extracted |
| 8 | ALKASIK_REPO_GOVERNANCE_DECREE_v1.0_FINAL | `docs/legal/canon/` | **Binary-only** — original .docx not extractable; repo rules extracted |
| 9 | ALKASIK_KNOWLEDGE_GOVERNANCE_DECREE_v1.0_FINAL | `docs/legal/canon/` | **Binary-only** — original .docx not extractable; knowledge lifecycle extracted |
| 10 | ALKASIK_RETENTION_ARCHIVE_GOVERNANCE_DECREE_v1.0_FINAL | `docs/legal/canon/` | **Binary-only** — original .docx not extractable; retention classes extracted |
| 11 | AK_KINGDOM_BUDGET_LAW_v1.0_FINAL | `docs/laws/` | **Extractable** — fully formed markdown, no binary dependency |

**Note:** The user brief states 12 laws/decrees. Only 11 were found. Constitution v1.1 FINAL (which would be the 12th document) is missing from `docs/governance/`. This is a gap.

### Binary-only note

All 10 canon law files carry the disclaimer: *"Original .docx file is binary and not extractable in current environment."* The canonical markdown files contain reconstructed Key Requirements but the authoritative .docx source cannot be directly verified. This creates a canonicalization risk for audit purposes.

---

## 2. Constitution → Law Mapping

Reference constitution: `ALKASIK_CONSTITUTION_v1.0.md` (baseline). Note: `v1.1_FINAL` does **not** exist on disk — only v1.0 is present.

| Constitution Article | Implementing Law(s) | Status |
|----------------------|---------------------|--------|
| **Art 1 — Sovereignty** (Hung Vuong supreme, no agent may alter objectives/risk kernel/execution/governance without approval) | Agent Law, Repo Governance Decree | Covered |
| **Art 2 — Objectives** (preserve capital, sustainable growth, disciplined operations, integration, 5 operational domains, bilingual mandate) | Economic Law, Capability Economy Framework, Budget Law | Covered (partially — bilingual mandate has no dedicated law) |
| **Art 3 — Safety** (7 safety principles: backup, no-delete, Sage review for risk kernel, test before merge, agent trade scope, dashboard safety, change logging) | Risk Law, Security Law, Execution Law, Repo Governance Decree | Covered |
| **Art 4 — Agent Authority** (Janus, Sage, Lang Lieu, Hermes, Iris, Helen, Yet Kieu roles and restrictions) | Agent Law, Janus Charter, Hermes Charter, Agent Charter (DRAFT) | **Partially covered** — Sage, Lang Lieu, Iris, Helen, Yet Kieu have no FINAL charters |
| **Art 5 — Risk Kernel** (inviolable; lot size, max DD, max exposure, max orders, margin guard, emergency stop, portfolio, kill switch require Sage review) | Risk Law | Covered |
| **Art 6 — Execution** (high danger zone; MT5 orders, TP/SL, trailing, spread, slippage, magic number, symbol config must be tested) | Execution Law | Covered |
| **Art 7 — Memory & Learning** (lessons require source, date, agent, validation, status; no unverified error→skill) | Memory Law, Knowledge Governance Decree, Retention & Archive Governance Decree | Covered |
| **Art 8 — Autonomous Coding** (Issue→Plan→Code→Review→Test→Sage→Janus→Deploy; OpenCode is tool, not decider) | Execution Law, Governance Charter (DRAFT) | **Partially covered** — Governance Charter is DRAFT only |
| **Art 9 — Emergency Power** (Sage requests safe mode; Yet Kieu reports runtime; Janus coordinates; Hung Vuong decides) | Emergency Reserve Framework, Security Law | Covered (financial emergencies only — Art 9's safe-mode/system emergency not codified in law) |
| **Art 10 — Amendments** (12-step process: propose → analyze → debate → review → approve → version) | Repo Governance Decree | Covered |

### CRITICAL FINDING: Missing v1.1

`ALKASIK_CONSTITUTION_v1.1_FINAL.md` does **not** exist in `docs/governance/`. However, `CONSTITUTIONAL_MAPPING.md` (dated 2026-06-07) references constitution Articles 27, 36, 37, 38 — numbers that do **not** exist in v1.0 (which has only 10 articles). This proves v1.1 existed at the time of the mapping but has since been lost or was never saved to disk. **Without v1.1, the full constitutional baseline for this review is unavailable.**

---

## 3. Law → Charter Mapping

| Law/Decree | Implementing Charter(s) | Status |
|------------|------------------------|--------|
| Agent Law | Janus Charter (FINAL), Hermes Charter (FINAL), Agent Charter (DRAFT in `docs/governance/`) | Partially covered — Sage, Lang Lieu, Iris, Helen, Yet Kieu charters missing |
| Memory Law | Hermes Charter (FINAL) | Covered |
| Information Law | **No charter** (Helen has no FINAL charter) | **GAP** |
| Risk Law | **No charter** (Sage has no FINAL charter) | **GAP** |
| Execution Law | **No charter** (Lang Lieu has no FINAL charter) | **GAP** |
| Security Law | **No charter** (Yet Kieu has no FINAL charter) | **GAP** |
| Economic Law | Treasury Charter (FINAL), Royal Treasury Charter (FINAL), Capability Economy Framework (FINAL) | Covered |
| Repo Governance Decree | **No charter** | **GAP** |
| Knowledge Governance Decree | Hermes Charter (FINAL) | Covered |
| Retention & Archive Governance Decree | Hermes Charter (FINAL) | Covered |
| Kingdom Budget Law | Treasury Charter (FINAL), Royal Treasury Charter (FINAL), Emergency Reserve Framework (FINAL) | Covered |

### Available FINAL Charters

| Charter | Path | Status |
|---------|------|--------|
| Janus Charter | `docs/charters/JANUS_CHARTER_v1.0_FINAL.md` | FINAL |
| Hermes Charter | `docs/charters/HERMES_CHARTER_v1.0_FINAL.md` | FINAL |
| Kingdom Treasury Charter | `docs/charters/AK_TREASURY_CHARTER_v1.0_FINAL.md` | FINAL |
| Royal Treasury Charter | `docs/charters/AK_ROYAL_TREASURY_CHARTER_v1.0_FINAL.md` | FINAL |

### Available DRAFT Charters (not FINAL)

| Charter | Path | Status |
|---------|------|--------|
| ALKASIK_AGENT_CHARTER_v1.0 | `docs/governance/ALKASIK_AGENT_CHARTER_v1.0.md` | DRAFT (no FINAL suffix, no authority/reviewer metadata) |
| ALKASIK_GOVERNANCE_CHARTER_v1.0 | `docs/governance/ALKASIK_GOVERNANCE_CHARTER_v1.0.md` | DRAFT (no FINAL suffix, Vietnamese-only, no authority/reviewer metadata) |

---

## 4. Gap Analysis

### 4.1 Constitutionally-mandated areas not covered by any law

| Constitutional Requirement | Coverage | Severity |
|---------------------------|----------|----------|
| Art 2 — Bilingual mandate (Vietnamese for decrees/proposals/reports; translation of foreign materials to both VN and EN) | **No dedicated law** | MEDIUM |
| Art 3.5 — "Không để agent tự trade ngoài phạm vi được cấp quyền" (agents may not trade outside authorized scope) | Implicit in Agent Law + Risk Law, but no explicit trade-scope boundary law | LOW |
| Art 3.6 — Dashboard safety: "Không để dashboard kiêm quyền điều khiển nguy hiểm nếu chưa có lớp xác nhận" | **Not codified in any law** | MEDIUM |
| Art 9 — Sage safe-mode trigger / system-level emergency (not financial) | Only financial emergencies covered by Emergency Reserve Framework; constitutional system-emergency (safe mode) not codified | **HIGH** |
| Art 4 — All 7 agent roles defined in constitution but only 2 (Janus, Hermes) have FINAL charters | 5 agents (Sage, Lang Lieu, Iris, Helen, Yet Kieu) lack FINAL charters | **HIGH** |

### 4.2 Laws that contradict the constitution

| Potential Issue | Analysis | Verdict |
|-----------------|----------|---------|
| Constitution Art 9 gives Sage authority to request safe mode; Emergency Reserve Framework escalation (Section 4) goes Detecting Agent → Janus → ... without mentioning Sage | Financial reserve framework vs constitutional system emergency — different domains. The safe-mode authority is not contradicted, just not implemented in the financial framework. | **No contradiction** (separate domains) |
| Constitution v1.0 Art 4 says Janus "không được tự ý sửa code production"; Janus Charter Section 9 says "Janus may NOT: Execute code" | Aligned | **No contradiction** |
| Constitution v1.0 Art 4 says Sage "không được tự ý tăng risk"; Risk Law says "No autonomous risk escalation" | Aligned | **No contradiction** |
| Budget Law mandates 92/8 split (Section 2). Constitution does not specify this split | No contradiction — Budget Law implements fiscal policy not enumerated in constitution | **No contradiction** (implementation detail) |

### 4.3 Charters that contradict their authorizing law

| Charter | Authorizing Law | Potential Conflict | Verdict |
|---------|-----------------|-------------------|---------|
| Janus Charter | Agent Law | Agent Law says "No autonomous execution without approval"; Janus Charter forbids execution entirely. More restrictive, not contradictory. | **No contradiction** |
| Hermes Charter | Memory Law, Knowledge Governance Decree, Retention Decree | Aligned on all counts (lesson lifecycle, knowledge stages, retention classes) | **No contradiction** |
| Treasury Charter | Economic Law | Treasury split and budget authority align with Economic Law capability lifecycle | **No contradiction** |
| Royal Treasury Charter | Economic Law | Sovereignty of Hung Vuong over royal funds aligns | **No contradiction** |

### 4.4 Binary-only law canonicalization

| Law | Risk | Assessment |
|-----|------|------------|
| Risk Law (binary .docx) | Key Requirements may be incomplete | **MEDIUM** — risk level table is likely complete but full text is unverifiable |
| Execution Law (binary .docx) | Key Requirements may be incomplete | **MEDIUM** — execution states and audit trail requirements likely complete |
| Security Law (binary .docx) | Key Requirements may be incomplete | **MEDIUM** — data class table likely complete |
| Economic Law (binary .docx) | Key Requirements may be incomplete | **MEDIUM** — capability lifecycle likely complete |
| Repo Governance Decree (binary .docx) | Key Requirements may be incomplete | **MEDIUM** — structure rules likely complete |
| Knowledge Governance Decree (binary .docx) | Key Requirements may be incomplete | **MEDIUM** — lifecycle diagram likely complete |
| Retention & Archive Governance Decree (binary .docx) | Key Requirements may be incomplete | **MEDIUM** — retention rules likely complete |
| Agent Law (binary .docx) | Sparse extraction (32 lines) | **HIGH** — only 3 restrictions listed compared to 7 agent roles in constitution |
| Memory Law (binary .docx) | Moderate extraction (30 lines) | **MEDIUM** — lesson requirements captured |
| Information Law (binary .docx) | Good extraction (33 lines) | **LOW** — I0-I9 classification fully captured |

**Overall Assessment:** All 10 canon laws originate from binary .docx sources that cannot be verified. The canonical markdown files are reconstructions. For audit and legal certainty, the .docx sources should be re-extracted in a capable environment or the markdown versions should be formally certified as authoritative replacements.

---

## 5. Missing FINAL Charters

| Agent | FINAL Charter Status | Notes |
|-------|---------------------|-------|
| **Janus** | `JANUS_CHARTER_v1.0_FINAL.md` ✓ | FINAL — upgraded from DRAFT, certified by NCP-R Wave 2 |
| **Hermes** | `HERMES_CHARTER_v1.0_FINAL.md` ✓ | FINAL — upgraded from DRAFT, certified by NCP-R Wave 2 |
| **Sage** | **MISSING** ❌ | No Sage charter exists in any directory — not even a DRAFT |
| **Lang Lieu** | **MISSING** ❌ | No Lang Lieu charter exists — not even a DRAFT |
| **Iris** | **MISSING** ❌ | No Iris charter exists — not even a DRAFT |
| **Helen** | **MISSING** ❌ | No Helen charter exists — not even a DRAFT |
| **Yet Kieu** | **MISSING** ❌ | No Yet Kieu charter exists — not even a DRAFT |

| Supporting Component | FINAL Status | Notes |
|---------------------|--------------|-------|
| **ALKASIK_AGENT_CHARTER** | DRAFT only | `docs/governance/ALKASIK_AGENT_CHARTER_v1.0.md` — no FINAL suffix, no reviewer metadata |
| **ALKASIK_GOVERNANCE_CHARTER** | DRAFT only | `docs/governance/ALKASIK_GOVERNANCE_CHARTER_v1.0.md` — no FINAL suffix, Vietnamese-only |

---

## 6. Verdict

| Dimension | Result |
|-----------|--------|
| **Constitution→Law Coverage** | 7 of 10 articles fully covered; 3 partially covered (Art 4, Art 8, Art 9) |
| **Law→Charter Coverage** | 4 of 11 laws have implementing charters; 5 laws (Information, Risk, Execution, Security, Repo Governance Decree) lack charters |
| **Constitutional Contradictions** | None found |
| **Law→Charter Contradictions** | None found |
| **Binary-only Canonicalization** | All 10 canon laws are unverifiable against .docx originals. AGENT_LAW extraction is critically sparse. |
| **Missing Constitution** | v1.1 FINAL referenced in CONSTITUTIONAL_MAPPING.md but absent from disk — articles 27, 36, 37, 38 referenced in mapping cannot be verified |
| **Missing Agent Charters** | 5 of 7 constitutionally-defined agents (Sage, Lang Lieu, Iris, Helen, Yet Kieu) have no FINAL charter |
| **DRAFT Items Pending Upgrade** | ALKASIK_AGENT_CHARTER v1.0, ALKASIK_GOVERNANCE_CHARTER v1.0 |

### Overall Verdict

**GAPS_FOUND.** The constitutional-to-legal-to-charter hierarchy is structurally sound for the domains that are implemented, but there are material gaps:

1. **Constitution v1.1 FINAL is missing** — this is the most critical finding, as it is the current baseline authority.
2. **5 of 7 agents lack FINAL charters** — Sage, Lang Lieu, Iris, Helen, and Yet Kieu have no operational charter defining their authority, permissions, and restrictions beyond the constitution.
3. **All 10 canon laws are binary-dependent** — the authoritative .docx source cannot be extracted, leaving the markdown reconstructions as best-effort approximations.
4. **3 constitutional requirements are not codified in any law**: dashboard safety (Art 3.6), bilingual mandate enforcement (Art 2.6), and system-level emergency safe-mode procedure (Art 9).

**Recommended immediate actions:**
- Recover or recreate Constitution v1.1 FINAL
- Produce FINAL charters for Sage, Lang Lieu, Iris, Helen, and Yet Kieu
- Upgrade ALKASIK_AGENT_CHARTER and ALKASIK_GOVERNANCE_CHARTER to FINAL
- Re-extract binary .docx sources or formally certify markdown canons as authoritative
- Codify dashboard safety, bilingual compliance, and safe-mode emergency procedure into law
