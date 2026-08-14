# Understand Cognityx configuration

Configuration answers a practical question: **what settings will this command
use?** Cognityx now provides static inspection commands that answer it without
starting the work. Static means the command reads and validates settings but
does not open Storage, create a database, start a parser, load a model, contact
a provider, train, evaluate, publish, or make a network call.

## There is no global master file

The SDK brings components together, but each domain keeps control of its own
persistent settings. In plain terms, Ingest decides how documents are read,
Storage decides where durable data goes, and Resource Context decides which
tenant, user, and project own the work. The highest-precedence file actually
loaded for one domain is called its **master configuration**.

```text
Resource Context settings ─┐
Storage settings ──────────┼─> Cogni / cogni ─> Ingest operation
Ingest settings ───────────┘
```

`cogni config show --component all` reports these owned domains separately. A
catalog path and a Jobs database path are process locations, not master files.

## Read the report

Every inspection command emits deterministic JSON with the same main ideas:

| Field | Meaning |
| --- | --- |
| `configuration_kind` | Persistent settings, a scientific workload, or composed dependency settings |
| `master_config` | The highest-precedence file actually loaded, or `built-in` |
| `config_layers` | Every file read, ordered from low to high precedence |
| `field_sources` | Where each final value came from |
| `overrides` | Only explicit environment or command values that changed a result |
| `effective` | Final values with secrets removed or represented by safe metadata |
| `valid`, `warnings`, `errors` | Whether validation succeeded and why |

Paths are normalized absolute paths. File hashes use the exact bytes read. A
file-selecting environment variable is reported as a selector; an environment
variable that changes one value is reported as an override. Parser defaults
inserted by the command-line library are not user overrides.

## Which kind of input is this?

Persistent settings may use discovery because they describe a stable local or
project environment. A scientific recipe stays explicit because discovering a
nearby file could silently run the wrong experiment. Runtime locations point
to process state. Dependency settings belong to another component. CI inputs
control automation. Immutable artifacts are evidence produced by completed
work and must never be treated as ambient settings.

| Repository | Persistent settings | Scientific or explicit input | Other classification | Static inspection in this slice |
| --- | --- | --- | --- | --- |
| `cognityx-sdk` | Layered Ingest settings | Bounded Inference selection remains explicit | Composes Storage and Resource Context; catalog and Jobs DB are runtime locations | `cogni config show|validate` |
| `cognityx-experiments` | None | Research YAML and nested component specs | Storage is dependency configuration; results destination is explicit | `cognityx-experiments config show|validate` or `cogni experiment config show|validate` |
| `cognityx-storage` | One discovered Storage TOML | None | Owner dependency used by other components | Through `cogni ... --component storage` and Python resolver |
| `cognityx-resource` | One discovered Context JSON plus field/scope overrides | None | Cross-service identity context | Through `cogni ... --component context` and Python resolver |
| `cognityx-inference` | One discovered Inference TOML | Boundary-search TOML and model revisions | Secrets-file environment value is a safe path override | `cognityx-inference config show|validate` |
| `cognityx-dataforge` | None | Required dataset build recipe | Optional Storage settings are dependency configuration; Jobs DB is runtime location | `cognityx-dataforge config show|validate` |
| `cognityx-training` | None | Required training spec, autotune plan, and evaluation request | Output directory is a runtime/publication location | `cognityx-train config show|validate` |
| `cognityx-evaluator` | None | Optional explicit judge/method file | Storage and tracking are execution dependencies | `cognityx-evaluator config show|validate` |
| `cognityx-ingest` | Owned through the SDK's layered Ingest settings | Routing plans and asset/bundle IDs remain explicit | Storage and Context are owner dependencies | Use `cogni ... --component ingest`; no new Ingest config group |
| `cognityx-jobs` | None | None | Caller-owned database location | No change; embedded repository |
| `cognityx-observability` | None | None | In-memory dependency settings supplied by callers | No change |
| `cognityx-core` | None | None | Contracts and value objects | No change |
| `cognityx/.github` | None | None | CI and reusable workflow inputs | No change |
| `cognityx.github.io` | MkDocs portal settings | None | CI assembles component sites and deploys Pages | Portal build validation |
| `cognityx-experiment-results` | None | None | Immutable evidence and publication artifacts | No change; never discovered or rewritten |

## Commands by owner

