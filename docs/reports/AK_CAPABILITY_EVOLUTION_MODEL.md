# AK_CAPABILITY_EVOLUTION_MODEL.md

**Generated:** 2026-06-07T09:30:21Z
**Directive:** WP35-PREP-01 Phase 4 — Capability Evolution Model
**Status:** Design Complete (No Runtime Activation)

---

## 1. Capability Lifecycle

```
                    +-----------+
                    |   DRAFT   |
                    +-----+-----+
                          |
                    +-----v-----+
              +-----+  REVIEWED +------+
              |     +-----+-----+      |
        (Reject)          |      (Needs Evidence)
              |     +-----v-----+      |
              +---->+ APPROVED  +<-----+
                    +-----+-----+
                          |
                    +-----v-----+
                    |  ACTIVE   |
                    +-----+-----+
                          |
             +-----------+-----------+
             |           |           |
       +-----v--+  +----v----+  +---v------+
       |EMERGING|  |DEVELOPING|  |ESTABLISHED|
       +-----+--+  +----+----+  +----+-----+
             |           |           |
       +-----v--+  +----v----+  +---v------+
       |DECLINING| | RETIRED  | | ADVANCED |
       +---------+ +---------+ +----------+
```

## 2. Lifecycle Stages

| Stage | Description | Requirements | Authority |
|-------|-------------|-------------|-----------|
| DRAFT | Capability candidate identified | >= 2 active skills | Automated |
| REVIEWED | Passed initial review | Evidence evaluation PASS | Sage + Hermes |
| APPROVED | Approved for activation | Governance gate PASS | Hung Vuong |
| ACTIVE | Available for agent inheritance | Owner activation | Hermes |
| EMERGING | Early capability maturity | < 3 months active | Metrics |
| DEVELOPING | Growing capability | 3-6 months, >= 2 agents | Metrics |
| ESTABLISHED | Mature capability | > 6 months, >= 4 agents | Metrics |
| ADVANCED | Peak capability | > 12 months, >= 6 agents, cross-domain | Metrics |
| DECLINING | Capability losing relevance | Decreasing usage metrics | Hermes |
| RETIRED | Capability no longer used | Zero usage for > 90 days | Sage |

## 3. Capability Creation

### 3.1 Creation Triggers

- **Multi-skill pattern detected:** >= 2 active skills from related domains
- **Cross-domain convergence:** Skills from 3+ domains forming coherent capability
- **Strategic nomination:** Agent or governance body nominates
- **Evolution detection:** Capability evolution from existing capability

### 3.2 Creation Requirements

| Requirement | Minimum |
|-------------|---------|
| Active skills | 2 |
| Distinct domains | 1 |
| Combined confidence | >= 70 (average) |
| Evidence quality | >= 3/5 (average per skill) |
| Strategic alignment | Must align with AK strategic objectives |

## 4. Maturity Levels

### 4.1 Emerging

```
Characteristics:
  - Recently activated (< 3 months)
  - Limited agent adoption (1-2 agents)
  - Single domain focus
  - High oversight requirement
  - Weekly review cycle
```

### 4.2 Developing

```
Characteristics:
  - 3-6 months since activation
  - Growing agent adoption (2-3 agents)
  - Starting cross-domain application
  - Moderate oversight
  - Bi-weekly review cycle
```

### 4.3 Established

```
Characteristics:
  - > 6 months since activation
  - Wide agent adoption (4-5 agents)
  - Cross-domain operation
  - Low oversight required
  - Monthly review cycle
```

### 4.4 Advanced

```
Characteristics:
  - > 12 months since activation
  - Near-universal agent adoption (6-7 agents)
  - Multi-domain mastery
  - Minimal oversight
  - Quarterly review cycle
```

### 4.5 Sovereign

```
Characteristics:
  - Constitutional-level capability
  - All agents adopted
  - All domains covered
  - Self-governing
  - Annual review
  - Hung Vuong-level oversight only
```

## 5. Capability Evidence

| Evidence Type | Description | Weight |
|--------------|-------------|--------|
| Operational metrics | Demonstrated capability usage | 30% |
| Lesson support | Underlying lessons supporting capability | 25% |
| Skill maturity | Average maturity of constituent skills | 25% |
| Cross-domain reach | Number of domains covered | 10% |
| Agent feedback | Agent-reported effectiveness | 10% |

## 6. Capability Governance

| Aspect | Requirement |
|--------|-------------|
| Creation gate | Sage + Hermes review |
| Approval gate | Hung Vuong approval |
| Maturity promotion | Automated metric evaluation |
| Decline detection | Monthly metrics review |
| Retirement | Sage authority + audit |
| Emergency stop | Hung Vuong immediate authority |

## 7. Capability Decline and Retirement

| Phase | Trigger | Action | Authority |
|-------|---------|--------|-----------|
| DECLINING | Usage down 50% over 30 days | Notification, review | Hermes |
| RETIRED | Zero usage for 90 days | Mark as RETIRED | Sage |
| ARCHIVED | RETIRED for > 1 year | Move to archive | Hermes |
