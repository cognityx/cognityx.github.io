# Cognityx Python SDK

This is the preferred entry point for day-to-day work.
Use the `cogni` CLI for source registration, ingest, job tracking, artifact
inspection, and safe cleanup.

```python
from cognityx import Cogni

cogni = Cogni.load()
asset = cogni.assets.add("paper.pdf", bundle="research/reports")
```

## Output and handoff rules

Use storage IDs and `storage://` URIs as the public contract.

```text
storage://<profile>/artifacts/ingest/documents/<document-id>/...
storage://<profile>/artifacts/ingest/runs/<run-id>/manifest.json
```

Do not use OS paths as API inputs or outputs.
Physical paths are only for backend operators when local inspection is enabled.

For DataForge, keep at least:

- `run_id`
- `job_id`
- `bundle_id`
- `asset_id`
- `document_id`
- provenance URI
- source `sha256`
- source-anchor IDs
- page-level evidence

## CLI output and handoff guide

### 1) `cogni bundle create <bundle-name>`

What it creates or changes
- Creates or finds a `DocBundle` and binds future source files.

Important IDs returned
- `bundle_id`

Generated artifacts
- Bundle manifest metadata.

Storage role and logical URI
- Stored under Storage metadata so bundle metadata is preserved independently.
- Example: `storage://<profile>/artifacts/ingest/bundles/<bundle_id>/manifest.json`

Result type
- Metadata only.

Using the result
- Pass the `bundle_id` into `cogni asset add --bundle`.
- Keep the `bundle_id` with run and document records.

Deletion impact
- Deleting a bundle stops direct reuse from that active pointer.
- It does not remove already processed documents or artifacts.

### 2) `cogni asset add <path> --bundle <bundle_name_or_id>`

What it creates or changes
- Registers a SourceAsset.
- Calculates SHA-256, writes source blob if it is not already present.

Important IDs returned
- `asset_id`
- `bundle_id`
- source `sha256`

Generated artifacts
- `storage://<profile>/artifacts/ingest/assets/<asset_id>/source`
- optional source metadata for checksum and size

Storage role and logical URI
- Storage owns CAS, deduplication, and blob placement.
- Source storage is accessed via canonical Storage URIs.

Result type
- Raw source plus metadata.

Using the result
- Re-run ingest from this source with `cogni ingest --asset <asset_id>`.
- Use returned `asset_id` for idempotent retries and bundle-level audits.

Deletion impact
- Logical deletion keeps history and reuse metadata.
- Physical blob removal happens only by background cleanup when no references remain.

### 3) `cogni ingest <local-path> [--bundle <bundle-name-or-id>]`

This is the normal ingest entry point for local files.

What it creates or changes
- Creates a new ingest run and starts a durable job.
- May create or reuse a SourceAsset based on hash.
- Generates document-level evidence and manifests.

Important IDs returned
- `run_id`
- `job_id`
- `bundle_id`
- `asset_id`
- `document_id`

Generated artifacts
- `storage://<profile>/artifacts/ingest/runs/<run_id>/manifest.json`
- `storage://<profile>/artifacts/ingest/documents/<document_id>/document.json`
- `storage://<profile>/artifacts/ingest/documents/<document_id>/evidence.jsonl`
- `storage://<profile>/artifacts/ingest/documents/<document_id>/provenance.json`
- `storage://<profile>/artifacts/ingest/documents/<document_id>/manifest.json`
- optional `storage://<profile>/artifacts/ingest/runs/<run_id>/parser/<backend>.json`

Storage role and logical URI
- Storage writes all raw and generated artifacts as immutable records.

Result type
- Raw source (via SourceAsset), generated documents, and immutable manifests.

Using the result
- Monitor with `cogni job status <job_id>` and `cogni run show <run_id>`.
- Pass `document_id` and artifact URIs to DataForge.

This command returns at least:

