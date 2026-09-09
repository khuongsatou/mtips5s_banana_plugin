# Banana Pro Dev/Production Environments Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Tách Banana Pro thành profile `dev` chạy trên `127.0.0.1:<port>` và profile `production` trỏ tới `https://bb.1nutnhan.com`, với production là mặc định và là cấu hình duy nhất của package release cho Codex Desktop.

**Architecture:** Một resolver Python dùng chung trả về environment đã chuẩn hóa, base URL, MCP URL và port. Các script health hiện có dùng resolver này; build script tạo package dev/production riêng trong `dist/` và luôn giữ `.mcp.json` trong source plugin là production. Test contract xác minh default, validation, propagation và release guard.

**Tech Stack:** Python 3 standard library, Bash, PowerShell, JSON, `unittest`, Codex plugin manifest/MCP config.

**Spec:** `docs/superpowers/specs/2026-09-09-dev-production-environments-design.md`

## Global Constraints

- Production base URL là `https://bb.1nutnhan.com`.
- Production MCP URL là `https://bb.1nutnhan.com/mcp`.
- Dev chỉ dùng `http://127.0.0.1:<port>`.
- Không có environment selector thì dùng production.
- Dev port hợp lệ trong khoảng `1..65535`, mặc định `8000`.
- Không commit secret, API key, token hoặc dữ liệu runtime.
- Package production không được chứa localhost trong `.mcp.json`.
- Không thay đổi skill workflow hoặc public backend metadata ngoài phần environment documentation cần thiết.

---

### Task 1: Add the environment resolver

**Files:**
- Create: `plugins/banana-pro-codex/scripts/env_config.py`
- Test: `tests/test_env_config.py`

**Interfaces:**
- Produces `EnvironmentConfig` with fields `environment`, `base_url`, `mcp_url`, `dev_port`.
- Produces `resolve_config(env: Mapping[str, str] | None = None, cli_environment: str | None = None, cli_port: int | None = None) -> EnvironmentConfig`.
- Produces `validate_base_url(value: str, environment: str) -> str`.

- [ ] **Step 1: Write failing resolver tests**

```python
class EnvironmentConfigTest(unittest.TestCase):
    def test_defaults_to_production(self):
        config = resolve_config({})
        self.assertEqual(config.environment, "production")
        self.assertEqual(config.base_url, "https://bb.1nutnhan.com")
        self.assertEqual(config.mcp_url, "https://bb.1nutnhan.com/mcp")

    def test_dev_uses_loopback_and_default_port(self):
        config = resolve_config({"BANANA_PRO_ENV": "dev"})
        self.assertEqual(config.base_url, "http://127.0.0.1:8000")
        self.assertEqual(config.mcp_url, "http://127.0.0.1:8000/mcp")

    def test_dev_accepts_custom_port(self):
        config = resolve_config({"BANANA_PRO_ENV": "dev", "BANANA_PRO_DEV_PORT": "9123"})
        self.assertEqual(config.base_url, "http://127.0.0.1:9123")

    def test_rejects_invalid_dev_port_and_non_loopback_dev_url(self):
        with self.assertRaises(ValueError):
            resolve_config({"BANANA_PRO_ENV": "dev", "BANANA_PRO_DEV_PORT": "0"})
        with self.assertRaises(ValueError):
            resolve_config({"BANANA_PRO_ENV": "dev", "BANANA_PRO_BASE_URL": "https://dev.example.com"})
```

- [ ] **Step 2: Run the focused test and verify it fails**

Run: `python3 -m unittest tests/test_env_config.py -v`

Expected: FAIL because `env_config.py` and `resolve_config` do not exist.

- [ ] **Step 3: Implement the resolver**

Implement a frozen dataclass. Read `BANANA_PRO_ENV`, `BANANA_PRO_BASE_URL`, and `BANANA_PRO_DEV_PORT`; use production when the selector is absent or empty; construct dev URLs only from `127.0.0.1` plus the validated port; normalize trailing slashes; reject unknown environments and invalid URL components.

- [ ] **Step 4: Run the focused test and verify it passes**

Run: `python3 -m unittest tests/test_env_config.py -v`

Expected: PASS for default production, custom dev port, and safety validation.

