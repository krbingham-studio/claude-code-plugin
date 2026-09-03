# Claude Code Plugin

A [Claude Code](https://docs.claude.com/en/docs/claude-code) plugin.

## Structure

- `.claude-plugin/plugin.json` — plugin manifest
- `commands/` — custom slash commands
- `agents/` — subagent definitions
- `skills/` — skills
- `hooks/` — hook scripts

## Installation

Add this repo as a plugin source in Claude Code and install `claude-code-plugin`.

## Development

Each command, agent, and skill lives in its own file under the matching directory. See the [Claude Code plugin docs](https://docs.claude.com/en/docs/claude-code/plugins) for authoring details.
