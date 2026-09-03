---
name: testing-evidence
description: Use after testing or verifying a change that has a Jira ticket — posts the evidence (commands run, real output, environment, what was and was not covered) as a comment on the issue. Use when asked to record, attach or upload test results, or when moving a ticket to review or QA.
---

# testing-evidence

Put the proof where the person deciding will look for it: a comment on the Jira
issue. A verification that lives only in a terminal scrollback is a verification
nobody else can act on.

## What a comment must contain

1. **What was tested** — the change, in one line, and the ticket it belongs to.
2. **The exact commands**, copyable, in the order they were run.
3. **Their real output.** Trimmed to the relevant part, never paraphrased and
   never reconstructed from memory.
4. **Where it ran** — branch and commit SHA, environment (local, container, CI,
   staging), and anything about it that would change the result.
5. **The result**, stated plainly: what passed, what failed, what is still red
   and why.
6. **What this does _not_ cover.** The single most valuable line in the comment
   — an untested path that nobody flags reads as a tested one.

## Format

Use a code block for anything machine-produced, so it survives Jira's
formatting:

```
{code}
$ make test
✓ 42 tests, 0 failures
{code}
```

Keep prose short and the evidence long. A summary sentence, then the blocks.

## Getting it onto the ticket

- Find the key from the branch name, then the commits, then ask. **Never invent
  one** — evidence on the wrong ticket is worse than evidence nowhere, because
  it will be believed.
- Read the issue first (`getJiraIssue`) to confirm it is the right one and to
  see what has already been posted. Do not post the same evidence twice; a
  re-run after a fix is a new comment that says what changed.
- Post with the Jira tooling's add-comment operation. This needs the Atlassian
  MCP server configured — if it is not available, say so and hand the formatted
  comment back for pasting rather than silently dropping it.
- **Transitioning the ticket is a separate decision** and belongs to the
  `jira-pm` agent. Posting evidence is not moving a lane.

## Never

- **Never fabricate output.** Not a plausible-looking test summary, not a
  tidied-up version of what you remember, not "should print". If you did not
  run it, say you did not run it.
- **Never post secrets or personal data.** Tokens, keys, connection strings,
  customer names and email addresses routinely appear in logs and Jira is
  broadly readable inside an org. Redact before posting, and redact by removing
  rather than by masking a value whose length gives it away.
- **Never present a partial run as a full one.** "3 of 5 suites, the other two
  need a database" is useful; "tests pass" is not, and is wrong.
- Never attach a large log wholesale. Link to the CI run and quote the part
  that matters.

## When the tests failed

Post it anyway, promptly. A failure recorded on the ticket is the fastest route
to somebody who can fix it; a failure held back until it is fixed is a day
nobody else knew. Say what failed, the output, and what you are doing about it.
