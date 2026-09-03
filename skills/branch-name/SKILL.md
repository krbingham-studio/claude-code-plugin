---
name: branch-name
description: Use when creating a git branch or asked what to call one. Produces a branch name carrying the Jira ticket key, which is where the commit message, the PR title and the ticket link all get theirs from.
---

# branch-name

The branch name is where the ticket key enters the workflow. `commit-message`,
`pr-title` and `testing-evidence` all read it from here first, so getting it
right once saves asking three times.

```
<type>/<TICKET>-<short-slug>
```

`feat/ABC-123-refresh-token-rotation`

- **type** — the same vocabulary as a commit type: `feat`, `fix`, `chore`,
  `docs`, `refactor`, `test`. Some teams use `feature/` and `bugfix/`; match
  what the repository already has.
- **TICKET** — the Jira key, uppercase, exactly as Jira writes it. Uppercase
  matters: the `[A-Z][A-Z0-9]+-[0-9]+` match the other skills use will not find
  `abc-123`.
- **slug** — two to five words, lowercase, hyphen-separated. Enough to
  recognise the branch in a list without opening it.

Keep it under about 50 characters in total. Long branch names get truncated in
every UI that shows them.

## Getting the key

Ask if you do not have one, or find it in the Jira tooling if the work is
already ticketed. **Never invent a key** — a branch named for a ticket that
does not exist propagates into every commit and the PR title before anyone
notices.

Without a ticket, drop that field: `chore/tidy-release-scripts`. Do not write a
placeholder; a literal `NO-TICKET` or `ABC-000` in a branch name will be
matched as a key by the other skills and copied faithfully into a commit.

## Rules

- **Check the repository's convention first.** `git branch -a` or the recent
  merge history. An established pattern wins; say so rather than introducing a
  second scheme.
- **Branch from the up-to-date base**, not from whatever is checked out.
  `git fetch` first.
- One branch, one ticket. A branch covering three tickets cannot be named, and
  that is the naming problem telling you something about the change.
- Never rename or force-push a branch someone else may have pulled.
