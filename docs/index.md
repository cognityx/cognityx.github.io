<div class="portal-hero" markdown>

# Cognityx Documentation

Build capable AI systems by following a clear flow from source files to model-ready datasets.

[Explore the platform](components/index.md){ .md-button .md-button--primary }
[Get started](getting-started.md){ .md-button }

</div>

## One platform, independent components

Each Cognityx component keeps its own repository, release cadence, tests, and
MkDocs configuration. This portal provides one public entry point and assembles
those component sites without copying their source documentation.

In plain terms, you take files, turn them into document evidence, then pass that
ready evidence forward to data curation and learning workflows. We call those
stable output IDs "manifests" in technical docs later, but you do not need that
term to use the workflow.

Typical platform flow:

- Start with files in `cogni`, which creates SourceAssets and runs ingest jobs.
- Review generated document evidence and artifacts.
- Feed curated pages to DataForge.
- Move curated sets to training and inference evaluation.

## Platform areas

| Area | Purpose |
| --- | --- |
| [Core](components/core.md) | Shared contracts and backend integration boundaries |
| [Inference](components/inference.md) | Model serving and inference operations |
| [Training](components/training.md) | Reproducible training and evaluation workflows |
| [Storage](components/storage.md) | Logical storage operations independent of the backend |
| [Jobs](components/jobs.md) | Durable background jobs and replayable progress events |
| [DataForge](components/dataforge.md) | Turns document evidence into datasets for training and evaluation |
| [Ingest](components/ingest.md) | Canonical PDF ingestion with source and page provenance |
| [Resource](components/resource.md) | Shared resource Context and cross-service reference values |
| [Python SDK](components/sdk.md) | `Cogni` Python facade, unified `cogni` CLI, lifecycle operations, and safe Blob cleanup |
