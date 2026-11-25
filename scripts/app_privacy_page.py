"""Turns the English section of an app's PRIVACY.md or TERMS.md into a page of the website.

Run from the repository root whenever the app's document changes, then commit the page:
python scripts/app_privacy_page.py ../SecondShiftManager/PRIVACY.md privacy.html second-shift-manager-privacy.html <contact e-mail>
python scripts/app_privacy_page.py ../SecondShiftManager/TERMS.md privacy.html second-shift-manager-terms.html <contact e-mail> terms
The contact e-mail must be the app's `privacyEmail` (lib/domain/legal_text.dart). The optional
fifth argument picks the document: `privacy` (the default) or `terms`.
"""
import html
import re
import sys
from pathlib import Path

src, template_page, out, email = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4]
kind = sys.argv[5] if len(sys.argv) > 5 else "privacy"
DOCS = {
    "privacy": ("Privacy policy",
                "How the Second Shift Manager app and its server handle personal data."),
    "terms": ("Terms of use",
              "The terms of use of the Second Shift Manager app and its server."),
}
title, description = DOCS[kind]

text = src.read_text(encoding="utf-8")
text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
english = text.split("## English", 1)[1].split("\n---", 1)[0].split("\n## ", 1)[0]
english = english.replace("{{PRIVACY_EMAIL}}", email)


def inline(s: str) -> str:
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", s)
    s = s.replace(html.escape(email), f'<a href="mailto:{email}">{email}</a>')
    s = re.sub(r"\bwww\.uoou\.gov\.cz\b", '<a href="https://uoou.gov.cz">www.uoou.gov.cz</a>', s)
    return s


body: list[str] = []
version = ""
lst = None
for line in english.strip().splitlines():
    line = line.rstrip()
    m_ul, m_ol = re.match(r"^- (.*)", line), re.match(r"^\d+\. (.*)", line)
    kind_of_list = "ul" if m_ul else "ol" if m_ol else None
    if lst and kind_of_list != lst:
        body.append(f"</{lst}>")
        lst = None
    if kind_of_list:
        if not lst:
            body.append(f"<{kind_of_list}>")
            lst = kind_of_list
        body.append(f"<li>{inline((m_ul or m_ol).group(1))}</li>")
    elif not line:
        continue
    elif line.startswith("#### "):
        body.append(f"<h3>{inline(line[5:])}</h3>")
    elif line.startswith("### "):
        body.append(f"<h2>{inline(line[4:])}</h2>")
    elif not version and re.fullmatch(r"\*Version of .*\.\*", line):
        version = line.strip("*").rstrip(".")
    else:
        body.append(f"<p>{inline(line)}</p>")
if lst:
    body.append(f"</{lst}>")

page = template_page.read_text(encoding="utf-8")
head, rest = page.split('<div class="prose">', 1)
_, tail = rest.split("</div>\n  </div>\n</main>", 1)
head = head.replace("<title>Privacy policy · Random Idea Studio</title>",
                    f"<title>{title} of Second Shift Manager · Random Idea Studio</title>")
head = re.sub(r'<meta name="description" content="[^"]*">',
              f'<meta name="description" content="{description}">', head)
indent = "      "
content = [
    '<p class="eyebrow">Second Shift Manager</p>',
    f"<h1>{title}</h1>",
    f"<p>{html.escape(version)}. The same text is shown in the app (Settings → About).</p>",
] + body
out.write_text(head + '<div class="prose">\n' + "\n".join(indent + c for c in content) + "\n    </div>\n  </div>\n</main>" + tail,
               encoding="utf-8", newline="\n")
print(f"{out}: {len(body)} blocks, {version}")
