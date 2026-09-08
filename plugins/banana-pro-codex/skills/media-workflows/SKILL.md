---
name: banana-pro-media-workflows
description: Điều phối workflow ảnh/video/media và mapping asset cho Banana Pro.
---
# Media Workflows

Dùng cho workflow nhiều bước: prompt → asset references → generation → extend/upscale/watermark → export.

Tách task theo từng bước và lưu manifest/report nhỏ; không gom toàn bộ context vào một file. Ghi input, output, config, job ID, trạng thái và lỗi. Giữ project ID local khác với workflow ID remote khi API yêu cầu. Với output async, poll job theo backoff có giới hạn và dừng khi completed/failed/cancelled.

