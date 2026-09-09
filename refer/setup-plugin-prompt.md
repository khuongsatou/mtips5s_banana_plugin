# Prompt tạo plugin Codex tương tự Motion Studio

Bạn là kiến trúc sư plugin Codex và kỹ sư hệ thống production. Hãy xây dựng một plugin Codex hoàn chỉnh có kiến trúc tương tự dự án tham chiếu hiện tại trong workspace, nhưng dành cho sản phẩm:

- Tên sản phẩm: `<TÊN SẢN PHẨM>`
- Tên plugin dạng hyphen-case: `<plugin-name>`
- Chức năng chính: `<MÔ TẢ CHỨC NĂNG>`
- Người dùng mục tiêu: `<ĐỐI TƯỢNG NGƯỜI DÙNG>`
- Ngôn ngữ giao tiếp với người dùng: tiếng Việt
- Hệ điều hành cần hỗ trợ: macOS cho Codex client, Linux/Windows cho runtime nếu phù hợp
- Có thể chạy runtime trên máy local hoặc máy GPU/CPU thuê từ xa qua SSH
- Backend/model cụ thể phải được ẩn khỏi metadata và giao diện công khai, chỉ xuất hiện trong diagnostics nội bộ khi cần

## 1. Đọc và phân tích dự án tham chiếu

Trước khi viết code:

1. Đọc toàn bộ `README.md`.
2. Đọc `plugins/motion-studio/.codex-plugin/plugin.json`.
3. Đọc tất cả `SKILL.md`, `agents/openai.yaml`, `CONNECT.md`.
4. Đọc các tài liệu trong `refer/`, đặc biệt kiến trúc tổng thể, flow end-to-end, setup host/MCP, interaction contract và input/output matrix.
5. Đọc toàn bộ test hiện có.
6. Kiểm tra các script setup, runtime server, health endpoint, model audit, job state và cách đăng ký MCP.
7. Lập bảng mapping giữa kiến trúc tham chiếu và plugin mới trước khi triển khai.

Không sao chép mù quáng tên model, URL riêng, token, model weights, voice sample, tên thương hiệu backend hoặc giới hạn không phù hợp với sản phẩm mới.

## 2. Cấu trúc thư mục bắt buộc

Tạo cấu trúc tối thiểu:

```text
<repository-root>/
├── README.md
├── CONNECT.md
├── .agents/plugins/marketplace.json
├── plugins/<plugin-name>/
│   ├── .codex-plugin/plugin.json
│   ├── assets/icon.png
│   ├── assets/logo.png
│   ├── skills/
│   │   ├── menu/SKILL.md
│   │   ├── menu/agents/openai.yaml
│   │   ├── <skill-1>/
│   │   ├── <skill-2>/
│   │   └── <skill-n>/
│   ├── scripts/
│   │   ├── connect.sh
│   │   ├── connect.ps1
│   │   └── host_profile.py
│   └── cloud/
│       ├── bootstrap.sh
│       ├── boot.py
│       ├── preflight.py
│       ├── worker.py
│       ├── progress.py
│       └── tests/
├── prompts/menu.md
├── refer/
└── tests/
```

Chỉ tạo `cloud/` nếu plugin thực sự cần máy thuê hoặc worker từ xa. Không tạo `.mcp.json` hoặc `.app.json` nếu MCP được đăng ký bằng script riêng như dự án tham chiếu.

## 3. Manifest plugin

Tạo `.codex-plugin/plugin.json` hợp lệ, không để placeholder `[TODO]`. Manifest phải có `name`, `version`, `description`, `author`, `homepage`, `repository`, `keywords`, `skills`, và các trường `interface` gồm `displayName`, `shortDescription`, `longDescription`, `developerName`, `category`, `websiteURL`, `brandColor`, `composerIcon`, `logo`, `logoDark`, `capabilities`, `defaultPrompt`.

Metadata công khai chỉ mô tả capability và lợi ích người dùng. Không đưa vào đó tên model backend, repository backend, số VRAM, tên GPU, token, URL nội bộ, đường dẫn máy cá nhân, model weights hoặc dữ liệu khách hàng.

## 4. Thiết kế skill

Tạo một skill `menu` làm bộ định tuyến chính. Menu phải kiểm tra nhẹ runtime hiện có, hiển thị toàn bộ capability, không tự setup/render/thay đổi máy, chờ người dùng chọn rồi chuyển sang skill tương ứng.

Mỗi skill chức năng cần có `SKILL.md`, `agents/openai.yaml`, `assets/runtime/`, `references/` và `scripts/`. `SKILL.md` phải mô tả trigger, setup hiện có, chọn host, các lệnh `use`, `host`, `check`, `models`, `setup`, `status`, `logs`, `down`, `connect`, hardware gate, model audit, giới hạn, staging input, configuration, confirmation khi capability yêu cầu, execute, wait, QC, lỗi và bàn giao output. Text-to-image phải tự submit khi prompt đã đủ, không thêm confirmation gate.

Mỗi `agents/openai.yaml` có dạng:

```yaml
interface:
  display_name: "<Tên hiển thị>"
  short_description: "<Mô tả ngắn>"
  default_prompt: "<Prompt tiếng Việt>"
```

## 5. Lifecycle chuẩn

Áp dụng state machine:

```text
unconfigured → checked → models_audited → setup → healthy → connected
→ input_staged → configured → confirmed → running → completed
→ qc_passed/qc_failed → delivered
```

Các trạng thái lỗi gồm `failed`, `cancelled`, `offline`, `insufficient_hardware`, `missing_models`, `invalid_input`, `confirmation_required`.

Chỉ giao thành công khi job đạt terminal state, file output tồn tại, file đọc được, metadata/duration được đo lại, QC cần thiết hoàn tất và trả về đường dẫn tuyệt đối.

