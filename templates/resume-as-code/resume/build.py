#!/usr/bin/env python3
"""Render a resume YAML to PDF (Typst) and Markdown.

Usage: python3 resume/build.py [path/to/resume.yml] [--out DIR] [--name BASENAME]
Defaults: resume/resume.yml -> resume/build/<FirstLast>_Resume.{pdf,md}
Fails (exit 1) if the PDF is not exactly 2 pages.
Requires: pip install typst pyyaml pypdf
"""
import argparse, pathlib, sys
import typst, yaml
from pypdf import PdfReader

HERE = pathlib.Path(__file__).resolve().parent
MAX_PAGES = 2

def to_markdown(d):
    h = d["header"]
    links = " | ".join(f"[{l['label']}]({l['url']})" for l in h.get("links", []))
    out = [f"# {h['name']}", "", h["title"], "", f"{h['email']} | {h['location']} | {links}", "",
           "## Professional Summary", "", d["summary"].strip(), "", "## Experience", ""]
    for j in d["experience"]:
        out += [f"### {j['title']} | {j['company']}", "", j["dates"], ""]
        if j.get("intro"): out += [j["intro"].strip(), ""]
        out += [f"- **{b['label']}:** {b['text']}" for b in j["bullets"]] + [""]
        if j.get("tech"): out += [" · ".join(j["tech"]), ""]
    if d.get("earlier"):
        out += ["## Earlier Experience", ""]
        out += [f"- **{e['title']} | {e['company']} ({e['years']}):** {e['text']}" for e in d["earlier"]] + [""]
    out += ["## Technical Skills", ""] + [f"- **{s['category']}:** {s['items']}" for s in d["skills"]] + [""]
    if d.get("certifications"):
        out += ["## Certifications", ""] + [f"- {c['name']} | {c['dates']}" for c in d["certifications"]] + [""]
    return "\n".join(out)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("data", nargs="?", default=str(HERE / "resume.yml"))
    ap.add_argument("--out", default=str(HERE / "build"))
    ap.add_argument("--name", default=None, help="output basename (default: <FirstLast>_Resume)")
    a = ap.parse_args()
    data_path = pathlib.Path(a.data).resolve()
    d = yaml.safe_load(data_path.read_text())
    a.name = a.name or (d["header"]["name"].replace(" ", "") + "_Resume")
    out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
    pdf = out / f"{a.name}.pdf"
    # Typst resolves yaml() relative to root; use a root that contains both files.
    root = pathlib.Path("/")
    pdf.write_bytes(typst.compile(str(HERE / "template.typ"), root=str(root),
                    font_paths=[str(HERE / "fonts")], sys_inputs={"data": str(data_path)}))
    (out / f"{a.name}.md").write_text(to_markdown(d))
    pages = len(PdfReader(str(pdf)).pages)
    print(f"{pdf} ({pages} pages), version {d.get('version')}")
    if pages > MAX_PAGES:
        sys.exit(f"FAIL: {pages} pages; resume must fit on {MAX_PAGES}")

if __name__ == "__main__":
    main()
