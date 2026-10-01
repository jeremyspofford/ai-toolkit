---
name: evidence-capture
description: At the end of a work session, record what was actually completed (not suggested or planned) as a sanitized entry in a resume evidence log. Use when the user says "log this", "capture evidence", "anything resume-worthy?", or wraps up a substantial session.
---

# Evidence capture

Keep an honest, append-only record of real accomplishments so resume updates never rely on memory or guesswork.

## 1. Load config

Read `resume.evidence_log` from `~/.config/ai-toolkit/config.yml`. If it's missing, ask where the log should live and offer to save it. If the file doesn't exist, create it with the header from step 4.

## 2. Separate what was done from what was discussed

Review the conversation and sort everything into three buckets:
- **Completed:** the user did it, deployed it, merged it, or confirmed it worked.
- **Suggested:** you (the assistant) proposed, drafted, or scripted it, and the user hasn't confirmed they used it. **This does not count.**
- **Unfinished:** started but not done, or the outcome is unknown.

Only "completed" items become entries. If an item's status or outcome is unclear, ask one direct question. If it's still unclear, log it with `status: needs-confirmation`.

## 3. Rate materiality

- **major:** a completed platform or migration, new ownership, a measured cost/reliability/security result, a certification, or a role change
- **meaningful:** a distinct completed improvement that adds real scope or depth
- **minor:** routine fixes, single resource edits, research, rewording

Minor items don't get entries unless they're part of something larger.

## 4. Write the entry

Append, never rewrite. If the same accomplishment is already logged, add this session as another `source` on that entry instead of creating a duplicate.

```markdown
# Evidence log   ← header, only when creating the file

### E-YYYYMMDD-<short-slug>
- date: YYYY-MM-DD (when the work completed)
- source: chat YYYY-MM-DD | git <repo nickname> | jira
- context: <employer>, <generic client type, e.g. "a manufacturing client"> | personal
- what: <what the user actually did>
- outcome: <supported result, or "none stated">
- metric: <exact number and how it was measured, or none>
- status: completed | needs-confirmation
- materiality: major | meaningful | minor
- disposition: pending
```

Sanitize every entry: no client names, internal URLs, hostnames, account IDs, ticket numbers, or confidential figures.

If nothing qualifies, reply exactly: "No resume evidence to capture."