```text
run_id
job_id
bundle_id
asset_id
document_id
artifact_uris
provenance_uri
page_count
failure_details
```

Deletion impact
- Deleting related records does not delete immutable manifests immediately.
- Physical artifacts are removed only through safe background cleanup after reference checks.

### 4) `cogni ingest --asset <asset_id>`

What it creates or changes
- Starts a new ingest run from an existing SourceAsset.
- Reuses source blob and skips re-upload.

Important IDs returned
- New `run_id`
- New `job_id`
- Existing `asset_id`

Generated artifacts
- Same set as local ingest listed in command 3.

Storage role and logical URI
- Reuses Storage CAS source and writes new run artifacts.

Result type
- Generated documents and manifests.

Using the result
- Use the returned `run_id`, `document_id`, and artifact URIs for same-stage DataForge handoff.

Deletion impact
- SourceAsset deletion does not touch this run until background checks are satisfied.

### 5) `cogni ingest --bundle-id <bundle_id>`

What it creates or changes
- Starts a run using a whole bundle source set.
- Applies SourceAsset dedup and parser runs consistently for selected inputs.

Important IDs returned
- New `run_id`
- New `job_id`
- Bundle context from `bundle_id`

Generated artifacts
- Run and document artifacts from command 3.

Storage role and logical URI
- Reads bundle and assets from Storage metadata, writes new run output in Storage.

Result type
- Generated documents and manifests.

Using the result
- Useful for rerun and backfill jobs with stable source references.

Deletion impact
- Bundle cleanup rules apply; artifacts stay discoverable for audit.

### 6) `cogni job status <job_id>`

What it creates or changes
- No mutation.
- Returns current job state from the durable job index.

Important IDs returned
- `job_id`
- state timeline summary

Generated artifacts
- None.

Storage role and logical URI
- Reads from Storage-aware job index.

Result type
- Metadata only.

Using the result
- Poll or gate automation until `completed` or `failed`.
- For full event sequence, move to `cogni job watch <job_id>`.

Deletion impact
- No deletion effect; read-only.

### 7) `cogni run show <run_id>`

What it creates or changes
- No mutation.
- Expands immutable run details and references.

Important IDs returned
- `run_id`
- `job_id`
- `bundle_id`
- `asset_id`
- `document_id`
- failure summary

Generated artifacts
- `storage://<profile>/artifacts/ingest/runs/<run_id>/manifest.json`

Storage role and logical URI
- Storage + Jobs durable lifecycle record.

Result type
- Immutable metadata plus run manifest linkage.

Using the result
- Use as the canonical run handoff audit before DataForge starts.
- Pair with `cogni artifact read <document-id> provenance` for source provenance.

Deletion impact
- Logical delete preserves manifest for audit.
- Physical blob cleanup still needs background policy.

### 8) `cogni document show <document_id>`

What it creates or changes
- No mutation.
- Resolves document record and latest artifact references.

Important IDs returned
- `document_id`
- linked `asset_id`
- current artifact IDs and versions

Generated artifacts
- Reports pointers to `document.json`, `evidence.jsonl`, `provenance.json`, `manifest.json`.

Storage role and logical URI
- Storage artifact index.

Result type
- Metadata with artifact references.

Using the result
- Inspect what was generated before sending to DataForge.
- Confirm page evidence presence and provenance ID continuity.

Deletion impact
- Deletion status changes workflow exposure but preserves historical references.

### 9) `cogni artifact read <document-id> <artifact-short-name>`

Examples:

```bash
cogni artifact read <document-id> provenance
cogni artifact read <document-id> document
cogni artifact read <document-id> evidence
cogni artifact read <document-id> manifest
```

What it creates or changes
- No mutation.
- Reads a concrete artifact from Storage.

Important IDs returned
- `document_id`
- requested `artifact` name and resolved storage URI.

Generated artifacts
- One requested artifact payload:
  - `document.json`
  - `evidence.jsonl`
  - `provenance.json`
  - `manifest.json`
  - optional `parser/<backend>.json`

