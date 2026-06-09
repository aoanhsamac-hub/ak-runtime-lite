from __future__ import annotations

from pathlib import Path
from typing import Any


class LanceDBUnavailableError(RuntimeError):
    """Raised when runtime LanceDB is required but not installed."""


class LanceDBAdapter:
    """Thin AK memory adapter.

    LanceDB is imported lazily so AK modules remain importable before the
    dependency is installed. Tests may inject a backend, but production storage
    must be LanceDB only.
    """

    backend_kind = "lancedb"

    def __init__(self, db_path: str | Path, backend: Any | None = None):
        self.db_path = Path(db_path)
        self.backend = backend

    def connect(self):
        if self.backend is not None:
            return self.backend
        try:
            import lancedb  # type: ignore
        except ImportError as exc:
            raise LanceDBUnavailableError(
                "lancedb is required for AK memory runtime; no fallback store is allowed"
            ) from exc
        self.backend = lancedb.connect(str(self.db_path))
        return self.backend

    def table(self, name: str):
        backend = self.connect()
        return backend.open_table(name)

    def ensure_table(self, name: str, rows: list[dict[str, Any]]):
        backend = self.connect()
        try:
            return backend.open_table(name), False
        except Exception:
            return backend.create_table(name, data=rows), True

    def insert(self, table_name: str, rows: list[dict[str, Any]]) -> None:
        if not rows:
            return
        table, created = self.ensure_table(table_name, rows)
        if not created:
            table.add(rows)

    def search(self, table_name: str, query: str, limit: int = 10) -> list[dict[str, Any]]:
        try:
            table = self.table(table_name)
        except Exception:
            return []
        if hasattr(table, "search"):
            try:
                result = table.search(query).limit(limit)
                if hasattr(result, "to_list"):
                    return list(result.to_list())
            except Exception:
                pass
        rows = self._table_rows(table)
        return [row for row in rows if query.lower() in str(row).lower()][:limit]

    def all(self, table_name: str) -> list[dict[str, Any]]:
        try:
            table = self.table(table_name)
        except Exception:
            return []
        return self._table_rows(table)

    def create_vector_index(self, table_name: str, column: str = "", metric: str = "cosine") -> dict[str, Any]:
        try:
            table = self.table(table_name)
        except Exception:
            return {"created": False, "error": f"table not found: {table_name}"}
        if hasattr(table, "create_index"):
            try:
                kwargs = {"metric": metric}
                if column:
                    kwargs["vector_column"] = column
                table.create_index(**kwargs)
                return {"created": True, "table": table_name, "column": column or "auto", "metric": metric}
            except Exception as exc:
                return {"created": False, "error": str(exc)}
        return {"created": False, "error": "backend does not support create_index"}

    def _table_rows(self, table) -> list[dict[str, Any]]:
        if hasattr(table, "to_arrow"):
            arrow_table = table.to_arrow()
            if hasattr(arrow_table, "to_pylist"):
                return list(arrow_table.to_pylist())
        if hasattr(table, "to_pandas"):
            frame = table.to_pandas()
            if hasattr(frame, "to_dict"):
                return list(frame.to_dict("records"))
        rows = getattr(table, "rows", [])
        return list(rows)
