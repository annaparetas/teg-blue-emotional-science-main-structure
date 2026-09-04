#!/usr/bin/env python3
"""Check local HTML and Markdown links without requiring a web server."""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
PRESERVED_FLAT_SITE = ROOT / "archive" / "pre-numbered-main-structure-2026-09-04"
TEXT_SUFFIXES = {".html", ".md"}
EXTERNAL_SCHEMES = {"http", "https", "mailto", "tel", "data", "javascript"}


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []
        self.anchors: set[str] = set()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.anchors.add(values["id"] or "")
        if values.get("name"):
            self.anchors.add(values["name"] or "")
        for attribute in ("href", "src"):
            if values.get(attribute):
                self.links.append(values[attribute] or "")


def html_data(path: Path) -> tuple[list[str], set[str]]:
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser.links, parser.anchors


def markdown_links(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    return re.findall(r"\]\(([^\s)]+)(?:\s+['\"].*?['\"])?\)", text)


def main() -> int:
    html_cache: dict[Path, set[str]] = {}
    problems: list[str] = []

    files = sorted(
        path for path in ROOT.rglob("*")
        if path.is_file()
        and path.suffix.lower() in TEXT_SUFFIXES
        and ".git" not in path.parts
        and PRESERVED_FLAT_SITE not in path.parents
    )

    for source in files:
        if source.suffix.lower() == ".html":
            links, anchors = html_data(source)
            html_cache[source.resolve()] = anchors
        else:
            links = markdown_links(source)

        for value in links:
            parsed = urlsplit(value)
            if parsed.scheme.lower() in EXTERNAL_SCHEMES or parsed.netloc:
                continue

            if parsed.path:
                target = (source.parent / unquote(parsed.path)).resolve()
            else:
                target = source.resolve()

            if not target.exists():
                problems.append(f"{source.relative_to(ROOT)} -> {value} [missing file]")
                continue

            if parsed.fragment and target.suffix.lower() == ".html":
                anchors = html_cache.get(target)
                if anchors is None:
                    _, anchors = html_data(target)
                    html_cache[target] = anchors
                if unquote(parsed.fragment) not in anchors:
                    problems.append(f"{source.relative_to(ROOT)} -> {value} [missing anchor]")

    if problems:
        print(f"Found {len(problems)} broken local links:")
        for problem in sorted(set(problems)):
            print(f"- {problem}")
        return 1

    print(f"Checked {len(files)} HTML and Markdown files: all local links resolve.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
