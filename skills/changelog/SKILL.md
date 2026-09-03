---
name: changelog
description: Draft a CHANGELOG.md entry from commits since the last tag, grouped and keyed to Jira tickets. Checks for semantic-release or similar automation first and defers to it rather than fighting it.
---

Write a changelog entry for the commits since the last release, but only
where nothing already does this automatically.

## Step 0 — check whether this repo already automates it

Several studio repos run `semantic-release` (or an equivalent) in CI, which
generates `CHANGELOG.md` from Conventional Commit messages on every merge to
main — exactly the format `commit-message` already produces. Writing a
manual entry on top of that duplicates it and can conflict with what CI is
about to overwrite.

Before drafting anything, check for:

- `semantic-release` (or `@semantic-release/*`) in `package.json`
- a `.releaserc*` or `release.config.*` file
- a `release-please-config.json`, or a `release-please` GitHub Action

If any of these are present, say so, and either stop (nothing to do — CI
handles it) or, if the user specifically wants a preview, describe what the
next automated entry would contain rather than writing it into the file
yourself.

If none are present, continue below.

## Steps (manual repos only)

1. Find the last release point: the most recent tag (`git describe --tags
--abbrev=0`), or if there is none, the repo's first commit.
2. List commits since then: `git log <last-tag>..HEAD --oneline`.
3. Group by `commit-message`'s type prefix:
   - `feat` → **Added**
   - `fix` → **Fixed**
   - `refactor`, `perf`, `style`, `chore`, `build`, `ci` → **Changed**
   - `docs` → **Documentation**
   - `revert` → **Reverted**

   Drop merge commits and anything with no type prefix — flag those instead
   of guessing a category, since a stray commit is more often noise than a
   miscategorized change.

4. Write entries in [Keep a Changelog](https://keepachangelog.com) style:
   one bullet per commit's subject line (cleaned up to read as a sentence),
   with the ticket key kept visible, e.g.:
   ```
   ## [Unreleased]

   ### Added
   - Retry login on token expiry (ENG-42)

   ### Fixed
   - Correct off-by-one in pagination (ENG-51)
   ```
5. Prepend the new section to `CHANGELOG.md` (create the file, with this
   same heading style, if it doesn't exist yet).
6. Show the drafted section to the user before writing it — this touches a
   file that ships to whoever reads the repo's history.

## Notes

- Never invent a version number here; leave the section headed
  `[Unreleased]` and let versioning be a separate, deliberate step.
- If a commit's ticket key can't be found (predates this convention, or was
  never scoped), include the entry without one rather than blocking the
  whole changelog on it.