- [ ] **Step 5: Commit the resolver and tests**

```bash
git add plugins/banana-pro-codex/scripts/env_config.py tests/test_env_config.py
git commit -m "feat: add banana environment resolver"
```

### Task 2: Migrate health and profile scripts to the resolver

**Files:**
- Modify: `plugins/banana-pro-codex/scripts/connect.sh`
- Modify: `plugins/banana-pro-codex/scripts/connect.ps1`
- Modify: `plugins/banana-pro-codex/scripts/host_profile.py`
- Test: `tests/test_env_scripts.py`

**Interfaces:**
- All three scripts resolve the same `base_url` for the same environment variables.
- Shell and PowerShell scripts preserve GET request behavior against `<base_url>/api/health`.
- `host_profile.py` preserves its safe JSON shape and adds the resolved `environment` field.

- [ ] **Step 1: Add script contract tests**

Test the Python profile with a local HTTP server and assert that `BANANA_PRO_ENV=dev` plus `BANANA_PRO_DEV_PORT=<server port>` requests `/api/health`; inspect shell/PowerShell source to assert they invoke the resolver and no longer contain an independent production fallback.

- [ ] **Step 2: Run tests to verify the migration contract fails**

Run: `python3 -m unittest tests/test_env_scripts.py -v`

Expected: FAIL because the existing scripts do not use the shared resolver.

- [ ] **Step 3: Update the scripts**

Use `python3 plugins/banana-pro-codex/scripts/env_config.py --print base_url` from Bash, invoke the same resolver through Python from PowerShell, and import it directly from `host_profile.py`. Preserve timeout/error behavior and never print environment variables containing secrets.

- [ ] **Step 4: Run script tests and a live health probe**

Run: `python3 -m unittest tests/test_env_scripts.py -v` and `BANANA_PRO_ENV=production bash plugins/banana-pro-codex/scripts/connect.sh`.

Expected: focused tests pass; production probe reaches `https://bb.1nutnhan.com/api/health` and reports the existing health JSON.

- [ ] **Step 5: Commit script migration**

```bash
git add plugins/banana-pro-codex/scripts tests/test_env_scripts.py
git commit -m "refactor: use shared environment config for health checks"
```

### Task 3: Add environment-specific MCP package generation

**Files:**
- Create: `plugins/banana-pro-codex/scripts/build_plugin.py`
- Create: `plugins/banana-pro-codex/config/README.md`
- Test: `tests/test_build_plugin.py`
- Modify: `.gitignore`

**Interfaces:**
- CLI: `python3 plugins/banana-pro-codex/scripts/build_plugin.py --environment production --output dist/production`.
- CLI: `python3 plugins/banana-pro-codex/scripts/build_plugin.py --environment dev --port 9123 --output dist/dev`.
- Produces a copied plugin tree with generated `.mcp.json` and unchanged plugin manifest/assets/skills.
- Production build fails if its generated MCP URL is not `https://bb.1nutnhan.com/mcp`.

- [ ] **Step 1: Write failing build tests**

```python
def test_production_build_writes_production_mcp(self):
    run_build("production", self.output)
    mcp = json.loads((self.output / ".mcp.json").read_text())
    self.assertEqual(mcp["mcpServers"]["banana-pro"]["url"], "https://bb.1nutnhan.com/mcp")

def test_dev_build_writes_custom_local_mcp(self):
    run_build("dev", self.output, port=9123)
    mcp = json.loads((self.output / ".mcp.json").read_text())
    self.assertEqual(mcp["mcpServers"]["banana-pro"]["url"], "http://127.0.0.1:9123/mcp")

def test_production_build_rejects_localhost_output(self):
    with self.assertRaises(SystemExit):
        run_build("production", self.output, base_url="http://127.0.0.1:9123")
```

- [ ] **Step 2: Run the build tests and verify failure**

Run: `python3 -m unittest tests/test_build_plugin.py -v`

Expected: FAIL because the build script does not exist.

- [ ] **Step 3: Implement the build script**

Copy the plugin directory with `shutil.copytree`, exclude generated/cache files, write only the target `.mcp.json`, validate the copied manifest exists, and refuse an output path inside the source plugin. Do not delete existing directories automatically; require an empty/nonexistent output directory.

