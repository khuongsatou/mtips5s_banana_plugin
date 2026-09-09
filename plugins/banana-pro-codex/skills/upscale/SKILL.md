---
name: banana-pro-upscale
description: Upscale ảnh bằng workflow Banana Pro, ưu tiên MCP/BB API và dùng giao diện Upscale làm fallback, có QA và bảo toàn file gốc.
---
# Upscale

Dùng skill này khi người dùng muốn phóng to hoặc tăng độ chi tiết ảnh. Giữ file nguồn nguyên vẹn và lưu output thành file mới.

## Workflow

- Xác nhận ảnh đầu vào, scale/độ phân giải mong muốn và định dạng output trước khi chạy.
- Ưu tiên capability upscale qua MCP hoặc BB API khi đã được expose trong phiên.
- Nếu MCP chưa khả dụng, dùng giao diện [Upscale](https://bb.1nutnhan.com/upscale) làm fallback. Không tự suy đoán payload hoặc endpoint private.
- Chọn model/scale được người dùng yêu cầu; nếu chưa nêu, dùng thiết lập mặc định của UI và báo lại trong kết quả.
- Chờ job hoàn tất nếu workflow bất đồng bộ; không khởi động lại chỉ vì một lần polling timeout.
- QA output: mở được, đúng kích thước kỳ vọng, không bị crop/đổi màu bất thường và file nguồn không bị ghi đè.
- Báo rõ engine thực tế và đường dẫn output trước khi bàn giao.
