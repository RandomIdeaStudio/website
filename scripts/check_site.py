"""Checks the static website before it is published.

Fails when:
- a required file is missing,
- a page loads anything from another server (scripts, styles, fonts, images, frames),
- a page has a script at all (the site is meant to have none),
- a link to a file or an anchor on this site points nowhere,
- a PLACEHOLDER is left in a published file.

Standard library only. Run from the repository root: python scripts/check_site.py
"""
from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ["index.html", "privacy.html", "second-shift-manager-privacy.html"]
REQUIRED = PAGES + ["style.css", "favicon.svg", "fonts/nunito-800.woff", "fonts/OFL.txt", ".nojekyll"]
PUBLISHED_TEXT = PAGES + ["style.css", "favicon.svg"]
EXTERNAL = re.compile(r"^(https?:)?//", re.IGNORECASE)


class Page(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: set[str] = set()
        self.links: list[str] = []      # <a href>, may point anywhere
        self.resources: list[str] = []  # things the browser loads by itself
        self.scripts = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = {k: (v or "") for k, v in attrs}
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "script":
            self.scripts += 1
        if tag == "a" and "href" in a:
            self.links.append(a["href"])
        elif tag == "link" and "href" in a:
            self.resources.append(a["href"])
        for key in ("src", "srcset", "poster", "data"):
            if key in a:
                self.resources.append(a[key].split()[0] if a[key] else "")
        if tag in ("iframe", "object", "embed"):
            self.resources.append(a.get("src") or a.get("data") or "embedded")


def main() -> int:
    problems: list[str] = []

    for name in REQUIRED:
        if not (ROOT / name).is_file():
            problems.append(f"missing file: {name}")

    parsed: dict[str, Page] = {}
    for name in PAGES:
        path = ROOT / name
        if not path.is_file():
            continue
        page = Page()
        page.feed(path.read_text(encoding="utf-8"))
        parsed[name] = page
        if page.scripts:
            problems.append(f"{name}: has {page.scripts} <script> tag(s); the site has no JavaScript")
        for res in page.resources:
            if EXTERNAL.match(res) or res == "embedded":
                problems.append(f"{name}: loads from another server: {res}")

    css = ROOT / "style.css"
    if css.is_file():
        text = css.read_text(encoding="utf-8")
        if "@import" in text:
            problems.append("style.css: uses @import")
        for url in re.findall(r"url\(\s*['\"]?([^'\")]+)", text):
            if EXTERNAL.match(url):
                problems.append(f"style.css: loads from another server: {url}")
            elif not (ROOT / url).is_file():
                problems.append(f"style.css: file not found: {url}")

    for name, page in parsed.items():
        for ref in page.links + page.resources:
            if not ref or EXTERNAL.match(ref) or ref.startswith(("mailto:", "tel:")):
                continue
            target, _, anchor = ref.partition("#")
            target_name = target or name
            if target and not (ROOT / target).is_file():
                problems.append(f"{name}: link to a missing file: {ref}")
                continue
            if anchor and target_name in parsed and anchor not in parsed[target_name].ids:
                problems.append(f"{name}: link to a missing anchor: {ref}")

    for name in PUBLISHED_TEXT:
        path = ROOT / name
        if path.is_file():
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if "PLACEHOLDER" in line:
                    problems.append(f"{name}:{number}: PLACEHOLDER left: {line.strip()[:90]}")

    for p in problems:
        print(f"FAIL {p}")
    print(f"{len(problems)} problem(s)" if problems else "OK: the site is self-contained and complete")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