```bash
# SDK composition and compatibility view
cogni config show [--component all|ingest|storage|context]
cogni config validate [--component all|ingest|storage|context]
cogni ingest-config show
cogni ingest-config validate

# Composed Storage dependency
cognityx-experiments config show \
  [--storage-config PATH | --storage-root PATH]
cognityx-experiments config validate \
  [--storage-config PATH | --storage-root PATH]
cogni experiment config show \
  [--storage-config PATH | --storage-root PATH]
cogni experiment config validate \
  [--storage-config PATH | --storage-root PATH]

# Persistent Inference settings
cognityx-inference config show [--config PATH]
cognityx-inference config validate [--config PATH]

# Explicit scientific inputs
cognityx-dataforge config show --config PATH
cognityx-dataforge config validate --config PATH
cognityx-train config show --config PATH [supported run overrides]
cognityx-train config validate --config PATH [supported run overrides]
cognityx-evaluator config show [--judge-config PATH]
cognityx-evaluator config validate [--judge-config PATH]
```

`show` and `validate` use the same resolver as execution. `validate` returns a
nonzero process status for a missing or malformed explicitly selected file.
`show` also returns nonzero when it cannot truthfully resolve the selection.
The `cogni experiment config` forms delegate directly to Experiments and do not
load the SDK composition root.

These inspection commands keep JSON as their default. Add `--human` for a
readable view of the same secret-safe report; presentation does not resolve the
configuration a second time.

## Selection rules that remain unchanged

Storage selects one file:

```text
explicit file
> COGNITYX_STORAGE_CONFIG
> project .cognityx/storage.toml
> XDG/user storage.toml
> built-in local settings
```

Resource Context also selects one base file, then applies explicit field and
scope overrides:

```text
explicit context file
> COGNITYX_CONTEXT_FILE
> project .cognityx/context.json
> configured user context
> built-in local context
```

Inference selects one file and deliberately has no new user-level fallback:

```text
explicit --config
> COGNITYX_INFERENCE_CONFIG
> project .cognityx/inference.toml
> built-ins
```

Ingest preserves its existing multi-file merge. Later files replace individual
values from earlier files:

```text
built-ins
< XDG/user ingest.toml
< project .cognityx/ingest.toml
< COGNITYX_INGEST_CONFIG file
< explicit --ingest-config file
< parser policy/backend command overrides
```

## JSON examples

The examples below are shortened to make the selection evidence easy to see.
Each block is valid JSON; real reports include the complete secret-safe
`effective` object and all field sources.

### Built-in-only configuration

With no judge file, Evaluator truthfully reports its deterministic built-in
method:

```json
{
  "component": "evaluator",
  "configuration_kind": "scientific-workload",
  "valid": true,
  "master_config": {
    "kind": "built-in",
    "path": null,
    "selected_by": "built-in",
    "sha256": null
  },
  "config_layers": [],
  "field_sources": {},
  "overrides": [],
  "effective": {
    "deterministic_only": true,
    "judge": null
  },
  "warnings": [],
  "errors": []
}
```

### Project/default discovery

Running from a project that contains `.cognityx/inference.toml` records the
project selector. The file is not mislabelled as explicit:

```json
{
  "component": "inference",
  "configuration_kind": "persistent-component",
  "valid": true,
  "master_config": {
    "kind": "file",
    "path": "/work/demo/.cognityx/inference.toml",
    "selected_by": "project",
    "sha256": "8d4c84e64b4d46ef2758d8f5f8dd1fe193651ba655b91f0f9a9434c3d78ec180"
  },
  "config_layers": [
    {
      "path": "/work/demo/.cognityx/inference.toml",
      "selected_by": "project",
      "sha256": "8d4c84e64b4d46ef2758d8f5f8dd1fe193651ba655b91f0f9a9434c3d78ec180",
      "changed_keys": ["manager.host", "manager.port"]
    }
  ],
  "overrides": [],
  "warnings": [],
  "errors": []
}
```

### Multiple loaded Ingest layers

Ingest lists every file it read in low-to-high order. The master is the final
file layer, not the later command value override:

```json
{
  "component": "ingest",
  "configuration_kind": "persistent-component",
  "valid": true,
  "master_config": {
    "kind": "file",
    "path": "/work/demo/selected-ingest.toml",
    "selected_by": "explicit",
    "sha256": "99e49b03553b8b6a979c49e12e9572b429c23fb5ca874fafc352465b0e30c59d"
  },
  "config_layers": [
    {
      "path": "/home/user/.config/cognityx/ingest.toml",
      "selected_by": "user",
      "sha256": "203678481495554477830d58532009de3f9850b6a5bc470db3d3d6b5a78fffa6",
      "changed_keys": ["ingest.parser_policy"]
    },
    {
      "path": "/work/demo/.cognityx/ingest.toml",
      "selected_by": "project",
      "sha256": "313863ea69c34869e04fdde49f739b23b7da27df501cdbb6482797336370946b",
      "changed_keys": ["ingest.inference.enabled"]
    },
    {
      "path": "/work/demo/selected-ingest.toml",
      "selected_by": "explicit",
      "sha256": "99e49b03553b8b6a979c49e12e9572b429c23fb5ca874fafc352465b0e30c59d",
      "changed_keys": ["ingest.parser_backends"]
    }
  ],
  "overrides": [],
  "effective": {
    "parser_policy": "compare",
    "parser_backends": ["pymupdf", "basic"],
    "inference_enabled": false
  },
  "warnings": [],
  "errors": []
}
```

