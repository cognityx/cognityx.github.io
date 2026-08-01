# Cognityx Python SDK

This is the main public entry point for day-to-day work.
It provides a thin Python client for convenience, and the `cogni` command for
document ingest and inspection.

```python
from cognityx import Cogni

cogni = Cogni.load()
result = cogni.assets.add("paper.pdf", bundle="research/reports")
asset = cogni.assets.get(result.asset_id)
```

The underlying flow for SourceAsset and DocBundle lifecycle is:

1. Register files in a bundle.
2. Start ingest from local paths, asset IDs, or bundle IDs.
3. Watch ingest progress and inspect generated documents.
4. Use stable IDs for data curation.

```bash
cogni bundle create research/reports
cogni asset add paper.pdf --bundle research/reports
cogni ingest /path/to/paper.pdf --bundle research/reports
cogni job watch <job_id>
cogni document show <document_id>
```

```bash
cogni asset delete src-... --yes
cogni cleanup blobs --dry-run
```

The platform keeps logical deletion records in metadata. Storage handles physical
file cleanup through a background job so unused blobs are removed safely.

## Deprecated / Compatibility

Technical naming and command aliases are retained for compatibility with older
automation:

- `cogni assets add` (plural) is mapped to the current flow.
- `--storage-root` remains available as an explicit advanced override.
- Direct source file references that rely on raw `source.pdf` names are not part of
  the current ingest surface.

- [Open SDK documentation](/sdk/)
- [Source repository](https://github.com/cognityx/cognityx-sdk)
