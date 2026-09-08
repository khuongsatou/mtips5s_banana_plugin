---
name: banana-pro-image-editing
description: Upload ảnh local và thực hiện image-to-image bằng Banana Pro.
---
# Image Editing

Trigger khi người dùng muốn giữ chủ thể/phong cách từ ảnh tham chiếu và chỉnh sửa.

Ảnh local không thể được BB đọc trực tiếp bằng path `/Users/...`. Dùng `POST /api/images/upload-bytes` với base64 và mime type; lấy `name` hoặc `mediaGenerationId`, rồi truyền vào `imageInputs` của `POST /api/images/generate`.

Luôn xác nhận quyền sử dụng asset, validate loại/kích thước file, giữ bản gốc, hiển thị configuration card và xin confirm trước generation. Báo rõ nếu upload hoặc output thất bại.

