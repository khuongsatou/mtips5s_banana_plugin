import json
import os
import subprocess
import sys
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "plugins" / "banana-pro-codex" / "scripts"


class HealthHandler(BaseHTTPRequestHandler):
    requests = []

    def do_GET(self):  # noqa: N802
        self.__class__.requests.append(self.path)
        payload = {"ok": True, "extension_ready": True, "flow_key_present": True}
        body = json.dumps(payload).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *_args):
        return


class EnvironmentScriptsTest(unittest.TestCase):
    def test_host_profile_uses_dev_port_and_reports_environment(self):
        HealthHandler.requests = []
        server = HTTPServer(("127.0.0.1", 0), HealthHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            env = os.environ.copy()
            env.update(
                {
                    "BANANA_PRO_ENV": "dev",
                    "BANANA_PRO_DEV_PORT": str(server.server_port),
                }
            )
            result = subprocess.run(
                [sys.executable, str(SCRIPTS / "host_profile.py")],
                env=env,
                capture_output=True,
                text=True,
                check=True,
            )
            profile = json.loads(result.stdout)
            self.assertEqual(profile["environment"], "dev")
            self.assertEqual(profile["base_url"], f"http://127.0.0.1:{server.server_port}")
            self.assertEqual(HealthHandler.requests, ["/api/health"])
        finally:
            server.shutdown()
            server.server_close()

    def test_shell_and_powershell_scripts_reference_shared_resolver(self):
        shell = (SCRIPTS / "connect.sh").read_text()
        powershell = (SCRIPTS / "connect.ps1").read_text()
        self.assertIn("env_config.py", shell)
        self.assertIn("env_config.py", powershell)
        self.assertNotIn('"https://bb.1nutnhan.com"', shell)
        self.assertNotIn('"https://bb.1nutnhan.com"', powershell)


if __name__ == "__main__":
    unittest.main()
