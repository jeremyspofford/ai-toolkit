# ai-toolkit

Practical Claude Code tools from a working DevOps engineer. They're the same ones I run every week, with my client details pulled out into a config file you fill in with yours.

| Tool | Kind | What it does |
|---|---|---|
| [Resume as Code](templates/resume-as-code) | Template | YAML resume → 2-page PDF, versioned releases, no-fabrication rules for AI help, monthly review procedure |
| [timecard](plugins/ai-toolkit/skills/timecard/SKILL.md) | Skill | Per-client, per-day work summary from git, Jira, and a work log |
| [tailor-resume](plugins/ai-toolkit/skills/tailor-resume/SKILL.md) | Skill | Role-specific resume from verified evidence only, plus a gap report |
| [evidence-capture](plugins/ai-toolkit/skills/evidence-capture/SKILL.md) | Skill | End-of-session log of what you actually shipped |
| [jira](plugins/ai-toolkit/skills/jira/SKILL.md) | Skill | Create with acceptance criteria, start a branch, update status |

Browse with examples: **[jeremyspofford.dev/toolkit](https://jeremyspofford.dev/toolkit)**

## Install the skills

```bash
claude plugin marketplace add jeremyspofford/ai-toolkit
claude plugin install ai-toolkit@jeremyspofford
```

Then run them as `/ai-toolkit:timecard`, `/ai-toolkit:tailor-resume`, and so on, or just describe what you want ("summarize my week for my timecard").

## Configure

```bash
mkdir -p ~/.config/ai-toolkit
curl -fsSL https://raw.githubusercontent.com/jeremyspofford/ai-toolkit/main/config.example.yml -o ~/.config/ai-toolkit/config.yml
```

Edit it with your workspace layout, the name and email variants your commits use, your Jira site, and so on. Each skill reads only its own section. If something is missing, it asks you and offers to save the answer. **Keep this file private:** it's where your client names live, not in the skills.

## Resume as Code

See [templates/resume-as-code](templates/resume-as-code) for setup. It's a repo template, not a skill.

## Design rules

- **Public code, private config.** Nothing in this repo knows who your clients are.
- **No fabrication.** The resume tools only use evidence you've confirmed, and they show their gaps.
- **Ask before anything other people see.** That covers Jira comments and status changes, and publishing.

MIT licensed.
