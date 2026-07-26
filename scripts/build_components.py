#!/usr/bin/env python3
"""Build every discovered component using its own MkDocs configuration."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    components = json.loads(args.manifest.read_text(encoding="utf-8"))
    output_root = args.output_root.resolve()
    for component in components:
        source = Path(component["source"]).resolve()
        subprocess.run(
            [
                sys.executable,
                "-m",
                "mkdocs",
                "build",
                "--strict",
                "--config-file",
                str(source / "mkdocs.yml"),
                "--site-dir",
                str(output_root / component["slug"]),
            ],
            check=True,
        )


if __name__ == "__main__":
    main()
