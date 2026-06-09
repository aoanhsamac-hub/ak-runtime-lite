from __future__ import annotations

from typing import Any

from memory.learning_registry.schemas import SignalClusterRecord


class SignalClusterRegistry:
    table_name = "signal_clusters"

    def __init__(self, adapter=None):
        self.adapter = adapter
        self._records: dict[str, SignalClusterRecord] = {}
        self._hydrate()

    def _hydrate(self) -> None:
        if not self.adapter:
            return
        rows = self.adapter.all(self.table_name)
        for row in rows:
            try:
                filtered = {k: v for k, v in row.items() if k in SignalClusterRecord.__dataclass_fields__}
                record = SignalClusterRecord(**filtered)
                self._records[record.cluster_id] = record
            except (TypeError, ValueError):
                continue

    def create_cluster(self, **payload) -> SignalClusterRecord:
        record = SignalClusterRecord(**payload)
        self._save(record)
        return record

    def get(self, cluster_id: str) -> SignalClusterRecord:
        try:
            return self._records[cluster_id]
        except KeyError as exc:
            raise KeyError(f"signal cluster not found: {cluster_id}") from exc

    def list_all(self, offset: int = 0, limit: int = 0,
                 cluster_type: str | None = None,
                 owner_agent: str | None = None) -> list[SignalClusterRecord]:
        records = list(self._records.values())
        if cluster_type:
            records = [r for r in records if r.cluster_type == cluster_type]
        if owner_agent:
            records = [r for r in records if r.owner_agent == owner_agent]
        if limit > 0:
            records = records[offset:offset + limit]
        elif offset > 0:
            records = records[offset:]
        return records

    def _save(self, record: SignalClusterRecord) -> None:
        self._records[record.cluster_id] = record
        if self.adapter:
            self.adapter.insert(self.table_name, [record.to_dict()])
