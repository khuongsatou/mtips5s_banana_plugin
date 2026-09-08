# Watermark MCP contract

Backend hiện dùng model LaMa ONNX trên VPS, chạy bằng ONNX Runtime CPU. Định dạng được hỗ trợ: PNG, JPEG và WebP. MCP public yêu cầu xác thực.

## Tool map

| Mục đích | Tool |
|---|---|
| Upload input | `upload_watermark_image` |
| Phát hiện vùng watermark | `detect_watermark_regions` |
| Tạo mask từ vùng phát hiện | `auto_brush_watermark` |
| Xóa tự động | `remove_watermark_auto` |
| Workflow hoàn chỉnh | `remove_watermark_complete` |
| Theo dõi job | `get_watermark_job` |
| Lấy output | `get_watermark_result` |
| Kiểm tra output | `qa_watermark_result` |

Không hard-code tham số khi chưa có schema runtime. Khi gọi MCP, đọc schema tool được expose ở phiên hiện tại và truyền đúng tên field do server yêu cầu.

## Acceptance

- Có input id/asset id từ bước upload.
- Job hoàn tất ở trạng thái terminal thành công.
- Có result từ `get_watermark_result`.
- `qa_watermark_result` xác nhận output đọc được và có thể bàn giao.
- Output được lưu thành bản mới; không xóa hoặc ghi đè input.
