# Cognityx Ingest

This component turns source files into structured evidence that teams can use downstream.
It keeps a stable record of the original file (called a SourceAsset, the original
uploaded document) and then builds page-level document data from it.

It is the handoff point for DataForge:

- `cogni ingest /path/to/file.pdf` for new local files.
- `cogni ingest --asset <asset_id>` for existing SourceAsset reuse.
- `cogni ingest --bundle-id <bundle_id>` for bundle-level reruns.

The generated output includes stable document and artifact references for
inspection and reruns. Page-level evidence is retained for review and quality checks.

Deletion and cleanup:

- Deleting an ingestion unit keeps metadata visible for traceability.
- Physical file cleanup is performed by Storage, which removes unreferenced blobs in
  a background process with safety checks.

Deferred roadmap:

- Reference-only external URI ingestion is intentionally deferred.
- Fully distributed worker scheduling is intentionally deferred.

- [Open generated Ingest documentation](/ingest/)
- [Source repository (access required)](https://github.com/cognityx/cognityx-ingest)
- [Request repository access](mailto:bhujay.bhatta@yahoo.com?subject=Access%20request%20for%20cognityx%2Fcognityx-ingest)
