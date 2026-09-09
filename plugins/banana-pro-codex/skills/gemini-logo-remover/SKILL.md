---
name: banana-pro-gemini-logo-remover
description: Xóa logo hoặc vùng không mong muốn khỏi ảnh bằng workflow chỉnh sửa ảnh Gemini của Banana Pro, kèm fallback Watermark Remover và QA output.
---
# Gemini Logo Remover

Dùng skill này khi người dùng muốn xóa logo khỏi ảnh bằng khả năng chỉnh sửa ảnh Gemini trong Banana Pro. Chỉ xử lý ảnh người dùng có quyền sử dụng và chỉnh sửa.

## Workflow

- Giữ file gốc và tạo output mới; không ghi đè ảnh nguồn.
- Ưu tiên Gemini image editing qua MCP hoặc BB API khi capability đã được expose trong phiên.
- Gửi prompt chỉnh sửa tập trung vào việc xóa logo, bảo toàn bố cục, chủ thể, ánh sáng và texture xung quanh; không tự suy đoán payload hoặc tên tool chưa được công bố.
- Nếu Gemini/MCP chưa khả dụng, mở [Watermark Remover](https://bb.1nutnhan.com/watermark-remover/) làm fallback tương tác.
- Preview và QA output: file mở được, đúng định dạng/kích thước, logo đã được xử lý, không tạo artifact lớn và file gốc còn nguyên.
- Báo rõ engine thực tế (`Gemini`, BB API hoặc browser fallback) và không báo hoàn tất nếu chưa có file output thật.

Với logo nằm trên vùng chi tiết, ưu tiên mask/brush có kiểm soát thay vì prompt quá rộng. Nếu kết quả không đạt, dừng sau một lần điều chỉnh có chủ đích và báo người dùng.
