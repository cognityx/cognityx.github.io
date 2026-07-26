#!/usr/bin/env python3
"""Discover Cognityx repositories with MkDocs sites and clone their sources."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path
from urllib.parse import quote


def run(*args: str, capture: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        check=False,
        text=True,
        capture_output=capture,
        env=os.environ,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--organization", required=True)
    parser.add_argument("--overrides", type=Path, required=True)
    parser.add_argument("--sources-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--directory-page", type=Path, required=True)
    return parser.parse_args()


def default_component(organization: str, repository: dict[str, object]) -> dict[str, object]:
    name = str(repository["name"])
    slug = name.removeprefix("cognityx-")
    return {
        "slug": slug,
        "title": name.replace("-", " ").title(),
        "repo": f"{organization}/{name}",
        "prefix": slug,
        "summary": f"Generated documentation for {name}.",
        "contact": "bhujay.bhatta@yahoo.com",
    }


def write_directory(path: Path, components: list[dict[str, object]]) -> None:
    lines = [
        "# All components",
        "",
        "Documentation is generated from private Cognityx repositories. Source",
        "links require authorization; use the access-request link if GitHub returns",
        "a not-found page.",
        "",
    ]
    for component in components:
        repository = str(component["repo"])
        subject = quote(f"Access request for {repository}")
        lines.extend(
            [
                f"## {component['title']}",
                "",
                str(component["summary"]),
                "",
                f"- [Open documentation](/{component['prefix']}/)",
                f"- [Source repository (access required)](https://github.com/{repository})",
                f"- [Request repository access](mailto:{component['contact']}?subject={subject})",
                "",
            ]
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    overrides = {
        component["repo"].split("/", 1)[1]: component
        for component in json.loads(args.overrides.read_text(encoding="utf-8"))
    }
    listed = run(
        "gh",
        "repo",
        "list",
        args.organization,
        "--limit",
        "1000",
        "--json",
        "name,defaultBranchRef,isArchived",
        capture=True,
    )
    if listed.returncode:
        raise RuntimeError(listed.stderr.strip())

    repositories = json.loads(listed.stdout)
    args.sources_root.mkdir(parents=True, exist_ok=True)
    components: list[dict[str, object]] = []
    for repository in repositories:
        name = repository["name"]
        if repository["isArchived"] or name in {".github", "cognityx.github.io"}:
            continue
        probe = run(
            "gh",
            "api",
            "--method",
            "GET",
            f"repos/{args.organization}/{name}/contents/mkdocs.yml",
            "--silent",
            capture=True,
        )
        if probe.returncode:
            continue

        component = dict(overrides.get(name, default_component(args.organization, repository)))
        source = args.sources_root / str(component["slug"])
        if source.exists():
            shutil.rmtree(source)
        cloned = run(
            "gh",
            "repo",
            "clone",
            f"{args.organization}/{name}",
            str(source),
            "--",
            "--depth",
            "1",
        )
        if cloned.returncode:
            raise RuntimeError(f"Unable to clone {args.organization}/{name}")
        component["source"] = str(source)
        components.append(component)

    order = {name: index for index, name in enumerate(overrides)}
    components.sort(
        key=lambda item: (
            order.get(str(item["repo"]).split("/", 1)[1], len(order)),
            str(item["repo"]),
        )
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(components, indent=2) + "\n", encoding="utf-8")
    write_directory(args.directory_page, components)


if __name__ == "__main__":
    main()
