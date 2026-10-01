---
name: timecard
description: Summarize the work done since the last timecard submission, per client and per day, from git commits, Jira activity, and a work log. Use when the user asks for a timecard, timesheet, weekly summary, status update, or "what did I do this week".
---

# Timecard summary

Turn a week of evidence into a per-client, day-by-day summary someone can paste into a timecard or status update. Never invent work or hours.

## 1. Load config

Read `~/.config/ai-toolkit/config.yml`, sections `identity` and `timecard` (format: `config.example.yml` in the ai-toolkit repo). If the file or a needed key is missing, ask the user for:
- the workspace folder (one subfolder per client)
- the folders to skip
- the name and email variants their commits use
- their timezone

Then offer to save the answers to that file.

If the user passed explicit dates (`/ai-toolkit:timecard 2026-03-16 2026-03-20`), use them as the window and skip step 2.

## 2. Decide the window

Get today's date in `identity.timezone`.
- `window: this-week` → Monday through today.
- `window: since-last-submission` → from the day after the most recent submission day before today, through today. Submission days come from `timecard.submission_days`; `last-weekday-of-month` means the last Mon–Fri of a month. Never cross into the previous month: start no earlier than the 1st.

Only weekdays are reported. If running unattended (as a scheduled task) and today isn't a submission day, reply with exactly one line ("Not a timecard day; skipping.") and stop.

## 3. Gather evidence

**Git.** List `timecard.workspace` fresh every run. Every subfolder except `skip_folders` is a client, so new clients are picked up automatically. In each client folder, find every git repo at any depth (skip `node_modules`, `.venv`, `vendor`). For each repo:
- Run `git log --all --since="<window start> 00:00" --pretty=format:"%H|%an|%ae|%ad|%s" --date=short`. Use `--all` so feature branches and worktrees count.
- Keep commits whose author name or email contains any of `identity.author_matches`, case-insensitive. A match on only a common first name is ambiguous. Include it only if it matches the repo's own `git config user.email`.
- For repos with real activity, read full bodies (`git log -1 --format=%B <hash>`) and skim diffs. The substance is usually in the body, not the subject.
- Multi-day infrastructure work (state migrations, imports, staged deploys) often lands as one commit at the end. Spread it across the days it plausibly happened, never before the window start.

**Jira (best-effort).** If an Atlassian connector is available, find issues updated in the window where the user is assignee or reporter. Look up their account by `identity.email`. Note status changes, their comments, and issues closed. Skip silently if unavailable.

**Work log (best-effort).** If `timecard.worklog` exists, use its entries dated within the window. Never edit it.

## 4. Write the summary

```
Timecard: Mon Oct 5 – Fri Oct 9, 2026
No activity found: Wed Oct 7   ← only if a weekday had nothing for any client

## Client A
**Mon Oct 5** - 2–4 sentences on what was accomplished, grouped by theme…
**Thu Oct 8** - …

## Client B
No development activity this period.
```

Rules:
- One short paragraph (2–4 sentences, no bullets) per client per day with activity, in date order. Never merge clients.
- Declarative, with no pronouns: "Migrated Lambda secrets to Terraform-managed config," not "He migrated…".
- Describe what changed and why it matters. Never cite ticket, issue, or MR numbers; the sentence must make sense on its own.
- Note decisions (mark them "(inferred)" if not explicit) and anything open or blocked, inside the paragraph.
- No hours; the user fills those in.

End with the complete summary. When this runs as a scheduled task, the final reply is often what gets emailed or pushed.

## Running it on a schedule

Create a scheduled task on the computer that has the repos, with a prompt like "Run the ai-toolkit timecard skill for the current window and end with the full summary." A cron that fires every Friday **and** on days 28–31, such as `59 11 28-31 * 5`, covers the month-end case. Fields filled in both day columns are OR'd, and step 2 filters out the non-submission days.
