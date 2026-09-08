#!/usr/bin/env python3
"""Prepare, monitor, and QA watermark-removal batches.

This helper does not call private APIs or expose credentials. It supports the
MCP workflow as well as the browser fallback by managing local files only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

SUPPORTED = {".png", ".jpg", ".jpeg", ".webp"}


def image_files(folder: Path) -> list[Path]:
    return sorted(p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in SUPPORTED)


def describe(path: Path) -> dict:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    info = {"name": path.name, "path": str(path.resolve()), "bytes": path.stat().st_size, "sha256": digest}
    try:
        result = subprocess.run(["file", "-b", str(path)], capture_output=True, text=True, check=False)
        info["file_type"] = result.stdout.strip()
    except OSError:
        info["file_type"] = "unknown"
    return info


def prepare(args: argparse.Namespace) -> int:
    source = Path(args.source).expanduser().resolve()
    destination = Path(args.destination).expanduser().resolve()
    destination.mkdir(parents=True, exist_ok=True)
    files = image_files(source)
    if not files:
        print(f"No supported images found in {source}", file=sys.stderr)
        return 2
    manifest = {
        "created_at": int(time.time()),
        "source": str(source),
        "destination": str(destination),
        "workflow": "anime-style-transfer -> watermark-removal -> qa",
        "items": [],
    }
    for index, path in enumerate(files, 1):
        target = destination / path.name
        if target.exists() and not args.overwrite:
            print(f"skip existing: {target}")
            continue
        shutil.copy2(path, target)
        manifest["items"].append({"index": index, "input": describe(target), "status": "ready"})
        print(f"prepared {index}/{len(files)}: {target.name}")
    manifest_path = destination / "watermark-batch.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(f"manifest: {manifest_path}")
    return 0


def watch(args: argparse.Namespace) -> int:
    folder = Path(args.folder).expanduser().resolve()
    expected = {name for name in args.names} if args.names else None
    deadline = time.monotonic() + args.timeout
    seen: set[str] = set()
    while True:
        current = {p.name for p in image_files(folder)}
        found = sorted((expected & current) if expected is not None else current)
        new = [name for name in found if name not in seen]
        for name in new:
            print(f"found: {folder / name}", flush=True)
        seen.update(found)
        if expected is not None and expected <= current:
            return 0
        if expected is None and found:
            return 0
        if time.monotonic() >= deadline:
            missing = sorted(expected - current) if expected is not None else []
            print("timeout" + (f"; missing: {', '.join(missing)}" if missing else ""), file=sys.stderr)
            return 1
        time.sleep(args.interval)


def qa(args: argparse.Namespace) -> int:
    folder = Path(args.folder).expanduser().resolve()
    files = image_files(folder)
    if args.names:
        wanted = set(args.names)
        files = [p for p in files if p.name in wanted]
    report = {"folder": str(folder), "checked": [], "ok": True}
    for path in files:
        item = describe(path)
        valid = path.stat().st_size > 0 and path.suffix.lower() in SUPPORTED
        item["ok"] = valid
        report["checked"].append(item)
        report["ok"] = report["ok"] and valid
    if not files:
        report["ok"] = False
        report["error"] = "no supported images found"
    output = Path(args.report).expanduser().resolve() if args.report else folder / "watermark-qa.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    print(f"report: {output}")
    return 0 if report["ok"] else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Support scripts for watermark-removal batches")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("prepare", help="copy source images and create a batch manifest")
    p.add_argument("source")
    p.add_argument("destination")
    p.add_argument("--overwrite", action="store_true")
    p.set_defaults(func=prepare)
    p = sub.add_parser("watch", help="wait for expected downloaded result files")
    p.add_argument("folder")
    p.add_argument("names", nargs="*")
    p.add_argument("--timeout", type=float, default=900)
    p.add_argument("--interval", type=float, default=2)
    p.set_defaults(func=watch)
    p = sub.add_parser("qa", help="validate local image outputs and write a JSON report")
    p.add_argument("folder")
    p.add_argument("names", nargs="*")
    p.add_argument("--report")
    p.set_defaults(func=qa)
    return parser


if __name__ == "__main__":
    parsed = build_parser().parse_args()
    raise SystemExit(parsed.func(parsed))
