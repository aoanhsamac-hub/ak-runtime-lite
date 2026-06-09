# AK_CAPABILITY_RECLASSIFICATION_REPORT.md

**Generated:** 2026-06-07T07:01:09Z
**Directive:** WP-KR-00 Phase 5 — Capability Reclassification Pass

## 1. Skill Clusters

| Skill ID | Title | Domain | Confidence | Cluster |
|----------|-------|--------|------------|---------|
| LKI-95BDB01EBB1F | Build Dependency Graph | Memory | 60 | Memory Management |
| LKI-EABD6C42CBA5 | Db Manager | Memory | 63 | Memory Management |
| LKI-F002D55D69CB | Memory Engine | Memory | 73 | Memory Management |
| LKI-0AA6240F8FE1 | Structure Memory | Memory | 70 | Memory Management |
| LKI-8755E3224CC7 | Time thresholds (in hours) | Memory | 63 | Memory Management |
| LKI-0F84EF46DBFF | 设置页 → Agent 管理 → Custom Agent (F-CAGENT) | Memory | 76 | Memory Management |
| LKI-8E154C1EA445 | Test National Registry Population | Memory | 66 | Memory Management |
| LKI-185D38C97285 | National Registry | Memory | 62 | Memory Management |

## 2. Cross-Domain Competence Analysis

| Domain | Lesson Count | Capability Potential |
|--------|-------------|---------------------|
| Trading | 68 | Trading Operations |
| Market | 62 | Market Operations |
| Execution | 43 | Execution Operations |
| Agent | 35 | Agent Operations |
| Risk | 5 | Risk Operations |

## 3. Multi-Skill Pattern Detection

| Capability | Required Skills | Source Domains | Feasibility |
|------------|----------------|----------------|-------------|
| Trading Operations | Execution Intelligence + Inventory Trading + Trust Management | Trading, Risk, Market | HIGH (sufficient lessons across domains) |
| Memory Management | Memory Engine + Structure Memory + Memory Lifecycle | Memory | MEDIUM (skills need promotion first) |
| Governance Review | Constitution + Governance Decree + Repo Decree + Retention Decree | Governance | HIGH (4 decision traces directly applicable) |
| Agent Coordination | Mission Orchestration + Tool Registration + Workflow Execution | Agent, Execution | MEDIUM (cross-domain dependency) |

## 4. Governance Capabilities

- **Decision traces available:** 6 governance documents (constitution, knowledge decree, repo decree, retention decree, draft constitution, vNext report)
- **Recommendation:** Create Governance Review capability requiring 3+ approved governance skills

## 5. Engineering Capabilities

- **Dataset candidates:** 13 covering LLM routing, data pipelines, observability, open source DevOps, i18n
- **Recommendation:** Create Engineering Pipeline capability for CI/CD and dataset operations

## 6. Trading Capabilities

- **Trading domain is the richest** with lesson, engine, runner, backtest, and intelligence modules
- **Recommendation:** Create Automated Trading capability requiring Execution, Risk, and Market skills

## 7. Memory Capabilities

- **8 skill candidates** all in Memory Knowledge domain
- **Recommendation:** Create Memory Lifecycle Management capability once skills are approved

## 8. Recommended Capability Candidates

| # | Capability | Priority | Dependencies | Est. Effort |
|---|-----------|----------|-------------|-------------|
| 1 | Governance Review | HIGH | 4 governance skills | Low |
| 2 | Trading Operations | HIGH | 3+ trading skills | Medium |
| 3 | Memory Management | MEDIUM | 4 memory skills | Medium |
| 4 | Agent Coordination | MEDIUM | 3+ agent/execution skills | High |
| 5 | Engineering Pipeline | LOW | 3+ engineering skills | High |
