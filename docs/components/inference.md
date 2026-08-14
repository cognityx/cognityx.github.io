# Cognityx Inference

Inference serving and model lifecycle capabilities for the platform.

- [Open generated Inference documentation](/inference/)
- [Source repository](https://github.com/cognityx/cognityx-inference)
- [Request repository access](mailto:bhujay.bhatta@yahoo.com?subject=Access%20request%20for%20cognityx%2Fcognityx-inference)

The legacy `llm-benchmark` console entry point and Python package are shipped
inside this repository as compatibility interfaces. They are not a separate
Cognityx repository or a current first-class platform component. They remain
unchanged in this rollout because their output is interactive and native, and
existing users depend on backward-compatible behavior. This compatibility
status does not define the final desired naming architecture.

Finite configuration, server-status, server-watch, and provider results now
have explicit readable forms where documented. Existing model, discovery, and
certified-profile commands retain `--format table|detail|json`. Service
processes, interactive chat, token streams, and the legacy compatibility
console remain native and are not converted by the new presentation option.
