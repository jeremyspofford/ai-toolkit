# Monthly resume review: procedure

A scheduled task on each computer you work from runs this file. Follow it exactly. `../RULES.md` overrides anything here.

Shells:
- **File work** (reading, searching, editing, building): any shell that can see the files.
- **git pull/push**: must run in a shell on the computer itself that has your git credentials. A sandboxed shell may be able to edit files but not push.

## 0. Sync first (always)

1. The repo path is `resume.repo` in `~/.config/ai-toolkit/config.yml`. If it is missing locally, clone it from its `origin`.
2. Run `git checkout main && git pull --rebase`. If that fails (no network, no credentials, merge conflict), stop and report **BLOCKED** with the error. Do not work from a stale copy.
3. `pip install typst pyyaml pypdf` if `python3 -c "import typst,yaml,pypdf"` fails.

## 1. Read state

Read `RULES.md`, `CHANGELOG.md`, `evidence/log.md`, `resume/resume.yml`, `resume/state.yml`, and any long-form files listed under `resume.long_form` in the config.
Get this machine's name with `hostname -s`.
Review window: from 14 days before `machines[<hostname>]` (or 45 days ago if absent) through today.

## 2. Collect evidence on this machine (best-effort; record what was and wasn't searched)

- **Git:**
  - Every git repo under `timecard.workspace`, at any depth. Skip `timecard.skip_folders`, and skip `node_modules`, `.venv`, and `vendor`.
  - Run `git log --all --since=<window start>` and keep commits whose author matches `identity.author_matches`.
  - Read commit bodies and diffs for substance, not just subjects.
- **Work log:** `timecard.worklog`, if present. Use entries dated in the window. Never edit it.
- **Jira:** issues updated in the window where you are assignee or reporter, via the Atlassian connector if available. Skip silently if not.
- **Past chats:** chats in the window with substantive completed work, if those tools are available. Skip silently if not.

## 3. Log evidence

For each distinct, completed piece of work that could plausibly matter for a senior DevOps/Platform resume, append an entry to `evidence/log.md` in the documented format:
- **Sanitized:** no client names, URLs, hostnames, ticket numbers, or account IDs.
- **Deduplicated** against existing entries by accomplishment, not by date or source. Add a new source to an existing entry rather than creating a duplicate.
- Routine work (small fixes, single resource edits, research) gets **no entry** unless it is part of a bigger completed effort.
- Unclear status or outcome → `status: needs-confirmation`.

## 4. Decide

Apply the "When the monthly run may change the resume" rules in `RULES.md` to all `pending` entries, including ones logged earlier by other machines.
- **No qualifying change:** leave `resume/resume.yml` alone. Result: **NO_UPDATE**.
- **Qualifying change:**
  - Edit `resume/resume.yml`, preferring to strengthen or replace a bullet. Keep your current role to about 8 bullets.
  - Bump `version` (usually minor).
  - Add a `CHANGELOG.md` entry with exact before/after text, why, and the evidence IDs.
  - Set those evidence entries to `included vX.Y.Z`.
  - Set `last_content_update` to today.
  - Run `python3 resume/build.py`; it must succeed (2 pages max). If it fails, tighten wording; never drop protected facts.
  - Result: **UPDATED vX.Y.Z**.
- If `last_content_update` has changed since step 0 (another machine updated it this cycle), do **not** make a second content update. Log evidence only.

## 4b. Year count (automatic, patch only)

1. Compute whole years from the career start in `RULES.md` ("Your settings") to today.
2. If the summary in `resume/resume.yml` states a different total ("N years across…"):
   - change only that number
   - bump the patch version
   - add a changelog entry ("Year count N-1 → N, from careerStart; auto-released per RULES.md")
   - build
3. After pushing (step 5), auto-release the new version **only if** nothing else is unreleased. That means `released/VERSION` must equal the version right before this bump. If so, run `gh workflow run resume.yml -f release_version=<new version>` from the credentialed shell. If other changes are still waiting for approval, don't release; list it in the report instead.
4. If "nearly four years" (AWS/GCP) no longer reads true, don't change it. Ask in the report.

## 5. Commit and push

1. Set `machines[<hostname>]` in `resume/state.yml` to today.
2. Commit evidence, state, and any resume changes in one commit:
   - message: `chore(resume): monthly review <hostname> <date>` or `feat(resume): vX.Y.Z — <short reason>`
 3. Run `git pull --rebase`, then `git push`. On a rebase conflict in `evidence/log.md` or `state.yml`, keep both sides' entries, then continue. Retry the push up to 3 times.
4. Never force-push. Never touch `released/` or the `released` tag; only you approve releases. Pushing to `main` lets CI tag the version and refresh the `latest` pre-release.

## 6. Mirror to Obsidian

Run `python3 resume/sync_obsidian.py`. It skips cleanly if there's no vault (`$OBSIDIAN_VAULT`, default `~/Obsidian_Vault`).

## 6b. Content suggestions (report only, never auto-publish)

Using this month's evidence plus what's already on the site, suggest up to **two** items, each with a one-line pitch and the evidence IDs behind it:
- **Blog post ideas:** a completed piece of work with a lesson worth sharing. If you keep a blog, check its posts and drafts first so you don't repeat a topic.
- **Project / case study:** a new project write-up, or an update to an existing one.
- **Stale copy:** anything on your site or profiles that no longer reads true, if you keep a site in this repo.

Never write or publish blog posts, and never edit site copy, in this run. You pick what to pursue. Say "No suggestions this month" when nothing qualifies. A thin month shouldn't produce filler.

## 7. Report (final reply, kept short)

- Result: NO_UPDATE | UPDATED vX.Y.Z | BLOCKED
- Window reviewed, sources searched, and sources unavailable
- New evidence entries: one line each
- If updated: the before/after lines
- Items needing your confirmation, phrased as yes/no questions
- Content suggestions from step 6b
- Year count: unchanged, or bumped to N (released / waiting on pending approval)
- If updated: "To approve it for general use: GitHub → Actions → Resume → Run workflow → version X.Y.Z."
