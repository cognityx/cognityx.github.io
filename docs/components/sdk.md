# Cognityx Python SDK

The Cognityx Python SDK is the normal application entry point. It provides the
`Cogni` Python composition root and the `cogni` command line, then delegates each
operation to the component that owns the behavior.

## Ingest Flow

```text
Cogni.assets / cogni asset
  -> Cogni.ingest_* / cogni ingest
  -> Ingest jobs, runs, and documents
  -> Cogni.artifacts / cogni artifact
  -> Cogni.provenance / cogni provenance
```

```python
from cognityx import Cogni

cogni = Cogni.load()
asset = cogni.assets.add("paper.pdf", bundle="research/reports")
run = cogni.ingest_asset(asset.asset_id)
document_id = run.results[0].document.document_id

names = cogni.artifacts.available(document_id)
provenance = cogni.artifacts.read(document_id, "provenance")
```

The normal CLI forms are:

```bash
cogni ingest <path>
cogni ingest --asset <asset-id>
cogni ingest --bundle <bundle-path>
cogni job watch <job-id>
cogni document show <document-id>
cogni artifact available <document-id>
cogni artifact read <document-id> provenance
cogni artifact locate <document-id> source-graph
cogni provenance resolve <document-id> <address-id>
```

The SDK validates logical artifact locations but does not replace component
authorization. Actual artifact-byte reads delegate to Ingest, and provenance
resolution inherits Source Graph and provenance-address authorization. Physical
Storage paths are never the public contract.

Use these layers in order:

- [SDK documentation](/sdk/) explains CLI and Python calls.
- [SDK command guide](/sdk/cli/) lists arguments, compatibility forms, and safe
  deletion commands.
- [Ingest schema and object map](/ingest/schema-map/) defines the nine artifact
  names, canonical records, Source Graph, provenance outcomes, and DataForge
  handoff.
- [Ingest documentation](/ingest/) provides the detailed component contracts.

`--storage-root`, plural command aliases, and ID-only `--bundle-id` remain
deprecated compatibility forms. Normal use loads Storage configuration and uses
`cogni ingest --bundle <bundle-path>`.

- [Source repository (access required)](https://github.com/cognityx/cognityx-sdk)
- [Request repository access](mailto:bhujay.bhatta@yahoo.com?subject=Access%20request%20for%20cognityx%2Fcognityx-sdk)
