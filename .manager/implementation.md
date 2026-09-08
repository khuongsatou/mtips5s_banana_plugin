# Implementation Notes

- Đã tạo cấu trúc `.agent/roles`, `.agent/skills`, `.agent/rules`, `.agent/workflows`.
- Đã tạo state files trong `.manager/`.
- Đã bootstrap feedback loop trong `.feedback/`.
- Bảo toàn toàn bộ file hiện có; dự án chưa có các thư mục này trước khi bootstrap.
- Đã tạo plugin `plugins/banana-pro-codex` với manifest, MCP config, 6 skills, scripts và assets.
- Đã liên kết MCP `https://bb.1nutnhan.com/mcp` và BB API health/generation/upload contracts.
- Đã tạo docs root, architecture/interaction/input-output references và plugin contract tests.
