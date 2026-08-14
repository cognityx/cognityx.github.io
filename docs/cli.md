# Command-line output and configuration map

Use these commands when you need to answer “what will Cognityx use?” before you
start work, or when you need to choose between stable machine output and a
readable terminal view. Configuration commands return a nonzero status when an
explicitly selected file is missing, malformed, or invalid.

```text
settings or scientific recipe
  -> pure owner resolver
  -> secret-safe JSON report
  -> optional later execution command
```

The inspection step stops at the report. It does not create a parser, Storage
runtime, Jobs database, dataset, model, provider client, tracker, output
directory, publication, or research result.

## Stable machine output and optional readable output

For the structured command families changed in this rollout, JSON remains the
default and first-class interface for scripts. Add `--human` only when a person
wants to read the same result as labelled text. Cognityx does not switch output
because a terminal is attached; this is technically called avoiding automatic
TTY detection.

The readable view is a presentation of the same already-created and
already-sanitized result. Rendering it does not repeat a domain operation,
resolve configuration again, open another Storage object, make another network
or provider request, construct a model, or inspect credentials. It keeps full
IDs, hashes, paths, logical `storage://` addresses, statuses, and safe error
categories without terminal-width shortening. Diagnostics remain on standard
error (`stderr`), while successful results remain on standard output
(`stdout`). Exit codes, confirmations, authorization checks, and mutations are
unchanged.

Streaming commands also keep their established machine stream by default. A
requested human stream renders and flushes each event as it arrives without
changing ordering, sequence numbers, or replay cursors.

Some specialist commands already had a different deliberate presentation
contract. Those contracts remain authoritative: Inference model/discovery
commands keep `--format table|detail|json`, and a full Training run keeps its
existing `--output-format human|json`. JSON remains explicitly available for
machine consumers on those surfaces.

## Delivered command and exception matrix

| Entry point | Readable coverage delivered | Intentionally unchanged |
| --- | --- | --- |
| `cogni` | Eligible finite Storage, asset, bundle, ingest, configuration, job, run, document, artifact, provenance, cleanup, description, and experiment results; `job watch --human` streams readable events | Experiments Mermaid `show-plan` and Markdown `research-summary` remain native text |
| `cognityx-ingest` | Compatibility ingest; asset and bundle operations; job, document, run, artifact, and cleanup results; `jobs events --follow --human` | Existing migration warnings, partial-failure diagnostics, confirmations, aliases, and default JSON/follow streams |
| `cognityx-experiments` | `config show|validate`, `validate`, `plan`, `run`, `preflight`, `status`, and structured `paper-material` | Mermaid `show-plan` and Markdown `research-summary` |
| `cognityx-dataforge` | Configuration, build result, dataset inspection, job show/watch/cancel, evaluation-set operations, and research-package operations | `dataset export` stays silent because the requested file is the result |
| `cognityx-evaluator` | `config show|validate` and completed `evaluate pair` results | Parser and domain failures keep their established channels and exit codes |
| `cognityx-inference` | Configuration reports, finite server status, readable server-watch events, and provider list/status/models/capabilities/test/setup results | `serve`, `manager serve`, interactive `chat`, and streamed inference tokens; existing model/discovery/certified-profile `--format` behavior |
| `cognityx-boundary` | Finite `--plan --human` review output | No execution surface was added; non-plan use remains rejected |
| `cognityx-train` | Static `config show|validate`; `--human` is an explicit alias for the full run’s existing human format | Full-run default and `--output-format human|json`; `cognityx-autotune` progress controller |
| `cognityx-evaluate` | Finite `plan`, `run`, `resume`, and `show` results | Evaluation recipes and stored manifest inputs remain explicit |
| `cognityx-track-publication` | One finite final tracking result | Storage reads and tracker writes are not repeated for presentation |

Native Mermaid, Markdown, interactive, silent, service-process, progress, and
token-stream outputs are not converted into tables merely because `--human`
exists elsewhere.

### Legacy compatibility interfaces

`llm-benchmark` is a legacy compatibility console entry point and Python
package shipped inside `cognityx-inference`. It is not a separate Cognityx
repository or a current first-class platform component. It remains unchanged in
this rollout because its output is interactive and native, and existing users
depend on its backward-compatible behavior. This describes the current
compatibility obligation; it does not make `llm-benchmark` the final desired
naming architecture.

## Copy-paste examples

Omit `--human` for the stable machine result; add it for the readable view:

```bash
cogni config show
cogni config show --human

cogni experiment config show
cogni experiment config show --human

cognityx-dataforge config show --config recipe.toml
cognityx-dataforge config show --config recipe.toml --human

cognityx-inference server status
cognityx-inference server status --human
```

The DataForge file in this example is a required scientific recipe. It is not a
persistent global configuration file and is never discovered implicitly.

## Command ownership and façades

`cogni experiment config show|validate` is available and delegates directly to
Cognityx Experiments. It does not copy the Experiments resolver or initialize
the broader SDK runtime merely to inspect configuration.

DataForge, Training, Evaluator, and Inference remain specialist component CLIs.
There is no `cogni dataforge`, `cogni train`, `cogni evaluator`, or `cogni
inference` command. Storage and Resource configuration inspection stays on the
existing `cogni config --component storage|context` surface. Storage, Resource,
Jobs, Observability, and Core do not gain invented standalone executables.

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

The same owner-controlled inspection is available through the bounded SDK
façade:

```bash
cogni experiment config show
cogni experiment config validate --storage-config storage.toml
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

Do not scrape human text. The default JSON report contains normalized paths,
exact-byte hashes, source labels, actual overrides, final secret-safe values,
warnings, and errors. See [Understand Cognityx configuration](configuration.md)
for the full field guide and examples.
