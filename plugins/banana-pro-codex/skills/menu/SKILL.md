---
name: banana-pro-menu
description: Bộ định tuyến tiếng Việt cho các capability Banana Pro của Codex.
---
# Banana Pro — Menu

Dùng khi người dùng muốn làm việc với Banana Pro. Kiểm tra nhẹ trạng thái bằng `scripts/connect.sh`, không tự setup, render hoặc thay đổi máy.

## Capability
1. Health/connect — kiểm tra BB API và FlowKit.
2. Image generation — tạo ảnh từ prompt.
3. Image editing — upload ảnh local rồi chỉnh sửa theo prompt.
4. Media workflows — chuẩn bị workflow, asset mapping và theo dõi output.
5. Watermark remover — xóa logo/watermark qua MCP LaMa ONNX, gồm detect, auto remove, job polling và QA.
6. Gemini logo remover — xóa logo bằng workflow chỉnh sửa ảnh Gemini, có Watermark Remover fallback và QA.
7. Upscale — phóng to/tăng chi tiết ảnh qua MCP/BB API hoặc giao diện Upscale fallback.
8. QA handoff — kiểm tra file, metadata, lỗi và bàn giao.

Nếu yêu cầu chưa rõ capability, hỏi người dùng chọn capability. Với tạo ảnh từ text, chuyển sang `banana-pro-image-generation`; khi prompt đã đủ thì tự chạy bằng cấu hình mặc định, không xin xác nhận. Với chỉnh sửa ảnh, vẫn staging input, hiển thị configuration card và xin xác nhận trước khi chạy.

Với yêu cầu xóa watermark, chuyển sang `banana-pro-watermark-remover`. Ưu tiên MCP trực tiếp, giữ file gốc và chỉ dùng browser UI làm fallback cho mask thủ công.

Với yêu cầu xóa logo bằng Gemini, chuyển sang `banana-pro-gemini-logo-remover`. Với yêu cầu upscale, chuyển sang `banana-pro-upscale`.
