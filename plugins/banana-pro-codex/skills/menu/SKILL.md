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
6. QA handoff — kiểm tra file, metadata, lỗi và bàn giao.

Nếu yêu cầu chưa rõ, hỏi người dùng chọn capability. Với tạo/chỉnh sửa, luôn staging input, hiển thị configuration card và xin xác nhận trước khi chạy.

Với yêu cầu xóa watermark, chuyển sang `banana-pro-watermark-remover`. Ưu tiên MCP trực tiếp, giữ file gốc và chỉ dùng browser UI làm fallback cho mask thủ công.