## 6. MCP gateway

Mỗi runtime có thể có MCP gateway riêng. Gateway phải bind vào `127.0.0.1`, có `/healthz`, `runtime_status`, staging input, interactive configuration, interactive confirmation, submit job, wait job, list/get job và trả JSON ổn định.

Mẫu API logic:

```text
runtime_status()
stage_input(source_path | source_url)
configure_<capability>_interactive(...)
confirm_<capability>_interactive(config_token)
render_<capability>(config_token, config_confirmed)
wait_for_<capability>(job_id)
render_<capability>_and_wait(config_token)
get_job(job_id)
list_jobs()
```

Nếu capability có confirmation gate và Codex không hỗ trợ elicitation, dùng một câu hỏi numbered list, hiển thị cấu hình đã resolve, yêu cầu xác nhận rõ ràng rồi mới truyền `config_confirmed=true`. Riêng text-to-image coi request tạo ảnh ban đầu là quyền submit và không hỏi xác nhận khi prompt đã đủ.

## 7. Host cache

Dùng `~/.<plugin-name>/hosts.json`, hoặc `%USERPROFILE%/<plugin-name>/hosts.json` trên Windows. Cache chỉ lưu host, local/remote, URL, OS, tài nguyên, capability/tier, runtime root, PM2 app names và tên biến môi trường chứa token.

Tuyệt đối không lưu bearer token, SSH password, private key, voice sample, model weights hoặc dữ liệu riêng. Đặt quyền file chỉ owner đọc/ghi.

## 8. Setup an toàn

1. `use` chỉ tái sử dụng runtime, không cài/download.
2. `host` chỉ đọc cache và health probe.
3. `check` chỉ đo phần cứng, RAM, disk, driver và runtime.
4. `models` chỉ audit file, không download.
5. `setup` là lệnh duy nhất được cài/download.
6. Chạy `check` trước mọi download.
7. Hiển thị checklist `READY`, `MISSING`, `INVALID`.
8. Chỉ tải file thiếu/hỏng.
9. Download vào `.part`, kiểm tra kích thước/hash/header rồi mới rename.
10. Không ghi đè âm thầm model hợp lệ.
11. Không khởi động runtime trùng port.
12. Chờ health check thành công trước `connect`.

Remote host phải thử SSH key/agent trước, dùng `BatchMode=yes`, không đặt password vào command/environment/PM2/log, phát hiện OS/shell trước khi chọn Bash hoặc PowerShell, và chạy hardware check từ xa trước khi copy/cài đặt.

## 9. Configuration card và confirmation

Trước compute/render của capability có confirmation gate, hiển thị:

```text
Cấu hình đề xuất

- Chức năng:
- Input:
- Output:
- Thời lượng:
- FPS:
- Độ phân giải:
- Chế độ xử lý:
- Prompt:
- Asset mapping:
- Audio/voice:
- Giới hạn đã áp dụng:
- Engine/fallback:
- QC sau khi hoàn tất:
- Thời gian ước tính:
- Cảnh báo:

1. Xác nhận cấu hình và bắt đầu.
2. Sửa cấu hình.
3. Hủy.
```

Nếu người dùng sửa bất kỳ trường nào của capability có confirmation gate, hiển thị lại card và yêu cầu xác nhận lại. Mục này không áp dụng cho text-to-image có prompt đầy đủ.

## 10. Bảo mật và trung thực

Không commit secret, model weights lớn, dữ liệu khách hàng hoặc voice sample. Không public hóa runtime nội bộ. Remote MCP phải dùng HTTPS + Bearer token. Nội dung voice/identity phải có consent. Không quảng cáo backend/model. Luôn báo engine thực tế, phân biệt AI result với fallback, không tự retry, không tự hạ chất lượng/tier và không báo hoàn tất khi chưa có file thật.

## 11. Tài liệu

Viết `README.md`, `CONNECT.md` và các tài liệu trong `refer/` về kiến trúc, flow end-to-end, host/MCP, interaction contract và input/output matrix. Mỗi skill có reference riêng cho workflow và giới hạn.

## 12. Kiểm thử

Tạo test cho manifest, danh sách skill, capability metadata, không lộ hardware/backend, tier ladder, model audit, atomic download, input validation, config token, confirmation gate của các capability cần gate, text-to-image tự submit không confirmation, job state, output existence, metadata probe, health endpoint, secret logging, port conflict, cleanup khi fail/cancel và retry không đổi cấu hình.

Chạy:

```bash
python3 -m unittest discover -s tests -v
```

Chạy thêm toàn bộ runtime tests nếu có.

## 13. Marketplace

Tạo `.agents/plugins/marketplace.json` với plugin local:

```json
{
  "name": "<plugin-name>-marketplace",
  "interface": { "displayName": "<Tên sản phẩm>" },
  "plugins": [
    {
      "name": "<plugin-name>",
      "source": { "source": "local", "path": "./plugins/<plugin-name>" },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "<Creativity hoặc nhóm phù hợp>"
    }
  ]
}
```

## 14. Tiêu chí nghiệm thu

Chỉ bàn giao khi Codex nhận diện plugin, menu và skill hoạt động, manifest validate, MCP health check hoạt động, local/remote setup an toàn, setup idempotent, model audit hoạt động, confirmation gate không thể bypass ở capability yêu cầu gate, text-to-image không hỏi xác nhận khi prompt đã đủ, monitor hoạt động, output được probe/QC, tài liệu khớp code, tất cả test pass và Git không chứa secret/model weights/dữ liệu khách hàng.

Cuối cùng báo cáo cấu trúc file, skill đã triển khai, MCP endpoint, lệnh setup/connect, test đã chạy, giới hạn còn lại và thông tin cần người dùng cung cấp.
