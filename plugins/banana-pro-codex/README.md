# Banana Pro Codex

Plugin local cho Codex, kết nối Banana Pro qua BB API và MCP, kèm workflow xóa watermark bằng model LaMa ONNX.

Tác giả / developer: **Sếp Khương**.

## Cấu hình

- API base mặc định: `https://bb.1nutnhan.com`
- Health: `/api/health`
- MCP: `/mcp` khi gateway được bật
- Xác thực MCP: OAuth + PKCE trong Codex; key `bbmcp_` được cấp tự động sau khi người dùng đăng nhập và chấp thuận
- Đổi API base bằng `BANANA_PRO_BASE_URL`

### Dev và production

Production là mặc định khi plugin được cài/release vào Codex Desktop:
`https://bb.1nutnhan.com` và `https://bb.1nutnhan.com/mcp`.

Dev chỉ chạy trên loopback:

```bash
BANANA_PRO_ENV=dev BANANA_PRO_DEV_PORT=9123 \
  plugins/banana-pro-codex/scripts/connect.sh
python3 plugins/banana-pro-codex/scripts/build_plugin.py \
  --environment dev --port 9123 --output dist/dev
```

Release production:

```bash
python3 plugins/banana-pro-codex/scripts/build_plugin.py \
  --environment production --output dist/production
```

Không đưa token vào package; `BANANA_PRO_MCP_API_KEY` vẫn được Codex/OAuth quản lý bên ngoài plugin.

Khi cài plugin, Codex tự khám phá OAuth từ MCP server và mở trang đăng nhập Banana Pro. Mỗi lần kết nối tạo một key riêng cho Codex; người dùng có thể thu hồi key đó trong trang **MCP API Keys**.

Không đặt token trực tiếp trong plugin, manifest, prompt hoặc log. Trước generation phải health check; text-to-image tự chạy khi prompt đã đủ và không hỏi confirmation, còn các capability khác theo gate trong skill tương ứng. Sau generation phải QA output.

## Workflow Anime → Xóa watermark → Upscale

Skill `banana-pro-anime-watermark-upscale` lưu workflow đã kiểm chứng thành pipeline tái sử dụng: tạo ảnh anime, xóa watermark, sau đó upscale 2X bằng Upscayl Standard tại [Upscayl](https://bb.1nutnhan.com/upscale). Pipeline giữ bản gốc, ghi manifest cho từng stage và dùng polling file thay vì phải canh giao diện thủ công.

Ví dụ:

```bash
python3 plugins/banana-pro-codex/skills/anime-watermark-upscale/scripts/pipeline_manifest.py \
  init work/anime-pipeline.json input/source.jpg
python3 plugins/banana-pro-codex/skills/anime-watermark-upscale/scripts/poll_outputs.py \
  ~/Downloads output_upscaled.png --report work/upscale-poll.json
python3 plugins/banana-pro-codex/skills/anime-watermark-upscale/scripts/pipeline_manifest.py \
  qa work/anime-pipeline.json --stage upscale --report work/qa-report.json
```

Các script chỉ quản lý file/manifest và QA local; MCP client hoặc browser UI vẫn là nơi thực hiện generation, watermark removal và upscale, nên không có API key hay endpoint private trong plugin.

## Xóa watermark

Skill `banana-pro-watermark-remover` dùng MCP với `remove_watermark_complete` hoặc workflow từng bước gồm upload, detect, auto-brush, remove, polling và QA. Backend chạy LaMa ONNX trên VPS, hỗ trợ PNG/JPEG/WebP. Trang [Watermark Remover](https://bb.1nutnhan.com/watermark-remover/) là fallback cho mask thủ công; output luôn được lưu như bản mới, không ghi đè ảnh gốc.

## Xóa logo bằng Gemini

Skill `banana-pro-gemini-logo-remover` dùng workflow chỉnh sửa ảnh Gemini qua capability đã được expose của MCP/BB API. Nếu Gemini chưa khả dụng, dùng trang [Watermark Remover](https://bb.1nutnhan.com/watermark-remover/) làm fallback; luôn báo engine thực tế và QA output.

## Upscale độc lập

Skill `banana-pro-upscale` xử lý upscale riêng lẻ qua MCP/BB API hoặc trang [Upscale](https://bb.1nutnhan.com/upscale) khi MCP chưa khả dụng. File nguồn luôn được giữ nguyên.
