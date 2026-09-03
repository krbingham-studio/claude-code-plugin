#!/usr/bin/env python3
"""Validate the plugin manifest, agents and skills for this repo."""
import glob
import json
import sys

import yaml

errors = []


def fail(msg):
    errors.append(msg)


def load_frontmatter(path):
    text = open(path, encoding="utf-8").read()
    if not text.startswith("---\n"):
        fail(f"{path}: missing YAML frontmatter (must start with '---')")
        return None
    try:
        end = text.index("\n---", 4)
    except ValueError:
        fail(f"{path}: frontmatter not terminated with '---'")
        return None
    try:
        data = yaml.safe_load(text[4:end])
    except yaml.YAMLError as e:
        fail(f"{path}: invalid YAML frontmatter ({e})")
        return None
    if not isinstance(data, dict):
        fail(f"{path}: frontmatter did not parse to a mapping")
        return None
    return data


def check_manifest():
    path = ".claude-plugin/plugin.json"
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        fail(f"{path}: file not found")
        return
    except json.JSONDecodeError as e:
        fail(f"{path}: invalid JSON ({e})")
        return

    for field in ("name", "version", "description"):
        if not data.get(field):
            fail(f"{path}: missing required field '{field}'")

    name = data.get("name")
    if name and (name != name.lower() or " " in name):
        fail(f"{path}: 'name' should be lowercase, hyphen-separated ({name!r})")


def check_entries(pattern, kind, name_from_path):
    seen = {}
    for path in sorted(glob.glob(pattern)):
        fm = load_frontmatter(path)
        if fm is None:
            continue
        for field in ("name", "description"):
            if not fm.get(field):
                fail(f"{path}: {kind} frontmatter missing '{field}'")

        name = fm.get("name")
        expected = name_from_path(path)
        if name and expected and name != expected:
            fail(f"{path}: frontmatter name '{name}' does not match path (expected '{expected}')")

        if name:
            if name in seen:
                fail(f"{path}: duplicate {kind} name '{name}' (already used by {seen[name]})")
            else:
                seen[name] = path


def main():
    check_manifest()
    check_entries(
        "agents/*.md",
        "agent",
        lambda p: p.split("/")[-1].removesuffix(".md"),
    )
    check_entries(
        "skills/*/SKILL.md",
        "skill",
        lambda p: p.split("/")[-2],
    )

    if errors:
        print(f"Found {len(errors)} problem(s):\n")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)

    print("All manifest, agent and skill files are valid.")


if __name__ == "__main__":
    main()
