# Evidence log

Sanitized record of work that could matter for the resume. Append-only: never delete entries, mark them `included` or `excluded` instead.
Rules: see `../RULES.md`. No client names, internal URLs, hostnames, ticket numbers, or confidential figures.

Entry format (the ai-toolkit `evidence-capture` skill writes these for you):

```
### E-YYYYMMDD-<short-slug>
- date: YYYY-MM-DD (when the work completed)
- source: git <repo-nickname> | worklog | jira | chat YYYY-MM-DD
- machine: <hostname that recorded it>
- context: <employer>, <generic client type> | personal
- what: <what you actually did>
- outcome: <supported result; "none stated" if none>
- metric: <exact number and its basis, or none>
- status: completed | needs-confirmation
- materiality: major | meaningful | minor
- disposition: pending | included vX.Y.Z | excluded (<reason>) | duplicate of E-…
```

## Entries
