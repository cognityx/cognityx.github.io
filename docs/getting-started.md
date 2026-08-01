# Getting started

Start with the component that matches the work you need to do. The component
pages link to generated documentation. Private source links are available for
authorized collaborators, with an email link for requesting access.

A normal workday starts here:

Put local files into Cognityx, run ingest, then let DataForge prepare training data.

1. Add a source file with `cogni`.
2. Track ingest run progress.
3. Inspect generated documents and artifacts.
4. Use that evidence in DataForge.

For local development, clone the relevant repository and follow its own README
and development instructions. The portal is an assembly layer; it does not
replace component-specific setup or release processes.

## Minimal working command flow

```bash
cogni ingest /path/to/paper.pdf
cogni job status <job_id>
cogni job watch <job_id>
cogni job cancel <job_id>
cogni document show <document_id>
```

If you already have IDs from earlier steps:

```bash
cogni ingest --asset <asset_id>
cogni ingest --bundle-id <bundle_id>
```

For bundle-level grouping:

```bash
cogni bundle create research/reports
cogni bundle ls
cogni ingest /path/to/paper.pdf --bundle research/reports
```

For background cleanup and deletion behavior:

- Deleting a bundle or asset keeps historical identifiers and references visible.
- Storage removes physical files with a safety check and auto-clean job that runs in the background.

Roadmap and intentionally deferred work:

- Reference-only external URI ingestion.
- True distributed workers and multi-host ingest execution.
- Advanced cross-service scheduler optimization.

## Documentation links

- [Core](components/core.md)
- [Inference](components/inference.md)
- [Training](components/training.md)
- [Storage](components/storage.md)
- [Jobs](components/jobs.md)
- [Ingest](components/ingest.md)
- [DataForge](components/dataforge.md)
- [Resource](components/resource.md)
- [Python SDK](components/sdk.md)
- [All discovered components](components/discovered.md)
