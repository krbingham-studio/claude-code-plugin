---
name: repo-setup
description: Bring a new or existing JS/TS repo up to the studio's baseline tooling — mise.toml for pinned tool versions, pnpm as the package manager, commitlint enforcing the commit-message skill's Conventional Commits format, and Prettier. Use when initializing a new repo, or when asked to standardize an existing one.
---

# repo-setup

Wire in the tooling that makes the studio's conventions enforced rather than
just documented. `commit-message` describes the format; this skill is what
makes a bad commit message fail before it merges. Same idea for formatting
and tool versions: the standard only holds if the repo checks it.

## Step 0 — read before you write

Never lay this down blind. A repo with its own established tooling that
merely differs from the studio default is not broken — check first:

- `package.json` — existing `packageManager`, `scripts`, dependencies already
  covering formatting or commit linting.
- Lockfiles — `package-lock.json` or `yarn.lock` alongside (or instead of) a
  `pnpm-lock.yaml`. Two lockfiles for one repo is worse than one wrong one.
- `mise.toml`, `.nvmrc`, `.tool-versions`, `.python-version` — an existing
  pin wins over a default; don't silently retarget a version another repo or
  CI already depends on.
- `.prettierrc*`, `prettier.config.*`, `.editorconfig` — a formatting config
  that already differs from the studio default is a decision, not an
  oversight; ask before overwriting it.
- `.git/hooks`, `.husky/`, `commitlint.config.*`, `lefthook.yml` — existing
  hook tooling to extend rather than duplicate.

If something is already in place and equivalent, say so and move on rather
than adding a second way to do the same job.

## 1. `mise.toml` — pin the tool versions

Pin every runtime the repo actually uses — don't add languages it doesn't
need. Read what's already running: an existing `package.json` `engines`
field, a Dockerfile's base image, CI's current `setup-node`/`setup-python`
version.

```toml
[tools]
node = "20"
pnpm = "9"
```

Add `python`, `go`, etc. only if the repo uses them. Prefer a major version
(`"20"`) over a specific patch unless the repo has a reason to pin tighter —
a floating major stays current on `mise install`; an over-pinned patch goes
stale silently.

## 2. pnpm as the package manager

- Set `"packageManager": "pnpm@<version>"` in `package.json`, matching the
  version pinned in `mise.toml`, so `pnpm/action-setup` (or any Corepack-aware
  tool) resolves it without a separate config.
- If `package-lock.json` or `yarn.lock` exists, remove it and run
  `pnpm install` to generate `pnpm-lock.yaml` — flag the switch to the user
  first if the repo has other contributors, since it changes what they run
  locally.
- Add `node_modules/` to `.gitignore` if it isn't already there.
- In CI, install with `jdx/mise-action` (see below) then
  `pnpm install --frozen-lockfile` — never a bare `pnpm install`, which can
  silently update the lockfile in CI.

## 3. Commit linting

Enforce the format `commit-message` already describes, rather than leaving it
as a convention nobody checks.

- `pnpm add -D @commitlint/cli @commitlint/config-conventional husky`
- `commitlint.config.js`:
  ```js
  module.exports = { extends: ["@commitlint/config-conventional"] };
  ```
- Wire a `commit-msg` hook via `husky` (`pnpm exec husky init`, then have the
  generated hook run `pnpm exec commitlint --edit "$1"`) so a malformed commit
  fails locally, not just in review.
- Add a CI step (or job) that runs `pnpm exec commitlint --from <base> --to
HEAD` on pull requests, so a commit pushed with `--no-verify` still gets
  caught.
- This checks _shape_ (type, casing, line length) — it can't verify the Jira
  key is real or that the summary matches the diff. That part is still
  `commit-message`'s job, applied by whoever writes the commit.

## 4. Prettier

- `pnpm add -D prettier`
- A `.prettierrc` at the repo's default settings unless the repo's existing
  code implies otherwise (tab width, quote style already in use — match it
  rather than reformatting the whole tree as a side effect of this setup).
- `.prettierignore` covering build output, lockfiles, and anything generated.
- `package.json` scripts: `"format": "prettier --write ."` and
  `"format:check": "prettier --check ."`.
- Run formatting on staged files at commit time via `lint-staged` +
  `husky`'s `pre-commit` hook, rather than reformatting the whole repo on
  every commit:
  ```json
  { "lint-staged": { "*.{js,jsx,ts,tsx,json,md}": "prettier --write" } }
  ```
- A CI step running `pnpm exec prettier --check .` so an unformatted file
  still fails the build if a hook was skipped.

## 5. Wire it into CI

Use `jdx/mise-action` to install the pinned versions from `mise.toml` in one
step, rather than a separate `setup-node`/`setup-python`/`pnpm/action-setup`
per tool — see this repo's own `.github/workflows/*.yml` for the pattern:

```yaml
- uses: actions/checkout@v4
- uses: jdx/mise-action@v2
- run: pnpm install --frozen-lockfile
- run: pnpm exec prettier --check .
- run: pnpm exec commitlint --from ${{ github.event.pull_request.base.sha }} --to HEAD
```

## Before finishing

- Run what you just wired up — `pnpm exec prettier --check .`, a deliberately
  malformed commit message against the hook — and show the actual output,
  not just that the files exist.
- List what was added or changed, and anything found in Step 0 that was left
  alone because it already met the standard.
