# Banana Pro Codex

Plugin local cho Codex, kết nối Banana Pro qua BB API và MCP, kèm workflow xóa watermark bằng model LaMa ONNX.

Tác giả / developer: **Sếp Khương**.

## Cấu hình

- API base mặc định: `https://bb.1nutnhan.com`
- Health: `/api/health`
- MCP: `/mcp` khi gateway được bật
- Xác thực MCP: OAuth + PKCE trong Codex; key `bbmcp_` được cấp tự động sau khi người dùng đăng nhập và chấp thuận
- Đổi API base bằng `BANANA_PRO_BASE_URL`

Khi cài plugin, Codex tự khám phá OAuth từ MCP server và mở trang đăng nhập Banana Pro. Mỗi lần kết nối tạo một key riêng cho Codex; người dùng có thể thu hồi key đó trong trang **MCP API Keys**.

Không đặt token trực tiếp trong plugin, manifest, prompt hoặc log. Trước generation phải health check và confirmation; sau generation phải QA output.

## Xóa watermark

Skill `banana-pro-watermark-remover` dùng MCP với `remove_watermark_complete` hoặc workflow từng bước gồm upload, detect, auto-brush, remove, polling và QA. Backend chạy LaMa ONNX trên VPS, hỗ trợ PNG/JPEG/WebP. Trang [Watermark Remover](https://bb.1nutnhan.com/watermark-remover/) là fallback cho mask thủ công; output luôn được lưu như bản mới, không ghi đè ảnh gốc.
