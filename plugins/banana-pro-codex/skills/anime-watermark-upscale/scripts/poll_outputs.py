#!/usr/bin/env python3
"""Poll a local download folder until expected image outputs exist."""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

SUPPORTED = {".png", ".jpg", ".jpeg", ".webp"}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("folder"); p.add_argument("names", nargs="+")
    p.add_argument("--timeout", type=float, default=900); p.add_argument("--interval", type=float, default=2)
    p.add_argument("--max-interval", type=float, default=20); p.add_argument("--report")
    args = p.parse_args()
    folder = Path(args.folder).expanduser().resolve()
    expected = set(args.names); deadline = time.monotonic() + args.timeout; delay = max(args.interval, 0.1)
    found = set()
    while True:
        current = {p.name for p in folder.iterdir() if p.is_file() and p.suffix.lower() in SUPPORTED} if folder.is_dir() else set()
        found = expected & current
        if found == expected:
            report = {"ok": True, "folder": str(folder), "found": sorted(found), "completed_at": int(time.time())}
            if args.report: Path(args.report).expanduser().resolve().write_text(json.dumps(report, indent=2) + "\n")
            print(json.dumps(report, ensure_ascii=False)); return 0
        if time.monotonic() >= deadline:
            report = {"ok": False, "folder": str(folder), "found": sorted(found), "missing": sorted(expected - found)}
            if args.report: Path(args.report).expanduser().resolve().write_text(json.dumps(report, indent=2) + "\n")
            print(json.dumps(report, ensure_ascii=False)); return 1
        time.sleep(delay); delay = min(delay * 1.5, args.max_interval)


if __name__ == "__main__":
    raise SystemExit(main())