- [ ] **Step 4: Add generated-output ignore rules and usage documentation**

Keep `dist/` ignored. Document that source `.mcp.json` remains production and that dev packages are disposable local artifacts; include exact commands for ports `8000` and custom ports.

- [ ] **Step 5: Run focused build tests and dry-run both profiles**

Run: `python3 -m unittest tests/test_build_plugin.py -v`; then run both build commands into temporary directories and inspect each `.mcp.json`.

Expected: production points to `https://bb.1nutnhan.com/mcp`; dev points to the requested loopback port.

- [ ] **Step 6: Commit packaging support**

```bash
git add plugins/banana-pro-codex/scripts/build_plugin.py plugins/banana-pro-codex/config/README.md tests/test_build_plugin.py .gitignore
git commit -m "feat: add dev and production plugin packaging"
```

### Task 4: Document default behavior and release procedure

**Files:**
- Modify: `README.md`
- Modify: `CONNECT.md`
- Modify: `plugins/banana-pro-codex/README.md`
- Modify: `refer/architecture.md`
- Test: `tests/test_plugin.py`

**Interfaces:**
- Documentation exposes `BANANA_PRO_ENV`, `BANANA_PRO_DEV_PORT`, and the two build commands.
- Documentation states that Codex Desktop release uses production by default.
- Existing health readiness contract remains unchanged.

- [ ] **Step 1: Add documentation assertions**

Extend `tests/test_plugin.py` to assert the production URL, `BANANA_PRO_ENV=dev`, `BANANA_PRO_DEV_PORT`, and the production release command appear in the relevant docs.

- [ ] **Step 2: Run documentation tests and verify any missing assertions**

Run: `python3 -m unittest tests/test_plugin.py -v`

Expected: FAIL until all docs describe the new environment workflow.

- [ ] **Step 3: Update the documentation**

Document three explicit modes: default/release production, local dev with default port 8000, and local dev with a custom port. Explain that MCP URL and health URL change together, and that tokens remain external to the package.

- [ ] **Step 4: Run documentation tests**

Run: `python3 -m unittest tests/test_plugin.py -v`

Expected: PASS without weakening existing manifest/skill assertions.

- [ ] **Step 5: Commit documentation**

```bash
git add README.md CONNECT.md plugins/banana-pro-codex/README.md refer/architecture.md tests/test_plugin.py
git commit -m "docs: document banana dev and production environments"
```

### Task 5: Full verification and release gate

**Files:**
- Modify: `tests/test_plugin.py` only if an integration assertion is missing.
- Verify: all files from Tasks 1-4.

**Interfaces:**
- Full test suite remains runnable with the existing command.
- Release dry-run proves production is safe by default.

- [ ] **Step 1: Run the complete test suite**

Run: `python3 -m unittest discover -s tests -v`

Expected: all tests pass.

- [ ] **Step 2: Run production package verification**

Run: `python3 plugins/banana-pro-codex/scripts/build_plugin.py --environment production --output /tmp/banana-pro-release-check`.

Inspect `/tmp/banana-pro-release-check/.mcp.json` and verify it contains exactly `https://bb.1nutnhan.com/mcp`; verify no token-like environment value or secret file was copied.

- [ ] **Step 3: Run dev package verification**

Run: `python3 plugins/banana-pro-codex/scripts/build_plugin.py --environment dev --port 9123 --output /tmp/banana-pro-dev-check`.

Verify the generated MCP URL is `http://127.0.0.1:9123/mcp` and the source plugin `.mcp.json` is still production.

- [ ] **Step 4: Run the real production health check**

Run: `BANANA_PRO_ENV=production bash plugins/banana-pro-codex/scripts/connect.sh`.

Expected: the response has `ok`, `extension_ready`, and `flow_key_present` as true, subject to current backend availability.

- [ ] **Step 5: Review the final diff and repository status**

Run: `git diff --check` and `git status --short`.

Expected: no whitespace errors, no generated `dist/` files tracked, and no secrets/model weights/customer data added.

- [ ] **Step 6: Commit the final verification adjustments, if any**

```bash
git add tests README.md CONNECT.md refer plugins/banana-pro-codex
git commit -m "test: verify environment-aware plugin release"
```
