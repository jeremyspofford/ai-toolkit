# Resume as Code

Your resume as a YAML file, a Typst template, and a GitHub Actions workflow:

- **One source.** `resume/resume.yml` holds content only. `build.py` renders a PDF and a Markdown copy, so diffs are readable.
- **A build that enforces length.** It fails if the PDF goes over 2 pages.
- **Versions.** Every push to `main` tags `vX.Y.Z` and refreshes a `latest` pre-release. A manual "Run workflow" promotes a version to `released`. Tag what you send with `applied/<company-role>`.
- **Rules for AI help.** `RULES.md` forbids fabrication and sets when a change is worth making. `resume/MONTHLY.md` is a monthly review procedure for a scheduled assistant: it logs evidence from your git history, updates only when something clears the bar, and suggests blog posts.
- **Tailoring with a gap report.** Use the `tailor-resume` skill from the ai-toolkit plugin.
- **Optional Obsidian mirror.** `resume/sync_obsidian.py`.

Background: [Resume as Code](https://jeremyspofford.dev/blog/resume-as-code).

## Start

```bash
# copy the template into a new repo (needs the GitHub CLI)
gh repo create my-resume --private --clone && cd my-resume
curl -fsSL https://github.com/jeremyspofford/ai-toolkit/archive/refs/heads/main.tar.gz \
  | tar -xz --strip-components=3 "ai-toolkit-main/templates/resume-as-code"
pip install typst pyyaml pypdf
python3 resume/build.py            # renders the example to resume/build/
```

Then:
1. **Replace the example** in `resume/resume.yml` with your resume. Keep the structure: header, summary, experience with label/text bullets, earlier, skills, certifications.
2. **Fill in "Your settings"** at the top of `RULES.md`: positioning, protected numbers, career start.
3. **Commit and push.** The workflow tags `v1.0.0` and attaches the PDF to a `latest` pre-release.
4. **Approve a version** for general use: GitHub → Actions → Resume → Run workflow → enter the version. It copies that version into `released/` and marks it the repo's Latest release.

## Layout

```
resume/resume.yml        content (source of truth)
resume/template.typ      layout; edit to restyle
resume/build.py          YAML → PDF + Markdown, fails over 2 pages
resume/MONTHLY.md        monthly review procedure for a scheduled assistant
resume/state.yml         cooldown + per-machine checkpoints for that review
resume/sync_obsidian.py  optional Obsidian mirror
RULES.md                 what may change and when; no fabrication
CHANGELOG.md             every version, with before/after text
evidence/log.md          sanitized record of real accomplishments
applications/            tailored resumes + gap reports, one folder each
released/                the approved version
```

## Monthly review on a schedule

With Claude, create a scheduled task on the computer that has your work repos, using a prompt like:

> Pull my resume repo, read RULES.md and resume/MONTHLY.md, and follow MONTHLY.md exactly. RULES.md wins over anything else. End with the report from step 7.

Set `identity`, `timecard`, and `resume.repo` in `~/.config/ai-toolkit/config.yml` (see `config.example.yml`) so the review knows where your repos are and which commits are yours.

## Publishing to a website

`released/resume.yml` is a stable, approved file. Render your site's resume page from it and serve `released/*_Resume.pdf` as the download. The page and the PDF then can't disagree. Uncomment the `deploy` job in the workflow to redeploy on release.

Fonts: Liberation Sans (SIL Open Font License, see `resume/fonts/`).
