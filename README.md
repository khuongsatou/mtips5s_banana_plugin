# Banana Pro Codex Plugin

Plugin local để Codex sử dụng Banana Pro qua BB API và MCP.

## Capabilities

Health/connect, text-to-image, image-to-image với upload bytes, media workflow, watermark removal và QA handoff.

## Watermark Remover

Workflow xóa watermark ưu tiên Banana MCP khi các tool đã được expose. Nếu MCP chưa khả dụng trong phiên, dùng BB API backend hoặc giao diện [Watermark Remover](https://bb.1nutnhan.com/watermark-remover/) làm fallback; luôn giữ file gốc và QA output trước khi bàn giao.

## Upscale

Workflow upscale ưu tiên Banana MCP khi các tool đã được expose. Nếu MCP chưa khả dụng trong phiên, dùng giao diện [Upscale](https://bb.1nutnhan.com/upscale) làm fallback và QA output trước khi bàn giao.

## Gemini Logo Remover

Skill `banana-pro-gemini-logo-remover` dùng workflow chỉnh sửa ảnh Gemini để xóa logo, giữ nguyên file gốc và QA output. Khi Gemini/MCP chưa khả dụng, dùng [Watermark Remover](https://bb.1nutnhan.com/watermark-remover/) làm fallback.

## Môi trường dev và production

Khi cài hoặc release vào Codex Desktop, plugin mặc định dùng production:
`https://bb.1nutnhan.com` và MCP `https://bb.1nutnhan.com/mcp`.

Dev chạy backend local trên loopback, mặc định port `8000`:

```bash
BANANA_PRO_ENV=dev bash plugins/banana-pro-codex/scripts/connect.sh
python3 plugins/banana-pro-codex/scripts/build_plugin.py --environment dev --output dist/dev
```

Đổi port dev bằng `BANANA_PRO_DEV_PORT=9123` hoặc `--port 9123`. Package release production:

```bash
python3 plugins/banana-pro-codex/scripts/build_plugin.py --environment production --output dist/production
```

Source `.mcp.json` luôn trỏ production; dev package được tạo riêng và không thay đổi cấu hình release.

## Cài đặt

Marketplace local nằm ở `.agents/plugins/marketplace.json`. Sau khi cài plugin, đặt key MCP ở biến môi trường `BANANA_PRO_MCP_API_KEY` nếu gateway yêu cầu.

API base mặc định: `https://bb.1nutnhan.com`. Không lưu token trong repository.
