"""
Convert BowCRQ .md docs into styled HTML pages under /bowcrq/<slug>/.

Rebuild when the source docs change:
    python tools/build-bowcrq-docs.py

Source docs live in E:/Development/BowCRQ_Tablet/. All output pages carry
<meta name="robots" content="noindex, nofollow"> so they stay invisible
to search engines until the Play Store launch. To flip them live, remove
the noindex block from each generated file (and the Disallow line in
robots.txt) at release time.

The markdown parser handles what the BowCRQ docs actually use: ATX
headings, paragraphs, unordered lists, GitHub-flavoured tables, inline
code, bold, links and horizontal rules. It is not a general-purpose
CommonMark renderer.
"""
from __future__ import annotations

import html
import re
from pathlib import Path

SRC_DIR = Path(r"E:\Development\BowCRQ_Tablet")
OUT_DIR = Path(r"E:\Development\website\bowcrq")

# (source filename, output slug, page title, eyebrow, description meta)
DOCS = [
    (
        "SECURITY.md",
        "security",
        "Security model",
        "BowCRQ",
        "BowCRQ security model: network posture, authentication, data at rest, change governance and Android distribution.",
    ),
    (
        "SBOM.md",
        "sbom",
        "Software Bill of Materials",
        "BowCRQ",
        "Exhaustive dependency inventory for BowCRQ, generated from the resolved build graphs.",
    ),
    (
        "THIRD-PARTY-NOTICES.md",
        "third-party-notices",
        "Third-party notices",
        "BowCRQ",
        "Third-party components bundled in BowCRQ, with licence summaries.",
    ),
    (
        "LICENCE.md",
        "licence",
        "Licence",
        "BowCRQ",
        "BowCRQ software licence.",
    ),
]


INLINE_CODE_RE = re.compile(r"`([^`]+)`")
BOLD_RE = re.compile(r"\*\*([^*]+)\*\*")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def render_inline(text: str) -> str:
    out = html.escape(text)
    # Links must run before code/bold so the URL chars aren't escaped twice.
    def link_sub(match: re.Match[str]) -> str:
        label, url = match.group(1), match.group(2)
        return f'<a href="{html.escape(url, quote=True)}">{html.escape(label)}</a>'
    # Because we escaped first, re-parse against the escaped text using
    # patterns that match the escaped delimiters.
    out = LINK_RE.sub(link_sub, out)
    out = BOLD_RE.sub(lambda m: f"<strong>{m.group(1)}</strong>", out)
    out = INLINE_CODE_RE.sub(lambda m: f"<code>{m.group(1)}</code>", out)
    return out


def parse_table(rows: list[str]) -> str:
    def cells(line: str) -> list[str]:
        cs = [c.strip() for c in line.strip().strip("|").split("|")]
        return cs

    header = cells(rows[0])
    body = [cells(r) for r in rows[2:]]

    thead = (
        "<thead><tr>"
        + "".join(f"<th>{render_inline(c)}</th>" for c in header)
        + "</tr></thead>"
    )
    tbody = (
        "<tbody>"
        + "".join(
            "<tr>"
            + "".join(f"<td>{render_inline(c)}</td>" for c in row)
            + "</tr>"
            for row in body
        )
        + "</tbody>"
    )
    return f'<div class="doc-table-wrap"><table class="doc-table">{thead}{tbody}</table></div>'


