# Cognityx Experiments

Cognityx Experiments turns a written research question into a checked sequence
of work. It freezes the question, treatments, measures, seeds, and stopping rule
before results are seen, then calls DataForge, Training, Inference, and
Evaluator through their public boundaries.

## Where it fits

```text
research YAML
  -> Experiments plan and preflight
  -> DataForge dataset
  -> Training candidate
  -> Inference paired outputs
  -> Evaluator scores
  -> immutable findings and research journal
```

The written research plan is technically called a scientific workload
specification. It remains an explicit command argument so a nearby file cannot
silently change which experiment runs. Experiments has no persistent settings
file of its own. Its `config show` and `config validate` commands explain the
Storage dependency used for the execution ledger.

```bash
cognityx-experiments config show
cognityx-experiments config validate --storage-config storage.toml
cognityx-experiments preflight research.yaml --results-repo PATH
cognityx-experiments run research.yaml --results-repo PATH
cognityx-experiments status <execution-id>
```

- [Open generated Experiments documentation](/experiments/)
- [Open the configuration and CLI map](../configuration.md)
- [Source repository (access required)](https://github.com/cognityx/cognityx-experiments)
- [Request repository access](mailto:bhujay.bhatta@yahoo.com?subject=Access%20request%20for%20cognityx%2Fcognityx-experiments)
