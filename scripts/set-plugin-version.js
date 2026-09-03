#!/usr/bin/env node
// Patches .claude-plugin/plugin.json's version field during semantic-release's
// prepare step, since it has no package.json for semantic-release to bump.
const fs = require("fs");
const path = require("path");

const version = process.argv[2];
if (!version) {
  console.error("Usage: set-plugin-version.js <version>");
  process.exit(1);
}

const manifestPath = path.join(
  __dirname,
  "..",
  ".claude-plugin",
  "plugin.json",
);
const manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
manifest.version = version;
fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2) + "\n");
console.log(`Updated ${manifestPath} to version ${version}`);
