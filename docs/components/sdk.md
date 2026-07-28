# Cognityx Python SDK

The primary application-facing Python SDK for Cognityx. It provides the thin
`Cogni` facade over the independently versioned Resource, Storage, and Ingest
repositories.

```python
from cognityx import Cogni

cogni = Cogni.load()
result = cogni.assets.add("paper.pdf", bundle="phd/rag")
asset = cogni.assets.get(result.asset_id)
```

- [Open SDK documentation](https://github.com/cognityx/cognityx-sdk)
- [Source repository](https://github.com/cognityx/cognityx-sdk)
