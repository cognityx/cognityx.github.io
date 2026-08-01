# Cognityx DataForge

DataForge consumes the outputs from ingest and prepares training and evaluation data.
Teams receive stable identifiers for documents and artifacts so they can build
datasets without worrying about storage internals.

After an ingest run finishes:

- Use the document and artifact IDs from the run output.
- Inspect page-level evidence inside the dataset material.
- Move directly into training or evaluation workflows.

DataForge avoids technical setup for storage locations, and uses the same
identifier-based handoff used by ingest jobs.

Preferred ingest handoff for DataForge:

- Start from `document.json`, `evidence.jsonl`, and `provenance.json` URIs.
- Use `provenance.json` as the canonical provenance contract.
- Do not reopen the raw source PDF to reconstruct section, page, or anchor provenance.

- [DataForge documentation](/dataforge/)
- [Source repository](https://github.com/cognityx/cognityx-dataforge)
