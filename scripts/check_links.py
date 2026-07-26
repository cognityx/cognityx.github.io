#!/usr/bin/env python3
"""Fail when generated HTML references a missing same-origin target."""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        targets = {"a": "href", "img": "src", "link": "href", "script": "src"}
        attribute = targets.get(tag)
        if not attribute:
            return
        for name, value in attrs:
            if name == attribute and value:
                self.links.append(value)


def target_path(site: Path, page: Path, link: str) -> Path | None:
    if link.startswith(("mailto:", "tel:", "javascript:", "data:")):
        return None
    relative_page = page.relative_to(site).as_posix()
    base = f"https://cognityx.github.io/{relative_page}"
    parsed = urlparse(urljoin(base, link))
    if parsed.netloc and parsed.netloc != "cognityx.github.io":
        return None
    path = unquote(parsed.path).lstrip("/")
    target = site / path
    if parsed.path.endswith("/"):
        target /= "index.html"
    elif not target.suffix:
        target = target / "index.html" if target.is_dir() else target
    return target


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("site", type=Path)
    args = parser.parse_args()
    site = args.site.resolve()
    broken: list[str] = []
    for page in site.rglob("*.html"):
        if page.name == "404.html":
            continue
        links = LinkParser()
        links.feed(page.read_text(encoding="utf-8"))
        for link in links.links:
            target = target_path(site, page, link)
            if target is not None and not target.exists():
                broken.append(f"{page.relative_to(site)} -> {link}")
    if broken:
        raise SystemExit("Broken internal links:\n" + "\n".join(sorted(set(broken))))


if __name__ == "__main__":
    main()
