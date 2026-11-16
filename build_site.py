"""
Builds index.html from the executed Jupyter notebook.
Usage:  python build_site.py
Needs:  pip install nbformat markdown pygments
"""
import html
import re
import nbformat
import markdown
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

NOTEBOOK = "project/CP_Group3A6_Student_Participation.ipynb"
OUTPUT = "index.html"

nb = nbformat.read(NOTEBOOK, as_version=4)
formatter = HtmlFormatter(nowrap=True)
md = markdown.Markdown(extensions=["tables", "fenced_code"])


def slug(text):
    text = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def fix_lists(src):
    # python-markdown needs a blank line before a list or table
    lines = src.split("\n")
    out = []
    for i, line in enumerate(lines):
        starts_block = re.match(r"^(\s*[-*] |\s*\d+\. |\|)", line)
        if i > 0 and starts_block and lines[i - 1].strip() != "":
            prev_is_block = re.match(r"^(\s*[-*] |\s*\d+\. |\|)", lines[i - 1])
            if not prev_is_block:
                out.append("")
        out.append(line)
    return "\n".join(out)


def render_markdown(src):
    md.reset()
    out = md.convert(fix_lists(src))
    # add ids to h2 / h3 so the sidebar can link to them
    def add_id(m):
        tag, inner = m.group(1), m.group(2)
        return f'<{tag} id="{slug(inner)}">{inner}</{tag}>'
    return re.sub(r"<(h2|h3)>(.*?)</\1>", add_id, out)


def render_output(o):
    kind = o.get("output_type")
    if kind == "stream":
        return f'<pre class="out-text">{html.escape(o["text"])}</pre>'
    if kind == "error":
        return f'<pre class="out-text out-err">{html.escape(o.get("ename", ""))}: {html.escape(o.get("evalue", ""))}</pre>'
    data = o.get("data", {})
    if "image/png" in data:
        b64 = data["image/png"].replace("\n", "")
        return f'<img class="out-img" alt="plot output" src="data:image/png;base64,{b64}">'
    if "text/html" in data:
        return f'<div class="out-table">{data["text/html"]}</div>'
    if "text/plain" in data:
        return f'<pre class="out-text">{html.escape(data["text/plain"])}</pre>'
    return ""


body = []
nav = []
count = 0
for cell in nb.cells:
    if cell.cell_type == "markdown":
        h = render_markdown(cell.source)
        for m in re.finditer(r'<h2 id="([^"]+)">(.*?)</h2>', h):
            nav.append((m.group(1), re.sub(r"<[^>]+>", "", m.group(2))))
        body.append(f'<section class="md">{h}</section>')
    elif cell.cell_type == "code":
        count += 1
        code = highlight(cell.source, PythonLexer(), formatter)
        outs = "".join(render_output(o) for o in cell.get("outputs", []))
        n = cell.get("execution_count") or count
        block = f'''<div class="cell">
  <div class="code-wrap">
    <div class="code-head"><span class="in">In [{n}]</span><button class="copy" type="button">Copy</button></div>
    <pre class="code highlight">{code}</pre>
  </div>'''
        if outs:
            block += f'\n  <div class="output"><div class="out-label">Out [{n}]</div>{outs}</div>'
        block += "\n</div>"
        body.append(block)

nav_html = "\n".join(f'<a href="#{i}">{html.escape(t)}</a>' for i, t in nav)
pyg_css = formatter.get_style_defs(".highlight")

