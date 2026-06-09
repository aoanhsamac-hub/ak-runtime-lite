# WP3 Memory Platform Workflow

This workflow validates the AK-native learning layer, LanceDB memory adapter,
agent memory interface, and OpenCode adapter-only safety boundary.

Run:

```powershell
D:\AK\.venv\Scripts\python.exe -m workflows.wp3_acceptance
```

Expected pass condition:

- score >= 0.95
- required WP3 files present
- no SQLite, Chroma, or FAISS memory backend usage
- LanceDB runtime dependency available
- OpenCode protected paths blocked
- local LanceDB insert/search smoke passes

