# Cognityx Ingest

Cognityx Ingest turns an original file into structured, traceable evidence. It
registers the original as a stable SourceAsset, runs document parsing, preserves
the parser's native result, and publishes document artifacts that downstream
programs can inspect without reopening the file.

## Where It Fits

```text
cogni
  -> SourceAsset / DocBundle
  -> IngestRun + Job
  -> Document
  -> Canonical Content
  -> Source Graph + Provenance Addresses
  -> DataForge
```

A SourceAsset is the stable logical record of an original file, while a
DocBundle is an optional logical grouping. An IngestRun records one execution
over one or more sources. Its Job is durable progress and cancellation history,
not document content. Each successful source result has a stable Document ID and
generated artifacts.

Use the Python SDK or `cogni` command line for normal work:

```bash
cogni ingest <path>
cogni ingest --asset <asset-id>
cogni ingest --bundle <bundle-path>
cogni job watch <job-id>
cogni document show <document-id>
cogni artifact available <document-id>
cogni artifact read <document-id> provenance
cogni provenance resolve <document-id> <address-id>
```

The generated document surface has exactly nine public artifact names:
`document`, `evidence`, `provenance`, `manifest`, `canonical-content`,
`source-graph`, `provenance-addresses`, `parser-observations`, and
`parser-fusion-decisions`. Artifact reads are authorized by Ingest; Storage owns
the physical bytes behind their logical `storage://` locations.

`document.json` is the v2 compatibility representation.
`canonical-content.json` is the current v3.2 parser-neutral source model. The
Source Graph is derived from validated canonical source facts and intentionally
contains no second copy of canonical text. It is a provenance structure, not a
semantic knowledge graph.

The run manifest hands DataForge logical references to provenance, canonical
content, the Source Graph, and provenance addresses. DataForge then owns derived
paragraph Q/A and composite Knowledge Units; Ingest does not generate a semantic
knowledge graph.

Deletion separates logical records from physical bytes. Asset and bundle
deletion is a recoverable logical change. Run and document deletion affects only
their stated generated scope. `cogni cleanup blobs` plans physical cleanup by
default, and `--yes` executes a fresh Storage-owned plan only after live-reference
and safety checks. Cleanup is explicit, not an always-running background service.

The complete schema hierarchy, important record fields, six provenance outcomes,
DataForge handoff, and delete map are maintained by Ingest:

- [Open the Ingest schema and object map](/ingest/schema-map/)
- [Open all generated Ingest documentation](/ingest/)
- [Open the SDK documentation](/sdk/)
- [Open the SDK command guide](/sdk/cli/)
- [Source repository (access required)](https://github.com/cognityx/cognityx-ingest)
- [Request repository access](mailto:bhujay.bhatta@yahoo.com?subject=Access%20request%20for%20cognityx%2Fcognityx-ingest)
