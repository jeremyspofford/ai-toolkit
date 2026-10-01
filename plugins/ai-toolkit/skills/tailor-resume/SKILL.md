---
name: tailor-resume
description: Build a role-specific resume from a job posting using only verified evidence, plus a gap report rating every requirement strong, adjacent, or gap. Use when the user pastes or links a job description, or says "tailor my resume", "customize my resume for this role", or "how do I match this job".
---

# Tailor a resume to a job posting

Make the resume lean toward the role **without adding anything untrue**. A tailored resume is a selection and a re-emphasis, not an embellishment.

## 1. Load config and sources

Read the `resume` section of `~/.config/ai-toolkit/config.yml`. Its sources, in order of trust:
1. `resume.source`: the general resume (YAML in the Resume as Code layout, or Markdown)
2. `resume.long_form`: longer write-ups of past work, if any
3. `resume.evidence_log`: entries with `status: completed` only

If config is missing, ask for the general resume (a file path or pasted text), and offer to save its location.

Get the posting: pasted text, a file, or a URL (fetch it). Save it with its URL and today's date.

## 2. Analyze the posting

List the must-haves, the nice-to-haves, the responsibilities, and the vocabulary (tool names, phrasing the posting repeats).

## 3. Match evidence

For each requirement, find support in the sources and rate it:
- **strong:** direct evidence of the same thing
- **adjacent:** related evidence (say what it is, e.g. "GitLab CI, not GitHub Actions")
- **gap:** no evidence

## 4. Write the tailored resume

Start from the general resume.

**You may:**
- reorder bullets so the strongest matches lead
- select, merge, or trim bullets, and bring back detail from long-form sources
- rewrite the summary for this role, using only facts already present
- use the posting's vocabulary **where it truthfully describes the same work**
- retitle the header line only to a title that honestly describes the person's function (e.g. "Senior DevOps / Platform Engineer")
- reorder and trim skills to lead with what the posting asks for

**You may not:**
- add a skill, tool, metric, title, certification, or experience with no evidence, even if the posting requires it
- inflate scope (team size, ownership, leadership) or change dates
- turn an "adjacent" into a claim of the real thing

Keep it to two pages. If the user has a `resume.build` command, write the tailored YAML next to the posting and run it, naming the output `<Name>_Resume_<Company>.pdf`.

Save everything to `<applications_dir>/<YYYY-MM>-<company>-<role-slug>/`:
- `job-description.md`
- the tailored resume
- `gap-report.md`

## 5. Gap report

`gap-report.md`: a table of requirement | rating | evidence or note. Then 2–4 honest suggestions for handling gaps in a cover letter or interview, such as transferable experience, active learning, or questions to ask. Gaps are for the candidate to address, never for the resume to paper over.

## 6. Show the user

Show the tailored resume (or PDF), the gap report, and a short word-level diff against the general resume. If it's in git, use `git diff --no-index --word-diff`. Ask before committing. When they say they've submitted it, suggest tagging that exact version (`git tag applied/<folder>`).
