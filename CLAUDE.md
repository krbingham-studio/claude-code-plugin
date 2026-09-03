# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A Claude Code plugin package. It has no build step, no package manifest, and no test suite — it's plain declarative content that Claude Code loads directly.

## Structure

- `.claude-plugin/plugin.json` — plugin manifest (name, version, description, author)
- `commands/` — custom slash commands
- `agents/` — subagent definitions
- `skills/` — skills
- `hooks/` — hook scripts

All four content directories are currently empty placeholders (`.gitkeep`). Each command, agent, and skill should live in its own file under the matching directory, per the [Claude Code plugin docs](https://docs.claude.com/en/docs/claude-code/plugins).

## Installation

Add this repo as a plugin source in Claude Code and install `claude-code-plugin`.
