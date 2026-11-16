"""Render a paper-reading Markdown report to portable dark HTML."""
import argparse
import html
import json
import os
import re
import shutil
import subprocess
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
KATEX_VERSION = "0.16.22"


def copy_math_assets(destination):
    """Copy only local display assets, preserving the bundled license."""
    vendor = ROOT / "vendor" / "katex"
    destination = destination / ("katex-" + KATEX_VERSION)
    pairs = [(vendor / "LICENSE", destination / "LICENSE"),
             (vendor / "dist" / "katex.min.css", destination / "katex.min.css")]
    pairs.extend((p, destination / "fonts" / p.name)
                 for p in sorted((vendor / "dist" / "fonts").iterdir())
                 if p.is_file())
    # Refuse to replace another version's files at an existing destination.
    for source, target in pairs:
        if target.exists() and target.read_bytes() != source.read_bytes():
            raise ValueError("Different existing math asset: " + str(target))
    for source, target in pairs:
        if not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
    return destination / "katex.min.css"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("markdown", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--assets-dir", type=Path,
                        help="Parent of the versioned math assets folder")
    parser.add_argument("--label", default="论文问题与方法讲解",
                        help="Display label; the title comes from the Markdown")
    parser.add_argument("--node", help="Node.js executable when not on PATH")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    from markdown_it import MarkdownIt
    from bs4 import BeautifulSoup

    source = args.markdown.resolve()
    output = (args.output or source.with_suffix(".html")).resolve()
    if output.parent != source.parent:
        parser.error("Keep HTML beside its Markdown to preserve relative links.")
    if output == source or output.suffix.lower() != ".html":
        parser.error("Output must be a distinct .html file.")
    if output.exists() and not args.overwrite:
        parser.error("Output exists; choose a new run or explicitly use --overwrite.")
    raw = source.read_text(encoding="utf-8")
    formulas = []

    def mask(match):
        index = len(formulas)
        formulas.append(match.group(1).strip())
        return "\n\nWORKFLOWMATHBLOCK" + str(index) + "END\n\n"

    masked = re.sub(r"(?ms)^\$\$[ \t]*\n(.*?)\n\$\$[ \t]*$", mask, raw)
    if re.search(r"^\$\$[ \t]*$", masked, re.M):
        parser.error("Unpaired display-math delimiter; each $$ needs its own line.")
    rendered = []
    if formulas:
        node = args.node or shutil.which("node")
        if not node:
            parser.error("Node.js not found; pass --node or add it to PATH.")
        result = subprocess.run(
            [node, str(ROOT / "scripts" / "render_math.cjs")],
            input=json.dumps(formulas, ensure_ascii=False),
            text=True, encoding="utf-8", capture_output=True, check=False)
        if result.returncode:
            raise RuntimeError("KaTeX parse failed: " + result.stderr.strip())
        rendered = json.loads(result.stdout)

    body = MarkdownIt("commonmark", {"html": True}).enable("table").render(masked)
    for index, value in enumerate(rendered):
        placeholder = "<p>WORKFLOWMATHBLOCK" + str(index) + "END</p>"
        if placeholder not in body:
            raise ValueError("Math must occupy an independent paragraph.")
        block = ('<div class="formula" role="group" aria-label="公式 '
                 + str(index + 1) + '">' + value + "</div>")
        body = body.replace(placeholder, block)
    soup = BeautifulSoup(body, "html.parser")
    toc = []
    for index, heading in enumerate(soup.find_all(["h2", "h3"]), 1):
        heading["id"] = "section-" + str(index)
        if heading.name == "h2":
            toc.append('<a href="#' + heading["id"] + '">'
                       + html.escape(heading.get_text()) + "</a>")
    for table in soup.find_all("table"):
        wrapper = soup.new_tag("div")
        wrapper["class"] = "table-wrap"
        table.wrap(wrapper)
        hint = soup.new_tag("p")
        hint["class"] = "table-hint"
        hint.string = "表格可左右滑动"
        wrapper.insert_before(hint)
    for picture in soup.find_all("img"):
        if picture.parent.name != "a":
            link = soup.new_tag("a", href=picture.get("src", ""))
            link["title"] = "查看原图"
            picture.wrap(link)
    title = soup.find("h1")
    title = title.get_text() if title else source.stem
    css = (ROOT / "assets" / "report.css").read_text(encoding="utf-8")
    if "WORKFLOWMATHBLOCK" in str(soup):
        raise ValueError("Unrendered formula placeholder remains.")
    if len(soup.select(".katex")) != len(formulas):
        raise ValueError("Rendered formula count mismatch.")
    stylesheet = ""
    if formulas:
        assets = (args.assets_dir or output.parent / "render-assets").resolve()
        css_file = copy_math_assets(assets)
        css_url = quote(os.path.relpath(css_file, output.parent).replace(os.sep, "/"),
                        safe="/.-_")
        stylesheet = '<link rel="stylesheet" href="' + css_url + '">'
    page = ('<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            "<title>" + html.escape(title) + "</title>" + stylesheet
            + "<style>" + css + "</style></head><body><main>"
            + '<div class="status">' + html.escape(args.label)
            + ' · 原图可点击放大</div><nav aria-label="目录">'
            + "".join(toc) + "</nav>" + str(soup) + "</main></body></html>")
    output.write_text(page, encoding="utf-8")
    print(json.dumps({"output": str(output), "formulas": len(formulas),
                      "images": len(soup.find_all("img")),
                      "scope": "Document rendering only; inspect content and visuals."},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
