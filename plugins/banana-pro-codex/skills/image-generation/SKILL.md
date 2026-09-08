---
name: banana-pro-image-generation
description: Tạo ảnh Banana Pro từ prompt qua BB API.
---
# Image Generation

Trigger khi người dùng muốn tạo ảnh từ text/prompt.

Endpoint: `POST https://bb.1nutnhan.com/api/images/generate`.

Payload mặc định: `runNow=true`, `generationMode=banana_text_to_image`, `provider=flow`, `imageProviderMode=flow`, `aspectRatio=VIDEO_ASPECT_RATIO_LANDSCAPE`. Chỉ đổi aspect ratio khi người dùng yêu cầu.

Health check → resolve prompt/output/aspect → configuration card → confirmation rõ ràng → submit → chờ terminal state → kiểm tra output tồn tại và trả đường dẫn tuyệt đối. Không tự retry, tự đổi tier hoặc báo hoàn tất khi chưa có output thật.

