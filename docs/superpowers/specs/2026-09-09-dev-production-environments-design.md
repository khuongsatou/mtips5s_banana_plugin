# Banana Pro Dev/Production Environments Design

## Goal

Tách cấu hình Banana Pro thành hai môi trường `production` và `dev`, trong đó production luôn là mặc định của plugin khi release và cài vào Codex Desktop.

## Decisions

- Production base URL: `https://bb.1nutnhan.com`.
- Production MCP URL: `https://bb.1nutnhan.com/mcp`.
- Dev base URL: `http://127.0.0.1:<port>`.
- Dev MCP URL: `http://127.0.0.1:<port>/mcp`.
- Port dev mặc định: `8000`, có thể thay bằng `BANANA_PRO_DEV_PORT` hoặc cờ CLI tương ứng.
- Không có cấu hình môi trường: resolve production.
- Chỉ `BANANA_PRO_ENV=dev` mới được phép chọn loopback.
- `.mcp.json` trong source plugin luôn là production config để package mặc định an toàn.
- Dev package được build vào `dist/dev`; production package được build vào `dist/production`.
- Không lưu token/API key trong config, package, log hoặc test fixture.

## Architecture

Một resolver Python dùng chung sẽ chuẩn hóa environment, base URL, MCP URL và port. Các script shell, PowerShell và health profile gọi resolver thay vì tự đặt default riêng. Build script tạo bản package theo profile bằng cách copy plugin và ghi `.mcp.json` tương ứng; source tree vẫn giữ production `.mcp.json`.

## Safety Rules

1. `production` là fallback duy nhất khi biến môi trường bị thiếu hoặc rỗng.
2. Dev chỉ chấp nhận host `127.0.0.1` và port TCP hợp lệ từ `1` đến `65535`.
3. Production không nhận port dev và không được trỏ tới loopback.
4. URL phải dùng `http` hoặc `https`, không cho phép userinfo, query hoặc fragment.
5. Health output chỉ được in URL không nhạy cảm và các cờ `ok`, `extension_ready`, `flow_key_present`.
6. Release validation phải fail nếu package production có MCP URL localhost.

## Verification

Unit tests kiểm tra resolver, URL validation, script propagation, generated MCP configs, production release guard và backward compatibility của `connect.sh`, `connect.ps1`, `host_profile.py`. Release verification chạy toàn bộ `python3 -m unittest discover -s tests -v` và build dry-run cho cả hai profile.
