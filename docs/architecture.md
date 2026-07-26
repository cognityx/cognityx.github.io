# Documentation architecture

The public portal is a thin build and publication layer:

1. GitHub Actions checks out this repository and selected private component repositories.
2. Each component builds its own `mkdocs.yml` into an independent site directory.
3. The portal builds its landing pages.
4. The assembly script copies the component sites under `/core/`, `/inference/`, `/training/`, and `/storage/`.
5. The resulting static tree is published to GitHub Pages.

Component repositories remain the source of truth. The portal owns only shared
navigation, cross-component orientation, and assembly configuration.

## Access model

The workflow uses a read-only GitHub token stored as `COGNITYX_DOCS_READ_TOKEN`
to check out private component repositories. The public Pages deployment uses
the portal repository's standard Pages permissions.