page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Student Participation and Academic Achievement Prediction – PAS Course Project</title>
<style>
:root {{
  --ink: #1d2327; --muted: #5b6770; --line: #dfe5e8; --bg: #ffffff; --panel: #f5f8f8;
  --accent: #0f7173; --accent-soft: #e4f1f0; --code-bg: #f7f9fa; --out-bg: #ffffff;
}}
* {{ box-sizing: border-box; }}
html {{ scroll-behavior: smooth; }}
body {{ margin: 0; font-family: -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  color: var(--ink); background: var(--bg); line-height: 1.6; font-size: 16px; }}
header {{ padding: 28px 32px 22px; border-bottom: 1px solid var(--line); background: var(--panel); }}
header h1 {{ margin: 0 0 4px; font-size: 26px; line-height: 1.25; }}
header p {{ margin: 0; color: var(--muted); }}
.links {{ margin-top: 14px; display: flex; gap: 10px; flex-wrap: wrap; align-items: center; }}
.links a, .toggle {{ font-size: 14px; text-decoration: none; color: var(--accent); border: 1px solid var(--accent);
  padding: 5px 12px; border-radius: 6px; background: #fff; cursor: pointer; font-family: inherit; line-height: 1.5; display: inline-block; }}
.links a:hover, .toggle:hover {{ background: var(--accent-soft); }}
.layout {{ display: flex; align-items: flex-start; }}
nav {{ position: sticky; top: 0; width: 250px; flex-shrink: 0; max-height: 100vh; overflow-y: auto;
  padding: 22px 14px; border-right: 1px solid var(--line); }}
nav .nav-title {{ font-size: 12px; text-transform: uppercase; letter-spacing: .06em; color: var(--muted);
  margin: 0 8px 8px; }}
nav a {{ display: block; padding: 6px 8px; border-radius: 6px; color: var(--ink); text-decoration: none; font-size: 14px; }}
nav a:hover, nav a.active {{ background: var(--accent-soft); color: var(--accent); }}
main {{ flex: 1; min-width: 0; padding: 10px 36px 60px; max-width: 1000px; }}
.md h1 {{ display: none; }}
.md h2 {{ margin: 40px 0 8px; padding-top: 10px; font-size: 23px; border-top: 1px solid var(--line); }}
.md h3 {{ margin: 26px 0 6px; font-size: 18px; }}
.md blockquote {{ margin: 10px 0; padding: 8px 14px; background: var(--accent-soft); border-radius: 6px; color: #134e4f; }}
.md blockquote p {{ margin: 0; }}
.md table, .out-table table {{ border-collapse: collapse; margin: 10px 0; font-size: 14px; }}
.md th, .md td, .out-table th, .out-table td {{ border: 1px solid var(--line); padding: 5px 10px; text-align: left; vertical-align: top; }}
.md th, .out-table th {{ background: var(--panel); }}
.out-table td {{ text-align: right; }}
.md code {{ background: var(--code-bg); padding: 1px 5px; border-radius: 4px; font-size: 14px; }}
.cell {{ margin: 16px 0; border: 1px solid var(--line); border-radius: 8px; overflow: hidden; }}
.code-head {{ display: flex; justify-content: space-between; align-items: center; padding: 4px 12px;
  background: var(--panel); border-bottom: 1px solid var(--line); font-size: 12px; color: var(--muted); }}
.copy {{ font-size: 12px; border: 1px solid var(--line); background: #fff; border-radius: 4px; padding: 2px 8px; cursor: pointer; }}
pre {{ margin: 0; overflow-x: auto; }}
pre.code {{ padding: 12px 14px; background: var(--code-bg); font-size: 13.5px; line-height: 1.5;
  font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace; }}
.output {{ padding: 10px 14px; background: var(--out-bg); border-top: 1px dashed var(--line); overflow-x: auto; }}
.out-label {{ font-size: 12px; color: var(--muted); margin-bottom: 4px; }}
pre.out-text {{ font-size: 13.5px; font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace; }}
.out-err {{ color: #b3261e; }}
.out-img {{ display: block; width: auto; max-width: min(100%, 820px); height: auto; margin: 6px 0; }}
body.hide-code .code-wrap {{ display: none; }}
body.hide-code .output {{ border-top: none; }}
footer {{ padding: 20px 32px; color: var(--muted); font-size: 13px; border-top: 1px solid var(--line); }}
@media (max-width: 860px) {{
  nav {{ display: none; }}
  main {{ padding: 6px 16px 40px; }}
  header {{ padding: 20px 16px; }}
}}
{pyg_css}
</style>
</head>
<body>
<header>
  <h1>Student Participation and Academic Achievement Prediction</h1>
  <p>PAS Course Project &middot; Group 3A6 (A Division, Batch 3) &middot; Guide: Mr. Rajkumar V. Patil</p>
  <div class="links">
    <a href="project/CP_Group3A6_Student_Participation.ipynb" download>Download notebook</a>
    <a href="project/student-por.csv" download>Original dataset</a>
    <a href="project/student_cleaned.csv" download>Cleaned dataset</a>
    <a href="https://archive.ics.uci.edu/dataset/320/student+performance" target="_blank" rel="noopener">Data source (UCI)</a>
    <button class="toggle" id="toggle" type="button">Hide code</button>
  </div>
</header>
<div class="layout">
<nav>
  <div class="nav-title">Sections</div>
  {nav_html}
</nav>
<main>
{chr(10).join(body)}
</main>
</div>
<footer>Generated from the executed Jupyter notebook. All outputs are real results of running the code.</footer>
<script>
document.getElementById('toggle').addEventListener('click', function () {{
  document.body.classList.toggle('hide-code');
  this.textContent = document.body.classList.contains('hide-code') ? 'Show code' : 'Hide code';
}});
document.querySelectorAll('.copy').forEach(function (btn) {{
  btn.addEventListener('click', function () {{
    var code = btn.closest('.code-wrap').querySelector('pre.code').innerText;
    navigator.clipboard.writeText(code).then(function () {{
      btn.textContent = 'Copied';
      setTimeout(function () {{ btn.textContent = 'Copy'; }}, 1200);
    }}).catch(function () {{}});
  }});
}});
var links = document.querySelectorAll('nav a');
var heads = Array.prototype.map.call(links, function (a) {{ return document.getElementById(a.getAttribute('href').slice(1)); }});
window.addEventListener('scroll', function () {{
  var cur = 0;
  heads.forEach(function (h, i) {{ if (h && h.getBoundingClientRect().top < 120) cur = i; }});
  links.forEach(function (a, i) {{ a.classList.toggle('active', i === cur); }});
}});
</script>
</body>
</html>
"""

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(page)
print("wrote", OUTPUT, "with", count, "code cells and", len(nav), "sections")
