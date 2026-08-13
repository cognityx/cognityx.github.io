# Configuration command-line map

Use these commands when you need to answer “what will Cognityx use?” before you
start work. They print JSON to standard output and return a nonzero status when
an explicitly selected file is missing, malformed, or invalid.

```text
settings or scientific recipe
  -> pure owner resolver
  -> secret-safe JSON report
  -> optional later execution command
```

The inspection step stops at the report. It does not create a parser, Storage
runtime, Jobs database, dataset, model, provider client, tracker, output
directory, publication, or research result.

## SDK composition

```bash
cogni config show --component all
cogni config validate --component all
```

Choose one owned section when automation needs a bounded report:

```bash
cogni config show --component ingest
cogni config show --component storage
cogni config show --component context
cogni config validate --component ingest --ingest-config PATH
```

`all` is a composition report, not a global master. Ingest, Storage, and
Resource Context each retain their own master selection. Catalog and Jobs
database paths appear as runtime selections.

The existing Ingest-only interface remains available:

```bash
cogni ingest-config show
cogni ingest-config validate
```

New automation should prefer `cogni config`. Both forms use the same Ingest
resolver. `--ingest-config PATH` is the highest file layer; parser policy and
backend arguments remain final value overrides. An explicit
`--inference-config PATH` is parsed and hashed as a bounded runtime selection.
Inspection does not construct an Inference client.

The SDK's ordinary operational commands are unchanged. See the generated
[SDK command guide](/sdk/cli/) for asset, bundle, ingest, job, run, document,
artifact, provenance, cleanup, Storage location, and experiment commands.

## Experiments

Experiments has no persistent settings file. Its config command explains the
Storage dependency shared by `run`, `preflight`, and `status`:

```bash
cognityx-experiments config show
cognityx-experiments config validate --storage-config storage.toml
cognityx-experiments config show --storage-root experiment-storage
```

`--storage-config` and the compatibility/testing `--storage-root` are mutually
exclusive. With neither, normal Storage discovery runs. Only when discovery
reaches built-in defaults does Experiments keep its historical local
`experiment-storage` root.

Research YAML and the results repository stay explicit:

```bash
cognityx-experiments preflight research.yaml --results-repo PATH
cognityx-experiments run research.yaml --results-repo PATH
cognityx-experiments status <execution-id>
```

The mirrored `cogni experiment ...` commands follow the same selection and no
longer force `experiment-storage` when a real Storage configuration was found.

## Inference

```bash
cognityx-inference config show
cognityx-inference config validate
cognityx-inference config show --config .cognityx/inference.toml
cognityx-inference config validate --config .cognityx/inference.toml
```

The config branch runs before vLLM, the web server, provider authentication,
manager/service creation, model loading, or Storage setup. It may report safe
metadata for `COGNITYX_SECRETS_FILE`, but it does not read that file or contact
a provider. [Inference configuration details](/inference/configuration/)
describe the project and environment selectors.

## DataForge

```bash
cognityx-dataforge config show --config dataforge.toml
cognityx-dataforge config validate --config dataforge.toml
```

The DataForge file defines a dataset build and contributes to its identity, so
`--config` remains required. Inspection stops before Storage, Jobs, Inference,
dataset construction, or manifest publication. The existing build syntax is
unchanged:

```bash
cognityx-dataforge build --config dataforge.toml
```

See the [DataForge reference](/dataforge/reference/).

## Training

```bash
cognityx-train config show --config training.toml
cognityx-train config validate --config training.toml
cognityx-train config show --config training.toml --seed 29
```

Supported run overrides can follow the static command. Only a supplied value
that changes the resolved spec appears under `overrides`. Inspection exits
before dataset reads, tokenizer or Transformers imports, CUDA checks, model
loading, Storage, training, tracking, publication, or output-directory
creation. The established run remains:

```bash
cognityx-train --config training.toml
```

Autotune and saved-output evaluation keep their explicit files. See
[Training configuration inspection](/training/configuration-inspection/).

## Evaluator

```bash
cognityx-evaluator config show
cognityx-evaluator config validate
cognityx-evaluator config show --judge-config judge.toml
cognityx-evaluator config validate --judge-config judge.toml
```

No file means the built-in deterministic-only method. A judge file defines the
scientific scoring method, so it is optional but always explicit. Inspection
stops before Storage reads, pair-manifest loading, judge/provider calls,
tracking, or publication. See the [Evaluator documentation](/evaluator/).

## Owner APIs without standalone executables

Storage and Resource do not gain new executables. Their diagnostics are exposed
through the SDK because the SDK is the normal application entry point:

```bash
cogni config show --component storage
cogni config validate --component storage
cogni config show --component context
cogni config validate --component context
```

The owner-level Python resolvers are `resolve_storage_config(...)` and
`resolve_resource_context(...)`. They do not open stored objects or create
execution IDs.

The compatibility-only `cognityx-ingest` executable also gains no config group.
Normal parser/Ingest settings belong to the SDK surface:

```bash
cogni config show --component ingest
```

## Automation pattern

Capture standard output and check the process status:

```bash
cogni config validate --component all > effective-config.json
cognityx-inference config validate --config inference.toml \
  > effective-inference.json
```

Do not scrape human log text. The JSON report contains normalized paths,
exact-byte hashes, source labels, actual overrides, final secret-safe values,
warnings, and errors. See [Understand Cognityx configuration](configuration.md)
for the full field guide and examples.
