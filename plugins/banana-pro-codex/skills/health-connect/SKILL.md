---
name: banana-pro-health-connect
description: Kiểm tra và kết nối Banana Pro BB API/FlowKit.
---
# Health & Connect

Trigger khi người dùng yêu cầu check, status, connect, models hoặc chẩn đoán Banana Pro.

1. Gọi read-only `scripts/connect.sh` hoặc `connect.ps1`.
2. READY chỉ khi `ok`, `extension_ready`, `flow_key_present` đều true.
3. Nếu dùng MCP, kiểm tra `https://bb.1nutnhan.com/mcp`. Plugin dùng OAuth + PKCE; nếu Codex báo chưa xác thực thì yêu cầu chạy luồng đăng nhập MCP, không yêu cầu người dùng dán API key thủ công.
4. Không cài đặt, download model, restart runtime hoặc in secret.
5. Báo rõ `healthy`, `offline`, `missing extension` hoặc `missing flow key`.

Base URL dùng `BANANA_PRO_BASE_URL`, mặc định là domain BB production.