def md_to_html_body(md: str) -> str:
    """Very small markdown-to-HTML pass for the BowCRQ doc set."""
    lines = md.splitlines()
    out: list[str] = []
    i = 0
    n = len(lines)

    # The first top-level heading becomes the page's <h1>, rendered by the
    # HTML wrapper. Skip it in the body pass so we do not duplicate it.
    while i < n and not lines[i].strip():
        i += 1
    if i < n and lines[i].startswith("# "):
        i += 1

    para: list[str] = []

    def flush_para() -> None:
        if para:
            out.append("<p>" + render_inline(" ".join(para).strip()) + "</p>")
            para.clear()

    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            flush_para()
            i += 1
            continue

        if stripped == "---":
            flush_para()
            out.append("<hr>")
            i += 1
            continue

        if stripped.startswith("### "):
            flush_para()
            out.append(f"<h3>{render_inline(stripped[4:].strip())}</h3>")
            i += 1
            continue

        if stripped.startswith("## "):
            flush_para()
            out.append(f"<h2>{render_inline(stripped[3:].strip())}</h2>")
            i += 1
            continue

        # Table: header row + separator row + body rows.
        if (
            stripped.startswith("|")
            and i + 1 < n
            and re.match(r"^\|\s*:?-+:?\s*(\|\s*:?-+:?\s*)+\|?\s*$", lines[i + 1].strip())
        ):
            flush_para()
            rows = [line]
            i += 1
            while i < n and lines[i].strip().startswith("|"):
                rows.append(lines[i])
                i += 1
            out.append(parse_table(rows))
            continue

        # Unordered list.
        if re.match(r"^[-*]\s+", stripped):
            flush_para()
            items: list[list[str]] = []
            while i < n:
                item_match = re.match(r"^[-*]\s+(.*)$", lines[i].strip())
                if item_match:
                    items.append([item_match.group(1)])
                    i += 1
                    # Fold soft-wrapped continuation lines into the current item.
                    while i < n:
                        cont = lines[i]
                        if not cont.strip():
                            break
                        if re.match(r"^[-*]\s+", cont.strip()):
                            break
                        if cont.startswith(("#", "|")):
                            break
                        # Continuation lines start with whitespace in the source.
                        if cont.startswith((" ", "\t")):
                            items[-1].append(cont.strip())
                            i += 1
                            continue
                        break
                else:
                    break
            out.append(
                "<ul>"
                + "".join(f"<li>{render_inline(' '.join(parts))}</li>" for parts in items)
                + "</ul>"
            )
            continue

        # Fallback: accumulate a paragraph.
        para.append(stripped)
        i += 1

    flush_para()
    return "\n\n          ".join(out)


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en" class="no-js">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | BowCRQ | RiskByDesign</title>
  <meta name="description" content="{description}">
  <meta name="robots" content="noindex, nofollow">
  <link rel="canonical" href="https://riskbydesign.net/bowcrq/{slug}/">
  <meta name="theme-color" content="#212428">

  <link rel="icon" type="image/png" href="/assets/favicon.png">
  <link rel="stylesheet" href="/css/style.css">
</head>
<body>

  <a class="skip-link" href="#doc">Skip to content</a>

  <header class="site-header">
    <div class="container header-inner">
      <a class="brand" href="/">
        <span class="brand-plate"><img class="brand-logo" src="/assets/riskbydesign-logo.png" alt="RiskByDesign" width="132" height="72"></span>
      </a>

      <nav class="site-nav" aria-label="Main navigation">
        <button class="nav-toggle" aria-expanded="false" aria-controls="nav-menu">
          <span class="nav-toggle-bar"></span>
          <span class="nav-toggle-bar"></span>
          <span class="nav-toggle-bar"></span>
          <span class="visually-hidden">Menu</span>
        </button>
        <ul id="nav-menu" class="nav-menu">
          <li><a href="/">Home</a></li>
          <li><a href="/lab/">The Lab</a></li>
          <li><a href="/blog/">Writing</a></li>
          <li><a class="nav-contact" href="/#contact">Contact</a></li>
        </ul>
      </nav>
    </div>
  </header>

  <main>
    <article id="doc" class="section post">
      <div class="container container-narrow">
        <p class="eyebrow reveal"><a href="/bowcrq/">{eyebrow} documents</a></p>
        <h1 class="post-title reveal">{title}</h1>

        <div class="post-body reveal">
          {body}
        </div>

        <p class="post-back"><a href="/bowcrq/">&laquo; Back to BowCRQ documents</a></p>
      </div>
    </article>
  </main>

  <footer class="site-footer">
    <div class="container footer-inner">
      <p>&copy; <span id="year">2026</span> Michael Walker &middot; ABN 40 630 841 483 &middot; All rights reserved.</p>
      <p class="footer-note">Built by hand. No trackers, no analytics, no cookies.</p>
    </div>
  </footer>

  <script src="/js/main.js"></script>
</body>
</html>
"""


def build_one(src_name: str, slug: str, title: str, eyebrow: str, description: str) -> None:
    src = SRC_DIR / src_name
    md = src.read_text(encoding="utf-8")
    body = md_to_html_body(md)
    out_path = OUT_DIR / slug / "index.html"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        HTML_TEMPLATE.format(
            title=html.escape(title),
            description=html.escape(description, quote=True),
            slug=slug,
            eyebrow=html.escape(eyebrow),
            body=body,
        ),
        encoding="utf-8",
    )
    print(f"wrote {out_path}")


def main() -> None:
    for entry in DOCS:
        build_one(*entry)


if __name__ == "__main__":
    main()
