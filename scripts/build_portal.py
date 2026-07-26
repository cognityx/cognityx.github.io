#!/usr/bin/env python3
"""Assemble the portal site and independently built component sites."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--portal-site", type=Path, required=True)
    parser.add_argument("--components-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, default=Path("components.json"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
    if args.output.exists():
        shutil.rmtree(args.output)
    shutil.copytree(args.portal_site, args.output)

    for component in manifest:
        source = args.components_root / component["slug"]
        if not source.is_dir():
            if component.get("optional"):
                continue
            raise FileNotFoundError(f"Missing required component site: {source}")
        destination = args.output / component["prefix"]
        shutil.copytree(source, destination)

    (args.output / ".nojekyll").touch()


if __name__ == "__main__":
    main()
