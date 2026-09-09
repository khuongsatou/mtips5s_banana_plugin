#!/usr/bin/env python3
"""Build a disposable Codex plugin package for one Banana environment."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any

from env_config import resolve_config


SCRIPT_DIR = Path(__file__).resolve().parent
PLUGIN_ROOT = SCRIPT_DIR.parent


def build_plugin(
    environment: str,
    output: str | Path,
    *,
    port: int | None = None,
    base_url: str | None = None,
) -> Path:
    destination = Path(output).resolve()
    source = PLUGIN_ROOT.resolve()
    if destination == source or source in destination.parents:
        raise ValueError("output must not be inside the source plugin")
    if destination.exists():
        raise FileExistsError(f"output already exists: {destination}")

    values = {"BANANA_PRO_ENV": environment}
    if base_url is not None:
        values["BANANA_PRO_BASE_URL"] = base_url
    if port is not None:
        values["BANANA_PRO_DEV_PORT"] = str(port)
    config = resolve_config(values)

    shutil.copytree(
        source,
        destination,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )
    mcp_path = destination / ".mcp.json"
    mcp: dict[str, Any] = {
        "mcpServers": {
            "banana-pro": {
                "type": "http",
                "url": config.mcp_url,
            }
        }
    }
    mcp_path.write_text(json.dumps(mcp, indent=2, ensure_ascii=False) + "\n")
    if not (destination / ".codex-plugin/plugin.json").is_file():
        raise RuntimeError("generated package is missing plugin manifest")
    if environment == "production" and config.mcp_url != "https://bb.1nutnhan.com/mcp":
        raise RuntimeError("production package must use the production MCP URL")
    return destination


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--environment", choices=("production", "dev"), default="production")
    parser.add_argument("--port", type=int)
    parser.add_argument("--base-url")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    result = build_plugin(
        args.environment,
        args.output,
        port=args.port,
        base_url=args.base_url,
    )
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
