---
name: banana-pro-watermark-remover
description: Xóa watermark hoặc logo khỏi ảnh bằng MCP Banana Pro và model LaMa ONNX, gồm detect, auto-brush, xử lý tự động, job polling và QA.
---
# Watermark Remover

Dùng skill này khi người dùng muốn xóa logo, watermark hoặc một vùng không mong muốn khỏi ảnh bằng Banana Pro MCP. Backend chạy model LaMa ONNX trên VPS; trang `https://bb.1nutnhan.com/watermark-remover/` chỉ là UI bổ sung/fallback.

## Nguyên tắc workflow

- Chỉ xử lý ảnh mà người dùng có quyền sử dụng và chỉnh sửa.
- Giữ nguyên file gốc; tạo output mới với tên hoặc thư mục riêng.
- Ưu tiên MCP trực tiếp. Các tool chính và contract tham khảo nằm trong [references/mcp-contract.md](references/mcp-contract.md).
- MCP yêu cầu xác thực API key/OAuth theo cấu hình plugin. Không yêu cầu người dùng dán key vào prompt và không ghi key vào log.
- Trước khi xử lý, xác nhận input, số lượng ảnh và chế độ (`Auto Remove` hoặc mask thủ công). Với thao tác có thể tạo output, hiển thị cấu hình và xin người dùng xác nhận.
- Sau khi xử lý, preview kết quả, kiểm tra watermark đã được loại bỏ và hỏi người dùng lưu vào Image Library hay tải file xuống.
- Với batch hoặc workflow có thời gian chờ, dùng `scripts/watermark_batch.py` để prepare, watch và QA thay vì canh UI thủ công.
- Với job async từ MCP, dùng `scripts/poll_jobs.py` qua adapter status đã được xác định; dùng backoff/timeout và không restart job chỉ vì một lần polling lỗi.

## Chế độ xử lý

### Một ảnh — workflow tự động

1. Upload bằng `upload_watermark_image`.
2. Ưu tiên `remove_watermark_complete` khi người dùng muốn tự động hóa toàn bộ.
3. Nếu cần kiểm soát từng bước, dùng `detect_watermark_regions`, sau đó `auto_brush_watermark` hoặc `remove_watermark_auto`.
4. Nếu tool trả về job, dùng `get_watermark_job` đến trạng thái terminal; không tự khởi động lại job chỉ vì polling timeout.
5. Lấy file bằng `get_watermark_result`, rồi chạy `qa_watermark_result` trước khi bàn giao.

### Mask thủ công / browser fallback

Chỉ mở UI Watermark Remover khi người dùng yêu cầu vẽ mask trực tiếp, MCP không khả dụng, hoặc cần xử lý tương tác mà MCP contract chưa hỗ trợ. Sau fallback, vẫn QA output và giữ bản gốc.

### Nhiều ảnh

- Upload từng ảnh bằng `upload_watermark_image` hoặc dùng workflow batch nếu schema MCP cung cấp.
- Không tự động chạy toàn bộ queue nếu chưa có xác nhận của người dùng.
- Theo dõi từng job, thu thập từng result và báo rõ ảnh thành công/thất bại.

## Image Library

Khi ảnh đến từ Image Library, dùng luồng `Sync Library` nếu UI hỗ trợ. Lưu output như một item mới và giữ liên kết với ảnh nguồn; không xóa hoặc thay thế item gốc. Nếu đồng bộ không khả dụng, dùng download rồi báo đường dẫn output.

## Lỗi và QA

- Nếu MCP chưa xác thực, dừng trước bước upload và hướng dẫn kết nối MCP; không yêu cầu key trong chat.
- Nếu job lỗi, báo lỗi cụ thể và không coi ảnh là đã xử lý.
- Nếu auto removal cho kết quả kém, thử detect/brush có kiểm soát hoặc chuyển browser fallback; không lặp lại vô hạn.
- Chỉ dùng các tool MCP đã công bố; không gọi endpoint private hoặc tự suy đoán payload.
- Kiểm tra output mở được, đúng định dạng/kích thước, watermark đã được xử lý và không bị ghi đè lên file gốc.
