import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "plugins" / "banana-pro-codex" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from build_plugin import build_plugin


class BuildPluginTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.output = self.temp_dir / "package"

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def read_mcp(self):
        return json.loads((self.output / ".mcp.json").read_text())

    def test_production_build_writes_production_mcp(self):
        build_plugin("production", self.output)
        self.assertEqual(
            self.read_mcp()["mcpServers"]["banana-pro"]["url"],
            "https://bb.1nutnhan.com/mcp",
        )
        self.assertTrue((self.output / ".codex-plugin/plugin.json").is_file())

    def test_dev_build_writes_custom_local_mcp(self):
        build_plugin("dev", self.output, port=9123)
        self.assertEqual(
            self.read_mcp()["mcpServers"]["banana-pro"]["url"],
            "http://127.0.0.1:9123/mcp",
        )

    def test_production_build_rejects_localhost_output(self):
        with self.assertRaises(ValueError):
            build_plugin("production", self.output, base_url="http://127.0.0.1:9123")

    def test_build_refuses_existing_output(self):
        self.output.mkdir()
        with self.assertRaises(FileExistsError):
            build_plugin("production", self.output)


if __name__ == "__main__":
    unittest.main()
