# Cognityx Documentation Portal

Public documentation assembly site for the Cognityx platform.

This repository owns the portal landing pages, shared navigation, and GitHub
Pages workflow. Component repositories remain the source of truth for their
own documentation and are built into stable paths under `/core/`,
`/inference/`, `/training/`, and `/storage/`.

## Local build

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
mkdocs build --strict
```

The publishing workflow requires a read token named
`COGNITYX_DOCS_READ_TOKEN` with access to the private component repositories.
