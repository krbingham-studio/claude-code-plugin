---
name: jira-transition
description: Move a Jira ticket's status at the natural points in its lifecycle — starting work, opening a PR, merging. Always confirms with the user before applying a transition; never guesses a workflow status name.
---

Move a Jira ticket to the status that matches what just happened to the work
it tracks, without assuming every project's workflow uses the same status
names.

## When this applies

- Starting work on a ticket (branch created via `branch-name`, or the user
  says they're picking it up).
- Opening a PR for it (after `pr-title` drafts the PR).
- The PR merging, or `testing-evidence` posting a passing result.
- The user explicitly asks to move a ticket.

This skill does not run on its own schedule — it's invoked at these points,
not polled for. It's the transition half of what `testing-evidence` deliberately
stops short of: that skill posts evidence to a ticket but leaves moving the
lane to this one, so the two don't race each other on the same issue.

## Steps

### 1. Identify the ticket

Resolve the ticket key the same way `commit-message` does (branch name, recent
commits, Jira tooling, or ask). Never transition a ticket the user hasn't
confirmed is the right one.

### 2. Fetch the real transitions

Call `getTransitionsForJiraIssue` for that ticket rather than assuming
status names like "In Progress" or "Done" exist — workflows differ per
project, and a project might use "In Dev", "Doing", "Review", or something
else entirely.

### 3. Match the event to a transition

Pick the transition whose name best matches what happened:

| Event         | Look for a transition named like               |
| ------------- | ---------------------------------------------- |
| Starting work | "In Progress", "In Dev", "Start"               |
| PR opened     | "In Review", "Code Review", "Ready for Review" |
| PR merged     | "Done", "Closed", "Ready for QA", "Resolved"   |

If nothing in the fetched list is a clear match, say so and ask the user
which transition to apply rather than picking the closest-sounding one —
a wrong status is worse than no status change, since it misleads whoever
looks at the board next.

### 4. Confirm before applying

State the ticket key, its current status, and the transition about to be
applied, and get an explicit go-ahead before calling
`transitionJiraIssue`. A status change is visible to everyone watching that
board — the same reasoning `create-ticket` applies to issue creation.

### 5. After transitioning

Confirm the new status back to the user. If a comment would help (e.g. the
PR link, or why a ticket skipped a stage), offer to add one with
`addCommentToJiraIssue` rather than adding it unasked.

## Notes

- Never transition a ticket backward (e.g. "Done" back to "In Progress")
  without the user explicitly asking for that — forward-only unless told
  otherwise.
- If the ticket is already in the target status, say so and do nothing;
  don't re-fire the same transition.
