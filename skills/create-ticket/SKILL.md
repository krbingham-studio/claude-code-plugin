---
name: create-ticket
description: Create a Jira ticket in a fixed shape — always asks which project, always links an epic. Use whenever a new Jira issue is about to be created, not only when the user says the word "ticket".
---

Create a new Jira issue. Every issue created under this skill has a project
the user confirmed and an epic it belongs to — neither is ever assumed.

## Steps

### 1. Ask which project

Never infer the Jira project from context (repo name, prior tickets in the
conversation, etc.) without confirming it with the user first. If they
haven't named one, list the visible projects (`getVisibleJiraProjects`) and
ask which it goes in. A wrong-project ticket is expensive to notice and fix
later — confirming costs one question.

### 2. Resolve the epic

Every ticket created under this skill links to an epic. Do not create an
issue with no epic and do not invent one.

- If the user named an epic, confirm it exists in the chosen project
  (`searchJiraIssuesUsingJql`, `getJiraIssue`).
- If they didn't, search the project's open epics and ask which one this
  belongs to.
- If no existing epic fits, say so and ask whether to create a new epic
  first (`createJiraIssue` with issue type Epic) or file the ticket under an
  existing catch-all epic if the project has one. Do not silently create the
  ticket without an epic while waiting for an answer — stop and ask.

### 3. Pick the issue type

Ask or infer from the request (bug report vs. new work vs. task) which issue
type fits, then fetch that type's required fields for the project
(`getJiraIssueTypeMetaWithFields`) so the create call doesn't fail on a
missing mandatory field partway through.

### 4. Draft the ticket

- **Summary** — short, specific, imperative (`Retry login on token expiry`,
  not `Login bug`).
- **Description** — structured, not a single paragraph:
  - **Problem / context** — what's wrong or what's needed, and why now.
  - **Acceptance criteria** — a bullet checklist of what "done" means.
  - **Notes** — links, related tickets, technical constraints, out-of-scope
    items, if any.
- **Epic Link** — the epic resolved in step 2.
- Labels/components only if the user asks for them or the project's
  convention makes one obvious (e.g. everything in this project gets a
  component matching the affected service).

### 5. Confirm before creating

Show the drafted summary, description, project, epic, and issue type to the
user. Creating a Jira issue is a visible, shared-state action — get an
explicit go-ahead before calling `createJiraIssue`.

### 6. After creating

Report the new ticket's key and a link back to the user. If work on it is
about to start, name the branch for it with `branch-name` — that's where
`commit-message`, `pr-title` and `testing-evidence` all read the key back
out from.
