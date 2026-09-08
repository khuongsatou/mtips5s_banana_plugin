# Scripts

`watermark_batch.py` hỗ trợ phần lặp lại quanh workflow MCP/browser mà không gọi API private:

```bash
python3 watermark_batch.py prepare ./inputs ./work
python3 watermark_batch.py watch ~/Downloads 798825860_anime-cleaned.png 793001888_anime-cleaned.png
python3 watermark_batch.py qa ./work --report ./work/qa.json
```

- `prepare`: copy ảnh vào workspace riêng và tạo `watermark-batch.json`.
- `watch`: chờ đủ file output được tải xuống, có timeout và exit code rõ ràng.
- `qa`: kiểm tra định dạng/kích thước file cơ bản, hash SHA-256 và tạo báo cáo JSON.

Script không chứa token, không upload file và không tự gọi endpoint nội bộ. Tool MCP vẫn thực hiện upload/process; script chỉ chuẩn bị, theo dõi và QA file local.

## Polling job MCP

`poll_jobs.py` theo dõi job async qua một adapter local đã biết schema. Adapter phải nhận job ID và in đúng một JSON object; script tự backoff, dừng ở trạng thái terminal, timeout và ghi report:

```bash
python3 poll_jobs.py JOB_ID \
  --status-command 'python3 ./mcp_status_adapter.py {job_id}' \
  --status-path status \
  --interval 2 --max-interval 20 --timeout 900 \
  --report ./work/poll-report.json
```

Nếu response nằm dưới `data.status`, dùng `--status-path data.status`. Adapter là nơi duy nhất gọi MCP client; không truyền API key qua command line và không ghi payload nhạy cảm vào report. `poll_jobs.py` không tự đoán URL hay endpoint private.
