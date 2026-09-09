"""Read-only Banana Pro host profile; never prints tokens or secret values."""
from __future__ import annotations
import json, urllib.request
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from env_config import resolve_config

CONFIG = resolve_config()
BASE_URL = CONFIG.base_url
with urllib.request.urlopen(BASE_URL + "/api/health", timeout=15) as response:
    payload = json.load(response)
safe = {key: payload.get(key) for key in ("ok", "extension_ready", "flow_key_present")}
print(json.dumps({"environment": CONFIG.environment, "base_url": BASE_URL, "health": safe}, ensure_ascii=False))
