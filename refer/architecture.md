# Plugin Architecture

Codex → skill router → MCP/API → Banana Pro → output/QC.

- Plugin manifest: `plugins/banana-pro-codex/.codex-plugin/plugin.json`.
- MCP config: `plugins/banana-pro-codex/.mcp.json`.
- API scripts: `plugins/banana-pro-codex/scripts/`.
- Skills: health, generation, editing, media workflow, QA.
- Environment resolver: `plugins/banana-pro-codex/scripts/env_config.py`.
- Codex Desktop release mặc định build profile production; dev package dùng `127.0.0.1:<port>` và được tạo riêng.
- Public metadata không chứa model backend, hardware, token hoặc dữ liệu người dùng.