### Explicit file selection

A DataForge recipe is never discovered. The explicit path and exact bytes are
part of the scientific identity:

```json
{
  "component": "dataforge",
  "configuration_kind": "scientific-workload",
  "valid": true,
  "master_config": {
    "kind": "file",
    "path": "/work/research/dataforge.toml",
    "selected_by": "explicit",
    "sha256": "633501d475b92edb79e61aa5e5c363bffc0ee45fd946a9a6464de76571040de3"
  },
  "config_layers": [
    {
      "path": "/work/research/dataforge.toml",
      "selected_by": "explicit",
      "sha256": "633501d475b92edb79e61aa5e5c363bffc0ee45fd946a9a6464de76571040de3",
      "changed_keys": ["recipe", "split_seed", "generator.model"]
    }
  ],
  "overrides": [],
  "warnings": [],
  "errors": []
}
```

### Environment and command value overrides

An override appears only when the supplied value changed the resolved value:

```json
{
  "component": "training",
  "configuration_kind": "scientific-workload",
  "valid": true,
  "overrides": [
    {
      "key": "seed",
      "source": "--seed",
      "previous": 17,
      "effective": 29,
      "changed": true
    }
  ],
  "field_sources": {
    "seed": "--seed"
  },
  "effective": {
    "seed": 29
  },
  "warnings": [],
  "errors": []
}
```

Inference uses the same rule for `COGNITYX_SECRETS_FILE`; the variable changes
only the safe file path and never causes inspection to read its contents.

### Malformed selected file

An explicit broken file fails instead of falling back to a default:

```json
{
  "component": "inference",
  "configuration_kind": "persistent-component",
  "valid": false,
  "master_config": {
    "kind": "file",
    "path": "/work/demo/broken.toml",
    "selected_by": "explicit",
    "sha256": null
  },
  "config_layers": [],
  "field_sources": {},
  "overrides": [],
  "effective": {},
  "warnings": [],
  "errors": [
    {
      "code": "configuration_invalid",
      "message": "Expected a closing bracket in /work/demo/broken.toml"
    }
  ]
}
```

The real error identifies the safe path and parse problem; it does not print a
secret value. The command returns a nonzero status.

### Redacted secrets

Inference reports only whether a secrets file is configured, its normalized
path, and the fact that inspection did not read it:

```json
{
  "component": "inference",
  "configuration_kind": "persistent-component",
  "valid": true,
  "overrides": [
    {
      "key": "secrets_file",
      "source": "COGNITYX_SECRETS_FILE",
      "previous": "/secure/team.json",
      "effective": "/run/secrets/inference.json",
      "changed": true
    }
  ],
  "effective": {
    "secrets_file": {
      "configured": true,
      "path": "/run/secrets/inference.json",
      "contents_read": false
    },
    "providers": {
      "openai": {
        "api_key_env": "OPENAI_API_KEY",
        "api_key_secret": "openai_api_key"
      }
    }
  },
  "warnings": [],
  "errors": []
}
```

Credential-bearing URI parts, passwords, tokens, keys, and secret-file contents
are never part of inspection output.

## Why specialized files remain explicit

The following commands are unchanged because their files define work or
scientific identity, not ambient machine settings:

- `cognityx-boundary --config PATH` selects a hardware boundary-search recipe.
- `cognityx-autotune --config PATH` selects a training capacity search.
- `cognityx-evaluate plan|run --config PATH` selects a saved-output evaluation.
- `cognityx-track-publication ...` receives explicit publication operands.
- The legacy `llm-benchmark` compatibility command and Python package shipped
  inside `cognityx-inference` keep their existing interactive/native behavior
  for backward compatibility. They are not a separate repository or a current
  first-class platform component, and this compatibility statement does not
  define the final desired naming architecture.
- Experiments research YAML, nested component specifications, manifests,
  publication snapshots, model revisions, and result artifacts remain explicit.

This separation prevents a project or user file from silently changing a
dataset build, training run, judge method, model boundary, or research result.

## Component sources of truth

Use this page to choose the right owner, then follow its generated site for the
complete schema and operational examples:

- [SDK configuration](/sdk/configuration/)
- [Experiments commands](/experiments/cli/)
- [Storage configuration](/storage/configuration/)
- [Resource architecture and Context discovery](/resource/architecture/)
- [Inference configuration](/inference/configuration/)
- [DataForge reference](/dataforge/reference/)
- [Training configuration inspection](/training/configuration-inspection/)
- [Evaluator documentation](/evaluator/)
- [Ingest documentation](/ingest/)
