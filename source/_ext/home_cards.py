"""Generate homepage cards from top-level Sphinx documents."""

from __future__ import annotations

import re
from pathlib import Path

from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx import addnodes


TITLE_SUFFIXES = (
    "综合说明与学习索引",
    "系列教学",
    "系列",
)


def _plain_text(value: str) -> str:
    value = re.sub(r"!\[[^]]*]\([^)]*\)", "", value)
    value = re.sub(r"\[([^]]+)]\([^)]*\)", r"\1", value)
    value = re.sub(r"[*_`#>]", "", value)
    return re.sub(r"\s+", " ", value).strip()


def _document_summary(path: Path) -> tuple[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    title = path.parent.name.upper()
    title_index = -1

    for index, line in enumerate(lines):
        match = re.match(r"^#\s+(.+?)\s*$", line)
        if match:
            title = _plain_text(match.group(1))
            title_index = index
            break

    short_title = title
    for suffix in TITLE_SUFFIXES:
        short_title = short_title.removesuffix(suffix).strip()

    paragraph: list[str] = []
    started = False
    for line in lines[title_index + 1 :]:
        stripped = line.strip()
        if not stripped:
            if started:
                break
            continue
        if stripped.startswith(("#", "```", ":::", "<")):
            if started:
                break
            continue
        started = True
        paragraph.append(stripped)

    summary = _plain_text(" ".join(paragraph))
    if not summary:
        summary = f"进入{short_title}栏目查看相关文档。"
    return short_title, summary


def _doc_link(docname: str, title: str) -> addnodes.pending_xref:
    link = addnodes.pending_xref(
        "",
        refdomain="std",
        reftype="doc",
        reftarget=docname,
        refexplicit=True,
    )
    link += nodes.strong(text=title)
    return link


class HomeCardsDirective(Directive):
    has_content = False

    def run(self):
        env = self.state.document.settings.env
        srcdir = Path(env.srcdir)
        paths = list(srcdir.glob("*/index.md"))
        preferred = {"c": 0, "stm32": 1, "linux": 2, "sw": 3}
        paths.sort(key=lambda path: (preferred.get(path.parent.name, 100), path.parent.name))

        grid = nodes.container(classes=["home-auto-grid"])
        for path in paths:
            env.note_dependency(str(path))
            section = path.parent.name
            docname = f"{section}/index"
            title, summary = _document_summary(path)

            card = nodes.container(classes=["home-auto-card"])
            card += nodes.paragraph(text=section.upper(), classes=["home-auto-kicker"])
            heading = nodes.paragraph(classes=["home-auto-title"])
            heading += _doc_link(docname, title)
            card += heading
            card += nodes.paragraph(text=summary, classes=["home-auto-summary"])
            more = nodes.paragraph(classes=["home-auto-more"])
            more += _doc_link(docname, "进入栏目 →")
            card += more
            grid += card

        return [grid]


def setup(app):
    app.add_directive("home-cards", HomeCardsDirective)
    return {
        "version": "1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
