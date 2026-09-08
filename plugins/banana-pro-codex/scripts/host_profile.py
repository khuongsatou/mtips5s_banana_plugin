"""Read-only Banana Pro host profile; never prints tokens or secret values."""
from __future__ import annotations
import json, os, urllib.request
BASE_URL = os.environ.get("BANANA_PRO_BASE_URL", "https://bb.1nutnhan.com").rstrip("/")
with urllib.request.urlopen(BASE_URL + "/api/health", timeout=15) as response:
    payload = json.load(response)
safe = {key: payload.get(key) for key in ("ok", "extension_ready", "flow_key_present")}
print(json.dumps({"base_url": BASE_URL, "health": safe}, ensure_ascii=False))

