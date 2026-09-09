# Connect Banana Pro với Codex

## MCP

Plugin đăng ký streamable HTTP tại `https://bb.1nutnhan.com/mcp`. Đặt secret vào `BANANA_PRO_MCP_API_KEY`; không ghi key vào file hoặc prompt.

## API read-only health

```bash
plugins/banana-pro-codex/scripts/connect.sh
```

Health chỉ được xem là Ready khi `ok`, `extension_ready` và `flow_key_present` đều là `true`.

## Chọn môi trường

Mặc định là production (`https://bb.1nutnhan.com`). Với backend local, đặt `BANANA_PRO_ENV=dev`; resolver sẽ dùng `http://127.0.0.1:8000` hoặc port trong `BANANA_PRO_DEV_PORT`.

Package release cho Codex Desktop phải được tạo bằng:

```bash
python3 plugins/banana-pro-codex/scripts/build_plugin.py \
  --environment production --output dist/production
```

Dev package có thể tạo bằng `--environment dev --port 9123`; MCP và health sẽ cùng dùng port đó.

## API capabilities

- `POST /api/images/generate`: text-to-image và image-to-image.
- `POST /api/images/upload-bytes`: upload bytes từ máy local.
- MCP `/mcp`: tool gateway nếu backend public đã bật.

Trước compute phải health check và resolve configuration. Text-to-image tự submit khi prompt đã đủ, không xin confirmation; các capability còn lại giữ confirmation gate theo skill tương ứng. Sau compute phải kiểm tra output thật và metadata.
