# Banana Pro Codex

Plugin local cho Codex, kết nối Banana Pro qua BB API và MCP.

## Cấu hình

- API base mặc định: `https://bb.1nutnhan.com`
- Health: `/api/health`
- MCP: `/mcp` khi gateway được bật
- MCP key: biến môi trường `BANANA_PRO_MCP_API_KEY`
- Đổi API base bằng `BANANA_PRO_BASE_URL`

Không đặt token trực tiếp trong plugin, manifest, prompt hoặc log. Trước generation phải health check và confirmation; sau generation phải QA output.

