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

    def test_watermark_remover_skill_is_registered(self):
        skill = PLUGIN / "skills/watermark-remover"
        text = (skill / "SKILL.md").read_text()
        self.assertIn("banana-pro-watermark-remover", text)
        self.assertIn("remove_watermark_complete", text)
        self.assertIn("Image Library", text)
        self.assertIn("không gọi endpoint private", text)

    def test_menu_routes_watermark_requests(self):
        text = (PLUGIN / "skills/menu/SKILL.md").read_text()
        self.assertIn("banana-pro-watermark-remover", text)

    def test_watermark_support_script_is_executable_and_documented(self):
        script = PLUGIN / "skills/watermark-remover/scripts/watermark_batch.py"
        self.assertTrue(script.is_file())
        self.assertTrue(script.stat().st_mode & 0o111)
        self.assertIn("watermark_batch.py", (script.parent / "README.md").read_text())

    def test_polling_script_is_executable_and_documented(self):
        script = PLUGIN / "skills/watermark-remover/scripts/poll_jobs.py"
        self.assertTrue(script.is_file())
        self.assertTrue(script.stat().st_mode & 0o111)
        self.assertIn("poll_jobs.py", (script.parent / "README.md").read_text())

if __name__ == "__main__":
    unittest.main()
