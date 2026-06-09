# Retrieval Optimization Report

**Date:** 2026-06-07
**Authority:** Hermes-36-000
**Status:** RECOMMENDATIONS ONLY — NO EXECUTION

---

## 1. Current Retrieval Architecture

```
Agent → MemoryInterface → {LessonRegistry, SkillRegistry, CapabilityRegistry, DatasetRegistry, DecisionTraceRegistry}
                              ↓
                         _records: dict (in-memory)
                              ↓
                      LanceDBAdapter → LanceDB (persistent)
                              ↓
                    LanceDB search → vector/text/fallback
```

All 5 code registries implement the same pattern:
- In-memory `_records: dict[str, RecordType]` for all CRUD
- `list_records()` returns full dict dump (no pagination)
- `search()` delegates to `LanceDBAdapter.search()` with full-table scan fallback
- No cross-registry query capability

---

## 2. Identified Bottlenecks

| ID | Bottleneck | Location | Severity |
|----|------------|----------|----------|
| B1 | **Volatile in-memory state** | All 5 registries: `_records: dict` | CRITICAL |
| B2 | **No persistent indices** | All YAML registries | HIGH |
| B3 | **Full-table scan fallback** | `lancedb_adapter.py:68` | HIGH |
| B4 | **No pagination** | All `list_records()` methods | MEDIUM |
| B5 | **No filtered queries** | All registries | MEDIUM |
| B6 | **No cross-registry joins** | Lesson ↔ Skill ↔ Capability | HIGH |
| B7 | **Single backend dependency** | `LanceDBAdapter` only | MEDIUM |
| B8 | **No materialized aggregation** | `knowledge_registry/` empty | MEDIUM |
| B9 | **LanceDB lazy fail-closed** | `lancedb_adapter.py:29-33` | LOW |
| B10 | **No archive index** | `memory/archive_registry/` empty | LOW |

---

## 3. Optimization Recommendations

### O1: Persist In-Memory Registries to LanceDB

**Problem:** `_records: dict` is populated on `__init__` by reading from LanceDB but never materialized as a persistent index. All data lost on process restart unless every `_save()` call reaches LanceDB.

**Recommendation:** Implement a boot-time hydration query that loads all rows from each LanceDB table into the in-memory dict. Add a periodic flush or write-through strategy so in-memory state never diverges from LanceDB.

**Expected improvement:** Elimination of silent data loss risk. Guaranteed persistence on every write path.

---

### O2: Create LanceDB Vector Indexes

**Problem:** `LanceDBAdapter.search()` falls back to `[row for row in rows if query.lower() in str(row).lower()]` — a linear scan — for tables without vector columns.

**Recommendation:** Configure LanceDB IVF-PQ indexes on the `content` and `summary` columns of the `lessons` table, `description` of `skills`, and `reasoning` of `decision_traces`. This enables sub‑millisecond approximate nearest‑neighbor search.

**Expected improvement:** O(n) full-table scan → O(log n) indexed search.

---

### O3: Add Pagination and Filtering to All Registries

**Problem:** `list_records()` returns every record as a flat list. Growing data volumes will cause unbounded memory and latency.

**Recommendation:** Add `list_records(offset=0, limit=100, status=None, owner_agent=None, tags=None)` parameters to all 5 registries. Implement server-side filtering in LanceDB queries instead of Python-side list comprehensions.

**Expected improvement:** Bounded response size. Filter push-down to database layer.

---

### O4: Implement Cross-Registry Foreign Key Index

**Problem:** Skills reference lessons by ID, capabilities reference skills by ID, but there is no index to traverse lesson→skill→capability. Queries must load all records and join in Python memory.

**Recommendation:** Create a materialized cross-reference view in `memory/knowledge_registry/`:

```yaml
cross_references:
  - lesson_id: LESSON-XXXX
    skills: [SKILL-YYYY, SKILL-ZZZZ]
    capabilities: [CAP-AAAA]
    traces: [TRACE-BBBB]
    status: APPROVED
```

This enables O(1) graph traversal from any lesson to its derived skills, capabilities, and supporting decision traces.

**Expected improvement:** O(n) sequential scan → O(1) index lookup for lineage queries.

---

### O5: Index YAML Registries in LanceDB

**Problem:** All 13 YAML registry files are parsed sequentially on every read. No index exists for `legal_index.yaml`, `protected_modules.yaml`, etc.

**Recommendation:** Create a dedicated `registry_index` table in LanceDB that mirrors all YAML registries. Update on registry write. This allows agents to query registries through the same `search()` API instead of file I/O.

**Expected improvement:** File I/O → indexed database query. Unified query interface for all registry types.

---

### O6: Build Archive Registry

**Problem:** 6 backup archives exist in `archive/` with no index. Restoring historical state requires manual inspection of each backup directory.

**Recommendation:** Create `memory/archive_registry/archive_index.yaml`:

```yaml
archives:
  - id: ARCHIVE-001
    date: 2026-06-07_011203
    source: sovereign/
    trigger: legal_reorganization
    registry_snapshot: <sha256 of legal_index.yaml at time>
```

**Expected improvement:** Discoverable backup history. Point-in-time restore capability.

---

### O7: Implement Caching Layer

**Problem:** Frequently accessed registries (legal_index.yaml, protected_modules.yaml) are re-read from disk on every access.

**Recommendation:** Add a read-through cache (TTL: 300s) for YAML registries. Invalidate on write. Cache hit avoids disk I/O.

**Expected improvement:** Sub-millisecond registry access for hot paths.

---

### O8: Introduce Streaming / Iterator for Large Result Sets

**Problem:** As the system grows, `list_records()` returning thousands of lessons will exhaust memory.

**Recommendation:** Implement `iter_records(batch_size=100)` generator on all registries. Yield records in batches from LanceDB using cursor-based pagination.

**Expected improvement:** Bounded memory consumption regardless of record count.

---

### O9: Enforce Search Index Before Table Scan

**Problem:** `LanceDBAdapter.search()` at line 68 unconditionally falls back to a Python list comprehension scan if the table has no `search()` method or if the search throws.

**Recommendation:** Before fallback, check if a vector index exists on the table. If not, raise `IndexRequiredError` instead of silently degrading. This makes missing indexes visible rather than hidden.

**Expected improvement:** Fail fast with actionable error instead of silent O(n) degradation.

---

## 4. Proposed Implementation Priority

| Priority | Opt | Description | Effort | Impact |
|----------|-----|-------------|--------|--------|
| P0 | O1 | Persist in-memory registries | Low | Critical |
| P0 | O3 | Pagination + filtering | Low | Critical |
| P1 | O2 | Vector indexes on LanceDB | Medium | High |
| P1 | O4 | Cross-registry index | Medium | High |
| P1 | O5 | Index YAML registries | Medium | High |
| P2 | O8 | Streaming iterators | Low | Medium |
| P2 | O7 | Read-through cache | Low | Medium |
| P3 | O6 | Archive registry | Low | Low |
| P3 | O9 | Fail on missing index | Low | Low |

---

## 5. Expected Outcomes After Full Implementation

| Metric | Before | After |
|--------|--------|-------|
| Registry query latency | O(n) scan | O(log n) index |
| Cross-registry traversal | Full load + Python join | O(1) index lookup |
| Memory safety | Risk of OOM | Bounded batches |
| Data persistence | Volatile on restart | Guaranteed write-through |
| Backup discoverability | Manual inspection | Indexed archive |
| YAML registry access | File I/O | Indexed DB query |
| Search quality | Substring fallback | Semantic vector search |

---

*End of Retrieval Optimization Report.*
