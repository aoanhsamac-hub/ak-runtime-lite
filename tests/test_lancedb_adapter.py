from memory.lancedb_adapter import LanceDBAdapter, LanceDBUnavailableError


class FakeBackend:
    def __init__(self):
        self.tables = {}

    def create_table(self, name, data=None, mode=None):
        table = FakeTable(data or [])
        self.tables[name] = table
        return table

    def open_table(self, name):
        if name not in self.tables:
            raise FileNotFoundError(name)
        return self.tables[name]


class FakeTable:
    def __init__(self, rows):
        self.rows = list(rows)

    def add(self, rows):
        self.rows.extend(rows)

    def search(self, query):
        return FakeSearch(self.rows, query)


class FakeSearch:
    def __init__(self, rows, query):
        self.rows = rows
        self.query = query
        self._limit = 10

    def limit(self, limit):
        self._limit = limit
        return self

    def to_list(self):
        return [
            row for row in self.rows
            if self.query.lower() in str(row).lower()
        ][: self._limit]


class TextOnlyTable(FakeTable):
    def search(self, query):
        raise ValueError("There is no vector column in the data")

    def to_arrow(self):
        return FakeArrow(self.rows)

    def to_pandas(self):
        return FakeFrame(self.rows)


class FakeArrow:
    def __init__(self, rows):
        self.rows = rows

    def to_pylist(self):
        return list(self.rows)


class FakeFrame:
    def __init__(self, rows):
        self.rows = rows

    def to_dict(self, orient):
        assert orient == "records"
        return list(self.rows)


def test_lancedb_adapter_uses_injected_backend_without_importing_lancedb(tmp_path):
    adapter = LanceDBAdapter(tmp_path, backend=FakeBackend())
    adapter.insert("lessons", [{"lesson_id": "L-1", "content": "coding lesson"}])

    results = adapter.search("lessons", "coding", limit=5)

    assert results == [{"lesson_id": "L-1", "content": "coding lesson"}]


def test_lancedb_adapter_fails_closed_when_lancedb_missing(tmp_path):
    adapter = LanceDBAdapter(tmp_path)

    try:
        adapter.connect()
    except LanceDBUnavailableError as exc:
        assert "lancedb" in str(exc).lower()
    else:
        assert adapter.backend is not None


def test_lancedb_adapter_has_no_sqlite_or_json_fallback(tmp_path):
    adapter = LanceDBAdapter(tmp_path, backend=FakeBackend())

    assert adapter.backend_kind == "lancedb"
    assert not hasattr(adapter, "sqlite_path")
    assert not hasattr(adapter, "json_path")


class StrictCreateBackend(FakeBackend):
    def __init__(self):
        super().__init__()
        self.create_calls = []

    def create_table(self, name, data=None, mode=None):
        self.create_calls.append((name, list(data or []), mode))
        if not data:
            raise AssertionError("real LanceDB table creation needs first-row data or schema")
        return super().create_table(name, data=data, mode=mode)


def test_lancedb_adapter_creates_table_with_first_insert_rows(tmp_path):
    backend = StrictCreateBackend()
    adapter = LanceDBAdapter(tmp_path, backend=backend)

    adapter.insert("lessons", [{"lesson_id": "L-1", "content": "first row"}])

    assert backend.create_calls == [
        ("lessons", [{"lesson_id": "L-1", "content": "first row"}], None)
    ]
    assert backend.tables["lessons"].rows == [{"lesson_id": "L-1", "content": "first row"}]


def test_lancedb_adapter_search_missing_table_returns_empty_without_creating(tmp_path):
    backend = StrictCreateBackend()
    adapter = LanceDBAdapter(tmp_path, backend=backend)

    assert adapter.search("missing", "anything") == []
    assert backend.create_calls == []


def test_lancedb_adapter_falls_back_to_text_scan_without_vector_column(tmp_path):
    backend = FakeBackend()
    backend.tables["lessons"] = TextOnlyTable([
        {"lesson_id": "L-1", "content": "real lancedb runtime smoke"},
        {"lesson_id": "L-2", "content": "other"},
    ])
    adapter = LanceDBAdapter(tmp_path, backend=backend)

    assert adapter.search("lessons", "runtime smoke", limit=1) == [
        {"lesson_id": "L-1", "content": "real lancedb runtime smoke"}
    ]
