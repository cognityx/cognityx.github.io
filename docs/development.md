# Development

Install the portal documentation dependencies and build the landing site:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
mkdocs build --strict
```

The production workflow builds component sites before invoking
`scripts/build_portal.py`. To add a component, add an entry to
`components.json`, add its page to `mkdocs.yml`, and add a checkout/build step
to `.github/workflows/publish.yml`.

Keep component content in its component repository. Do not copy generated HTML
into this repository.
