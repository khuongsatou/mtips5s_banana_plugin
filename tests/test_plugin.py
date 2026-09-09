from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "banana-pro-codex"

class PluginContractTest(unittest.TestCase):
    def test_manifest_and_mcp_are_valid(self):
        manifest = json.loads((PLUGIN / ".codex-plugin/plugin.json").read_text())
        mcp = json.loads((PLUGIN / ".mcp.json").read_text())
        self.assertEqual(manifest["name"], "banana-pro-codex")
        self.assertEqual(manifest["mcpServers"], "./.mcp.json")
        self.assertEqual(mcp["mcpServers"]["banana-pro"]["url"], "https://bb.1nutnhan.com/mcp")

    def test_refresh_scripts_are_packaged(self):
        scripts = PLUGIN / "scripts"
        self.assertTrue((scripts / "refresh-youtube-workflow-preview.cjs").is_file())
        self.assertTrue((scripts / "auto-refresh-youtube-workflows.cjs").is_file())

    def test_skill_contracts_exist(self):
        skills = [p for p in (PLUGIN / "skills").iterdir() if p.is_dir()]
        self.assertGreaterEqual(len(skills), 5)
        for skill in skills:
            self.assertTrue((skill / "SKILL.md").is_file())
            self.assertTrue((skill / "agents/openai.yaml").is_file())
            self.assertTrue((skill / "assets/runtime").is_dir())
            self.assertTrue((skill / "references").is_dir())
            self.assertTrue((skill / "scripts").is_dir())

if __name__ == "__main__":
    unittest.main()
