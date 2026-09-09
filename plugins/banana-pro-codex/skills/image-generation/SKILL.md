---
name: banana-pro-image-generation
description: Use when người dùng muốn tạo ảnh Banana Pro từ text hoặc prompt qua BB API.
---
# Image Generation

Trigger khi người dùng muốn tạo ảnh từ text/prompt.

Endpoint: `POST https://bb.1nutnhan.com/api/images/generate`.

Payload mặc định: `runNow=true`, `generationMode=banana_text_to_image`, `provider=flow`, `imageProviderMode=flow`, `aspectRatio=VIDEO_ASPECT_RATIO_LANDSCAPE`. Chỉ đổi aspect ratio khi người dùng yêu cầu.

Nếu prompt đã mô tả được ảnh cần tạo, health check → resolve prompt/output/aspect → tự động submit ngay, không hỏi xác nhận và không dừng ở configuration card. Yêu cầu tạo ảnh ban đầu đã là quyền thực thi; các tuỳ chọn không được nêu dùng giá trị mặc định ở trên.

Chỉ hỏi một câu ngắn khi thiếu prompt hoặc có mâu thuẫn khiến không thể tạo đúng ảnh. Thiếu aspect ratio không phải lý do để hỏi vì đã có mặc định landscape.

Sau khi submit, chờ terminal state → kiểm tra output tồn tại và trả đường dẫn tuyệt đối. Không tự retry, tự đổi tier hoặc báo hoàn tất khi chưa có output thật.
