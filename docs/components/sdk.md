# Cognityx Python SDK

The primary application-facing Python SDK for Cognityx. It provides the thin
`Cogni` facade over the independently versioned Resource, Storage, and Ingest
repositories, plus the unified `cogni` CLI.

```python
from cognityx import Cogni

cogni = Cogni.load()
result = cogni.assets.add("paper.pdf", bundle="phd/rag")
asset = cogni.assets.get(result.asset_id)
```

The SDK supports complete SourceAsset and DocBundle lifecycle operations,
including logical deletion and deleted-resource inspection. Physical Blob
cleanup remains separate, dry-run-first, and reference-safe.

```bash
cogni assets add paper.pdf --bundle phd/rag
cogni assets delete src-... --yes
cogni cleanup blobs --dry-run
```

- [Open SDK documentation](https://github.com/cognityx/cognityx-sdk)
- [Source repository](https://github.com/cognityx/cognityx-sdk)
