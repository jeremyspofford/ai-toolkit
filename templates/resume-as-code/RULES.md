# Resume rules

These govern every change to `resume/resume.yml`, `evidence/log.md`, and anything in `applications/`. An AI assistant (scheduled or interactive) must read this file before editing any of them. **Fill in the "Your settings" section first.**

## Your settings

- **Positioning:** <e.g. Senior Platform Engineer, AWS-focused>
- **Protected numbers** (change only when you say so): <list every metric already on your resume>
- **Career start** (for the year count): <YYYY-MM>
- **Not on the resume until earned:** <certs in progress, skills you're learning>
- **Page limit:** 2

## Hard rules (never broken)

- **No fabrication.** Never invent metrics, scope, team size, leadership, outcomes, causality, skills, tools, certifications, titles, or dates. Every claim must trace to evidence (`evidence/log.md` or something you said explicitly).
- **Suggestions are not accomplishments.** Something the assistant proposed, drafted, or scripted counts only after you confirm it was delivered or used.
- **Protected facts:** name, contact details, titles, employers, dates, certifications, and the protected numbers change only when you say so. Never increment numbers from the calendar, except the total year count derived from your career start.
- **Confidentiality:** no client or customer names, internal URLs, hostnames, account IDs, ticket numbers, or confidential figures, anywhere in this repo.
- **Employer vs. personal:** personal projects never appear as employer work.
- **Layout:** the general resume must build to the page limit or fewer (`build.py` enforces 2 pages).

## When the resume may change

Evidence is always logged. The resume itself changes only when one of these holds:
- **One major item:** a completed platform or migration, substantial new ownership, a measured cost/reliability/security result, a certification, or a role change.
- **Two or more meaningful items:** distinct completed improvements that add scope or depth not already on the page.

**Minor items never trigger an update**, however many pile up. That covers routine fixes, single resource edits, research, rewording, and more work on something already listed. Time passing never triggers one either.

Allow at least 30 days between content updates, except for major items, role or cert changes, or corrections you ask for.

Prefer strengthening or replacing an existing bullet over adding one.

## Versioning

`version:` in `resume/resume.yml`:
- **major:** role or career restructure
- **minor:** a new or substantively changed accomplishment, skill, or cert
- **patch:** a correction, or a year-count update

Every change gets a `CHANGELOG.md` entry with the exact before/after text, why, and the evidence IDs.

Tags, created by `.github/workflows/resume.yml`:
- `vX.Y.Z`: immutable
- `latest`: moving; the newest version
- `released`: moving; the version you approved for general use
- `applied/<slug>`: exactly what you sent for a specific application

## Tailored resumes (`applications/<YYYY-MM-company-role>/`)

- Start from `resume/resume.yml`, plus `evidence/log.md` entries with `status: completed`.
- **May:** reorder, select, merge, or trim bullets; use the posting's vocabulary where it truthfully describes the same work; rewrite the summary for the role; reorder or trim skills.
- **May not:** add a skill, tool, metric, or experience with no evidence.
- Always write `gap-report.md`, rating each requirement strong / adjacent / gap.
- Must also fit on 2 pages.