Storage role and logical URI
- Reads immutable artifact blob from Storage.

Result type
- Generated content, metadata, and evidence depending on artifact selected.

Using the result
- `provenance` output is the primary DataForge handoff.
- DataForge should not reopen the raw source PDF to reconstruct page or section provenance.
- Keep `document_id`, `asset_id`, source `sha256`, and source-anchor IDs in any
  downstream knowledge unit or training record.

Deletion impact
- Metadata views remain accessible until safe cleanup policy removes blobs.

### 10) `cogni document delete <document_id>`

What it creates or changes
- Marks the document as deleted (logical).

Important IDs returned
- `document_id`

Generated artifacts
- No new artifacts.

Storage role and logical URI
- Storage metadata deletion mark.

Result type
- Metadata state only.

Using the result
- Use `cogni document show` and `cogni run show` to inspect remaining provenance.

Deletion impact
- Does not immediately remove source or generated blobs.
- Safe cleanup may remove physical blobs later if no reference remains.

### 11) `cogni run delete <run_id>`

What it creates or changes
- Marks an ingest run as deleted (logical).

Important IDs returned
- `run_id`

Generated artifacts
- No new artifacts.

Storage role and logical URI
- Storage run metadata record is updated.

Result type
- Metadata state only.

Using the result
- Validate completion with `cogni run show <run_id>` before cleanup expectations.

Deletion impact
- Keeps immutable run manifest for audit.
- Physical run artifacts are removed only by background cleanup policy.

### 12) `cogni cleanup blobs`

What it creates or changes
- Runs or reports Storage-safe cleanup.

Important IDs returned
- Optional cleanup session ID in logs.

Generated artifacts
- None for user consumption.

Storage role and logical URI
- Storage-managed physical artifact lifecycle.

Result type
- Operational status and summary.

Using the result
- Use `--dry-run` before destructive mode.
- Run when logical deletes are frequent or storage usage grows.

Deletion impact
- Removes only physically unreferenced CAS blobs.
- Preserves any blob still referenced by run, document, or asset state.

## Generated outputs and what each one means

- `document.json`: canonical pages, blocks, sections, objects, and relations.
- `evidence.jsonl`: exact page and source evidence rows.
- `provenance.json`: complete DataForge-ready provenance handoff.
- `manifest.json`: stable references to all related document artifacts.
- `parser/<backend>.json`: optional backend-specific parser audit output.
- `ingest/runs/<run-id>/manifest.json`: immutable run manifest with inputs, outputs, failures, and timings.

## End-to-end practical handoff

```text
source file
  → cogni asset add /path/research/paper.pdf --bundle research/reports
     returns bundle_id, asset_id, sha256
  → cogni ingest --asset <asset_id>
     returns run_id, job_id, bundle_id, asset_id, document_id,
     artifact URIs, provenance URI, page count, failure details
  → cogni artifact read <document_id> provenance
     returns storage://<profile>/artifacts/ingest/documents/<document_id>/provenance.json
  → DataForge consumes run_id and provenance/document references for dataset build
```

For DataForge input, the stable handoff values are:

- `storage://<profile>/artifacts/ingest/runs/<run_id>/manifest.json`
- `storage://<profile>/artifacts/ingest/documents/<document_id>/provenance.json`
- `storage://<profile>/artifacts/ingest/documents/<document_id>/document.json`
- `storage://<profile>/artifacts/ingest/documents/<document_id>/evidence.jsonl`

## Deprecated / Compatibility

Compatibility remains available for migration, but new operators should use the flow above.

- `cogni assets add` (plural) is mapped to the current flow.
- `--storage-root` is retained as an explicit advanced override only.
- Raw source path references are not part of the normal application contract.

- [Open SDK documentation](/sdk/)
- [Source repository](https://github.com/cognityx/cognityx-sdk)
