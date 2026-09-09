#!/usr/bin/env node
"use strict";

const fs = require("node:fs");
const path = require("node:path");
const { spawnSync } = require("node:child_process");

const scriptName = "auto-refresh-youtube-workflows.cjs";
const candidates = [
  process.env.BANANA_PRO_AUTO_REFRESH_SCRIPT,
  process.env.BANANA_PRO_REPO_ROOT && path.join(process.env.BANANA_PRO_REPO_ROOT, "scripts", scriptName),
  "/opt/banana-pro/scripts/auto-refresh-youtube-workflows.cjs",
].filter(Boolean);
const target = candidates.find((candidate) => fs.existsSync(candidate));

if (!target) {
  console.error(`Cannot find ${scriptName}. Set BANANA_PRO_AUTO_REFRESH_SCRIPT or BANANA_PRO_REPO_ROOT.`);
  process.exit(1);
}

const result = spawnSync(process.execPath, [target, ...process.argv.slice(2)], {
  cwd: process.env.BANANA_PRO_REPO_ROOT || path.dirname(path.dirname(target)),
  env: process.env,
  stdio: "inherit",
});

if (result.error) throw result.error;
process.exitCode = result.status === null ? 1 : result.status;
