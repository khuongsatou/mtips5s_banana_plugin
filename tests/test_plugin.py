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
        self.assertIn("gemini-logo-removal", manifest["keywords"])
        self.assertIn("Gemini logo removal", manifest["interface"]["capabilities"])
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

    def test_root_readme_documents_watermark_remover_url(self):
        text = (ROOT / "README.md").read_text()
        self.assertIn("https://bb.1nutnhan.com/watermark-remover/", text)

    def test_root_readme_documents_upscale_url(self):
        text = (ROOT / "README.md").read_text()
        self.assertIn("https://bb.1nutnhan.com/upscale", text)

    def test_environment_workflow_is_documented(self):
        docs = "\n".join(
            (ROOT / path).read_text()
            for path in (
                "README.md",
                "CONNECT.md",
                "plugins/banana-pro-codex/README.md",
                "refer/architecture.md",
            )
        )
        self.assertIn("BANANA_PRO_ENV=dev", docs)
        self.assertIn("BANANA_PRO_DEV_PORT", docs)
        self.assertIn("--environment production", docs)
        self.assertIn("Codex Desktop", docs)

    def test_menu_routes_watermark_requests(self):
        text = (PLUGIN / "skills/menu/SKILL.md").read_text()
        self.assertIn("banana-pro-watermark-remover", text)

    def test_gemini_logo_and_upscale_skills_are_registered(self):
        gemini = PLUGIN / "skills/gemini-logo-remover/SKILL.md"
        upscale = PLUGIN / "skills/upscale/SKILL.md"
        self.assertIn("banana-pro-gemini-logo-remover", gemini.read_text())
        self.assertIn("https://bb.1nutnhan.com/watermark-remover/", gemini.read_text())
        self.assertIn("banana-pro-upscale", upscale.read_text())
        self.assertIn("https://bb.1nutnhan.com/upscale", upscale.read_text())

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
