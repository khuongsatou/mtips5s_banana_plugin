import unittest

from pathlib import Path
import sys

SCRIPTS = Path(__file__).resolve().parents[1] / "plugins" / "banana-pro-codex" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from env_config import resolve_config


class EnvironmentConfigTest(unittest.TestCase):
    def test_defaults_to_production(self):
        config = resolve_config({})
        self.assertEqual(config.environment, "production")
        self.assertEqual(config.base_url, "https://bb.1nutnhan.com")
        self.assertEqual(config.mcp_url, "https://bb.1nutnhan.com/mcp")

    def test_dev_uses_loopback_and_default_port(self):
        config = resolve_config({"BANANA_PRO_ENV": "dev"})
        self.assertEqual(config.environment, "dev")
        self.assertEqual(config.base_url, "http://127.0.0.1:8000")
        self.assertEqual(config.mcp_url, "http://127.0.0.1:8000/mcp")

    def test_dev_accepts_custom_port(self):
        config = resolve_config(
            {"BANANA_PRO_ENV": "dev", "BANANA_PRO_DEV_PORT": "9123"}
        )
        self.assertEqual(config.base_url, "http://127.0.0.1:9123")
        self.assertEqual(config.mcp_url, "http://127.0.0.1:9123/mcp")

    def test_rejects_invalid_dev_port_and_non_loopback_dev_url(self):
        with self.assertRaises(ValueError):
            resolve_config({"BANANA_PRO_ENV": "dev", "BANANA_PRO_DEV_PORT": "0"})
        with self.assertRaises(ValueError):
            resolve_config(
                {
                    "BANANA_PRO_ENV": "dev",
                    "BANANA_PRO_BASE_URL": "https://dev.example.com",
                }
            )

    def test_rejects_unknown_environment(self):
        with self.assertRaises(ValueError):
            resolve_config({"BANANA_PRO_ENV": "staging"})


if __name__ == "__main__":
    unittest.main()
