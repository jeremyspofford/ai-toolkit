---
name: jira
description: Jira + git workflows through an Atlassian connector. Create issues with acceptance criteria, start work on an issue (branch from the base branch and move it to In Progress), or update an issue (status, comments, fields, recent commits). Use for "create a ticket", "start PROJ-201", "move this to done", "comment on the ticket", or a bare issue key.
---

# Jira workflows

Requires an Atlassian (Jira) connector or MCP server. If none is available, say so and stop.

## Config

Read the `jira` section of `~/.config/ai-toolkit/config.yml`:
- `site`
- `default_project`
- `projects`
- `base_branch`
- `branch_pattern`
- `in_progress_status`

If it's missing, ask for the site and project key, assume `origin/main` and `{key-lower}-{slug}`, and offer to save the answers.

**Resolving the issue key:**
- Accept `PROJ-201`, `proj-201`, or a bare `201`. A bare number gets `default_project`.
- If no key is given, infer it from the current branch name using `branch_pattern`. Otherwise ask.

## Workflow: create-issue

1. From the user's description, draft:
   - a summary (an imperative phrase)
   - a description: the problem or context, then the desired outcome
   - **acceptance criteria** as a checklist of observable, testable conditions. Always include them.
2. Pick the issue type (Task, Bug, or Story) from the wording. Check required fields with the connector's issue-type metadata.
3. Show the draft and confirm before creating. Then create it and return the key and link.

## Workflow: start-branch

1. Get the issue and show its summary and status.
2. `git fetch`, then create the branch from `base_branch` using `branch_pattern`. The slug is the summary in lowercase kebab-case, at most about 6 words. If the branch already exists, check it out instead.
3. Transition the issue to `in_progress_status` if that transition is available. If it isn't, list the available transitions and ask.
4. Report the branch name and the new status.

## Workflow: update-issue

- **Status:** get the available transitions and pick the one matching the user's words ("done", "in review"). If it's ambiguous, ask.
- **Comment:** write in plain language. To summarize recent work, use `git log <base_branch>..HEAD --oneline` plus the substance of the diffs, not just commit subjects.
- **Fields:** assignee, labels, story points, and so on. Check field metadata first.

Confirm before any change someone else will see (transitions, comments). Report what changed, with the issue link.
