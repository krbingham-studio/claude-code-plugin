---
name: commit-message
description: Use whenever writing a git commit message — before every `git commit`, when amending, or when asked for a message for staged work. Produces a Conventional Commits message carrying the Jira ticket key when one applies.
---

# commit-message

Write the message to the Conventional Commits format, with the Jira ticket key
in it whenever the work has one.

```
<type>(<scope>): <summary> (<TICKET>)

<body>

<footers>
```

`feat(cms): include block-demo-page in the Pages grouping (WEB-321)`

## The parts

**type** — one of `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`,
`build`, `ci`, `chore`, `revert`. Pick by what the change _does_ to the
product, not by which files moved: a refactor that fixes a bug is a `fix`.

**scope** — the component or area, lowercase, optional. Use one the repository
already uses; read `git log` rather than inventing a taxonomy.

**summary** — imperative mood, lowercase, no full stop. "include block-demo-page
in the Pages grouping", not "added" or "adds". Say what the change does, not
which function you touched. Keep the whole header line — type, scope, summary
and the ticket in parens — under ~72 characters.

**TICKET** — the Jira key, `(WEB-321)`, in parentheses at the end of the
description. Jira links a commit to an issue by finding the key anywhere in the
message; putting it last keeps the summary reading as a sentence and the key
still shows up in a one-line `git log --oneline`.

**body** — only when the _why_ is not obvious. What was happening before, what
decided this approach, what you rejected. Wrap at 72 columns. The diff already
says what changed; the body is the part a reader cannot reconstruct.

**footers** — `BREAKING CHANGE: <what and how to migrate>` for anything that
breaks a caller. `Refs: ABC-124` for tickets the change relates to but does not
implement.

## Finding the ticket key

In order, stopping at the first that answers:

1. **The branch name.** `feature/ABC-123-refresh-tokens` → `ABC-123`. Match on
   `[A-Z][A-Z0-9]+-[0-9]+`.
2. **Recent commits on this branch.** `git log -n 20 --format=%s` — the key is
   almost always already there.
3. **The Jira tooling**, if a ticket is identifiable from the work itself.
4. **Ask.** One question, once.

**Never invent a key, and never carry one over from an unrelated branch.** A
wrong key silently attaches this work to somebody else's ticket, which is worse
than no key at all — nobody goes looking for a link that appears to exist.

When there is genuinely no ticket — a hotfix, a personal repo, a chore nobody
raised — omit it and write the rest of the message normally. Do not write
`NO-TICKET` or a placeholder.

## Before writing, read the repository

**A repository's established style wins over this format.** Run
`git log --oneline -n 20` first. If the history plainly uses something else —
sentence-case summaries with no type prefix, a different key position, gerunds —
say so and ask which to follow rather than silently switching the project to
Conventional Commits in one commit. A commit log is only useful while it is
consistent.

Also honour anything the project's own `CLAUDE.md`, `CONTRIBUTING.md` or commit
hooks specify. A `commit-msg` hook is the authority: match what it enforces.

## Rules

- **One commit, one change.** A refactor and a behaviour change in the same
  commit can only be reviewed as neither.
- **Never describe work you did not do.** The message describes the staged diff
  — check it with `git diff --cached` rather than writing from memory of the
  conversation.
- **No secrets in a message.** Tokens, keys and internal URLs are as permanent
  in a commit message as in a file, and harder to remove.
- Do not add attribution or tool footers unless the project asks for them.
