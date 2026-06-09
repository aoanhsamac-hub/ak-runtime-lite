# Retrieval Optimization — Implementation Plan

**Directive:** HERMES-CLEANUP-01 Phase 5
**Date:** 2026-06-07
**Status:** PLAN ONLY — NO EXECUTION

---

## 1. Current Retrieval Architecture Review

### 1.1 Hermes Findings (Validated)

| Finding | Status | Detail |
|---------|--------|--------|
| In-memory only storage | CONFIRMED | All 5 Python registries use `_records: dict` |
| No vector indexes | CONFIRMED | LanceDB tables exist but no IVF-PQ configured |
| Full-table scan fallback | CONFIRMED | `[row for row in rows if query.lower() in str(row).lower()]` |
| No pagination | CONFIRMED | `list_records()` returns unbounded list |
| No cross-registry index | CONFIRMED | lesson→skill→capability graph has no index |
| YAML registries unindexed | CONFIRMED | Sequential parse on every read |
| Archive not indexed | CONFIRMED | `memory/archive_registry/` empty |
| No caching layer | CONFIRMED | Every registry access re-reads from source |

### 1.2 Current Query Latency Estimates

| Query Type | Current Mechanism | Est. Latency (0 records) | Est. Latency (10K records) |
|-----------|------------------|--------------------------|---------------------------|
| Get lesson by ID | `_records[lesson_id]` (O(1)) | <1ms | <1ms |
| List all lessons | `list(_records.values())` (O(n)) | <1ms | ~10ms |
| Search lessons | LanceDB fallback scan (O(n)) | <1ms | ~500ms |
| List skills for agent | List comprehension filter (O(n)) | <1ms | ~50ms |
| Cross-registry (lesson→skill→cap) | Full load + Python join (O(n×m)) | <1ms | ~5s |
| YAML registry lookup | File read + parse (O(1)) | ~2ms | ~2ms |
| Archive lookup | Manual directory listing | ~50ms | ~500ms |

---

## 2. Optimization Opportunities

### 2.1 Critical Priority (P0)

| ID | Optimization | Current | Target | Effort |
|----|-------------|---------|--------|--------|
| O1 | **Persist in-memory state to LanceDB** | Volatile dict, data lost on restart | Write-through to LanceDB on every `_save()` | Low |
| O2 | **Add pagination to all list_records()** | Unbounded returns | `offset`/`limit` params; LanceDB query push-down | Low |
| O3 | **Add filtered queries to all registries** | Full list + Python filter | Server-side filtering by status, owner, tags | Low |

### 2.2 High Priority (P1)

| ID | Optimization | Current | Target | Effort |
|----|-------------|---------|--------|--------|
| O4 | **Create LanceDB vector indexes** | Full-table scan on search | IVF-PQ index on content/summary columns | Medium |
| O5 | **Build cross-registry reference index** | O(n×m) Python joins | O(1) graph lookup via central index | Medium |
| O6 | **Index YAML registries in LanceDB** | Sequential file parse per read | Fast DB-backed lookup via registry_index table | Medium |

### 2.3 Medium Priority (P2)

| ID | Optimization | Current | Target | Effort |
|----|-------------|---------|--------|--------|
| O7 | **Implement read-through cache** | Re-reads YAML on every access | TTL-based cache (300s) with write invalidation | Low |
| O8 | **Add streaming iterators** | All records in memory at once | Batch iterator (100 records per batch) | Low |

### 2.4 Lower Priority (P3)

| ID | Optimization | Current | Target | Effort |
|----|-------------|---------|--------|--------|
| O9 | **Build archive index** | No programmatic archive discovery | `archive_registry.yaml` with snapshot hashes | Low |
| O10 | **Fail-fast on missing indexes** | Silent fallback to full scan | Raise `IndexRequiredError` when index absent | Low |

---

## 3. Implementation Roadmap

### 3.1 Sprint 1 — Foundation (Priority: P0)

