#!/usr/bin/env python3
"""Preview the canonical site and its sibling Development Engine on one origin."""
from __future__ import annotations
import argparse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

SITE = Path(__file__).resolve().parents[1]
ENGINE = SITE.parent / "inner-compass-nervous-system-organization-gradient"

class Handler(SimpleHTTPRequestHandler):
    def translate_path(self, path: str) -> str:
        parts = unquote(urlsplit(path).path).lstrip("/").split("/")
        root = SITE
        if parts[0] in {SITE.name, ENGINE.name}:
            root = SITE if parts.pop(0) == SITE.name else ENGINE
        target = root.joinpath(*parts).resolve()
        if not target.is_relative_to(root.resolve()) or ".git" in parts:
            return str(SITE / ".unavailable-preview-path")
        return str(root.joinpath(*parts))

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--host", default="127.0.0.1")
    args = parser.parse_args()
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"Site: http://{args.host}:{args.port}/", flush=True)
    print(f"Engine: http://{args.host}:{args.port}/{ENGINE.name}/", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

if __name__ == "__main__":
    main()
