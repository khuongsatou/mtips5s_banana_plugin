---
name: banana-pro-anime-watermark-upscale
description: Workflow ảnh anime → xóa watermark → upscale 2X, có manifest, polling file và QA.
---
# Anime → Watermark → Upscale

Dùng cho workflow nhiều bước đã kiểm chứng trên Banana Pro:

1. Tạo/chuyển ảnh sang style anime bằng Banana Pro.
2. Xóa logo hoặc watermark bằng MCP Watermark Remover (LaMa ONNX); dùng browser fallback khi cần brush trực tiếp.
3. Upscale bản đã xóa watermark bằng Upscayl tại `https://bb.1nutnhan.com/upscale`, mặc định model `Upscayl Standard`, scale `2X`.
4. Tải output về thư mục riêng, không ghi đè input.
5. QA kích thước, định dạng, dung lượng và hash; ghi kết quả vào manifest.

## Handoff và polling

Tạo workspace workflow bằng `scripts/pipeline_manifest.py init`. Sau mỗi bước cập nhật manifest bằng `set-stage`. Với job MCP, dùng poller MCP hiện có trong skill watermark-remover. Với browser fallback hoặc Upscayl, dùng `scripts/poll_outputs.py` để chờ file được tải xuống; không restart job chỉ vì một lần polling timeout.

Manifest phải lưu input/output, stage, config, job ID nếu có, thời điểm, trạng thái và lỗi. Không lưu API key, cookie hoặc payload nhạy cảm.

## Quy tắc an toàn

- Chỉ xử lý ảnh người dùng có quyền sử dụng/chỉnh sửa.
- Giữ bản gốc và các intermediate quan trọng.
- Không gọi endpoint private hoặc tự suy đoán API của Upscayl.
- Chỉ báo hoàn tất sau khi file tồn tại, mở được và QA đạt.
