# Connect Banana Pro với Codex

## MCP

Plugin đăng ký streamable HTTP tại `https://bb.1nutnhan.com/mcp`. Đặt secret vào `BANANA_PRO_MCP_API_KEY`; không ghi key vào file hoặc prompt.

## API read-only health

```bash
plugins/banana-pro-codex/scripts/connect.sh
```

Health chỉ được xem là Ready khi `ok`, `extension_ready` và `flow_key_present` đều là `true`.

## API capabilities

- `POST /api/images/generate`: text-to-image và image-to-image.
- `POST /api/images/upload-bytes`: upload bytes từ máy local.
- MCP `/mcp`: tool gateway nếu backend public đã bật.

Trước compute phải health check, resolve configuration và xin confirmation. Sau compute phải kiểm tra output thật và metadata.

