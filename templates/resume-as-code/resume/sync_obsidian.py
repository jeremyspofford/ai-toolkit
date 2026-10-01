#!/usr/bin/env python3
"""Mirror the resume into the Obsidian vault (if one exists on this machine).

Vault: $OBSIDIAN_VAULT or ~/Obsidian_Vault. Target: <vault>/$OBSIDIAN_RESUME_DIR (default Resume/)
  Latest/      newest version, built from resume/resume.yml
  Released/    the approved version from released/
  Applications/<slug>/  tailored resumes, gap reports, job descriptions
  Resume Changelog.md   copy of CHANGELOG.md
  Resume.md             index note with current versions
Run from anywhere after `git pull`. Exits 0 with a message if there is no vault.
"""
import datetime, os, pathlib, shutil, subprocess, sys, yaml

REPO = pathlib.Path(__file__).resolve().parent.parent
vault = pathlib.Path(os.environ.get("OBSIDIAN_VAULT", pathlib.Path.home() / "Obsidian_Vault"))
if len(sys.argv) > 1: vault = pathlib.Path(sys.argv[1])
if not vault.is_dir():
    print(f"No Obsidian vault at {vault}; skipping vault sync (GitHub only).")
    sys.exit(0)
sub = os.environ.get("OBSIDIAN_RESUME_DIR", "Resume")
dest = vault / sub

def copy_tree(src, dst, exts=(".pdf", ".md")):
    if not src.is_dir(): return []
    dst.mkdir(parents=True, exist_ok=True)
    copied = []
    for f in sorted(src.iterdir()):
        if f.is_file() and f.suffix in exts and f.name != "README.md":
            shutil.copy2(f, dst / f.name); copied.append(f.name)
    return copied

# Latest: build fresh from resume/resume.yml
doc = yaml.safe_load((REPO / "resume/resume.yml").read_text())
latest_v = doc["version"]
base = doc["header"]["name"].replace(" ", "") + "_Resume"
build = REPO / "resume" / "build"
subprocess.run([sys.executable, str(REPO / "resume/build.py")], check=True)
copy_tree(build, dest / "Latest")

released_v = (REPO / "released/VERSION").read_text().strip() if (REPO / "released/VERSION").exists() else None
if released_v:
    copy_tree(REPO / "released", dest / "Released")

apps = []
for app in sorted((REPO / "applications").glob("*/")):
    if copy_tree(app, dest / "Applications" / app.name): apps.append(app.name)

shutil.copy2(REPO / "CHANGELOG.md", dest / "Resume Changelog.md")
head = subprocess.run(["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
lines = [
    "---", "tags: [resume, career]", f"latest_version: {latest_v}",
    f"released_version: {released_v or 'none yet'}", f"synced: {datetime.date.today()}", "---", "",
    "# Resume", "",
    "Managed automatically from the resume repo. Edits made here are overwritten on the next sync.", "",
    f"- **Latest** (v{latest_v}, newest draft): [[{sub}/Latest/{base}.md|markdown]] · [[{sub}/Latest/{base}.pdf|PDF]]",
    (f"- **Released** (v{released_v}, approved for general use): [[{sub}/Released/{base}.md|markdown]] · [[{sub}/Released/{base}.pdf|PDF]]"
     if released_v else "- **Released**: none approved yet"),
    "- **Changelog**: [[Resume Changelog]]", "",
    "## Applications", "",
] + ([f"- [[{sub}/Applications/{a}/gap-report|{a}]]" for a in apps] or ["None yet."]) + ["", f"_Synced from commit {head}._", ""]
(dest / "Resume.md").write_text("\n".join(lines))
print(f"Synced to {dest}: latest v{latest_v}, released {released_v or 'none'}, {len(apps)} application(s).")