| Task | Files Affected | Description | Acceptance |
|------|---------------|-------------|------------|
| T1.1 | `memory/lesson_registry.py` | Add boot-time hydration: load all rows from LanceDB on `__init__` | All persisted lessons are available in-memory on startup |
| T1.2 | `memory/skill_registry.py` | Same pattern as T1.1 | Skills survive restart |
| T1.3 | `memory/capability_registry.py` | Same pattern | Capabilities survive restart |
| T1.4 | `memory/dataset_registry.py` | Same pattern | Datasets survive restart |
| T1.5 | `memory/decision_trace_registry.py` | Same pattern | Traces survive restart |
| T1.6 | All 5 registries | Add `list_records(offset=0, limit=100, status=None, owner=None, tags=None)` | Paginated, filtered queries supported |
| T1.7 | `memory/lancedb_adapter.py` | Ensure `search()` supports filtered queries | Filters push down to LanceDB |

**Verification:** `python -m pytest tests/` — existing tests continue to pass. New tests verify hydration and pagination.

### 3.2 Sprint 2 — Indexing (Priority: P1)

| Task | Files Affected | Description | Acceptance |
|------|---------------|-------------|------------|
| T2.1 | `memory/lancedb_adapter.py` | Add `create_vector_index(column, metric="cosine")` | IVF-PQ index created on LanceDB table |
| T2.2 | `tests/test_lancedb_adapter.py` | Add index creation test | Index creation verified in CI |
| T2.3 | New: `memory/index_registry.py` | Cross-registry index: `knowledge_registry/cross_reference.yaml` | O(1) lookup from lesson→skill→capability |
| T2.4 | `memory/knowledge_registry/` | Populate with materialized cross-reference view | Graph traversal without full table loads |
| T2.5 | New: `memory/yaml_registry_index.py` | Index YAML registries in LanceDB `registry_index` table | YAML queries go through DB, not file I/O |
| T2.6 | `sovereign/legal_index.yaml` | First target for YAML indexing | Legal queries use database index |

**Verification:** Cross-reference test: given lesson_id, return associated skills, capabilities, and traces in <10ms.

### 3.3 Sprint 3 — Performance (Priority: P2–P3)

| Task | Files Affected | Description | Acceptance |
|------|---------------|-------------|------------|
| T3.1 | New: `memory/cache.py` | Generic read-through cache with TTL | Configurable TTL, write-through invalidation |
| T3.2 | All 5 registries | Apply cache decorator to hot paths | Cache hit: <1ms, cache miss: normal path |
| T3.3 | All 5 registries | Add `iter_records(batch_size=100)` generator | No OOM with 1M records |
| T3.4 | New: `memory/archive_registry/archive_index.yaml` | Index of all 6 backup archives | Programmatic archive discovery |
| T3.5 | `memory/lancedb_adapter.py` | Add index existence check before fallback | Fail fast with `IndexRequiredError` |

**Verification:** Performance benchmarks: search <10ms for 10K records (indexed), pagination bounded at 100 records, cache hits <1ms.

---

## 4. Architecture After Optimization

```
Agent → MemoryInterface
           │
           ├── LessonRegistry ─────┐
           ├── SkillRegistry ──────┤
           ├── CapabilityRegistry ─┤  ←─ hydrated from LanceDB on boot
           ├── DatasetRegistry ────┤
           └── DecisionTraceRegistry ┘
                    │
                    ├── Cache (TTL 300s)
                    │
                    ├── LanceDBAdapter
                    │       ├── Vector index (IVF-PQ)
                    │       ├── Text index
                    │       └── Registry index table
                    │
                    ├── CrossReferenceIndex (knowledge_registry/)
                    │       └── lesson → skill → capability → trace
                    │
                    ├── YAMLRegistryIndex (registry_index table)
                    │       └── legal, constitution, agent, governance, ...
                    │
                    └── ArchiveIndex (archive_registry/archive_index.yaml)
                            └── backup date → snapshot hash
```

---

## 5. Performance Targets

| Query Type | Before | After (10K records) | Improvement |
|-----------|--------|---------------------|-------------|
| Search lessons | ~500ms (full scan) | <10ms (vector index) | 50× |
| List lessons (paginated) | ~10ms (all) | <1ms (100 batch) | 10× |
| Cross-registry lookup | ~5s (Python join) | <1ms (index) | 5000× |
| YAML registry access | ~2ms (file I/O) | <1ms (DB index) | 2× |
| Cache hit (hot path) | ~2ms (file I/O) | <1ms (memory) | 2× |
| Known lesson by ID | <1ms (dict) | <1ms (dict) | — |

---

*End of Retrieval Optimization Implementation Plan.*
