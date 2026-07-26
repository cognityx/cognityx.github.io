# Documentation architecture

The public portal is a thin build and publication layer:

1. GitHub Actions enumerates repositories in the Cognityx organization.
2. Repositories containing a root `mkdocs.yml` are cloned with read-only credentials.
3. Each component builds its own configuration into an independent site directory.
4. The portal builds its landing pages and generated component directory.
5. The assembly script copies component sites under stable URL prefixes.
6. Internal links are checked before the static tree is published to GitHub Pages.

Component repositories remain the source of truth. The portal owns only shared
navigation, cross-component orientation, and assembly configuration.

## Access model

The workflow uses a read-only GitHub token stored as `COGNITYX_DOCS_READ_TOKEN`
to check out private component repositories. The public Pages deployment uses
the portal repository's standard Pages permissions.

Current component repositories dispatch an immediate rebuild after each push
to their default branch. A two-hour scheduled discovery run includes future
Cognityx repositories automatically once they provide a root `mkdocs.yml`.
