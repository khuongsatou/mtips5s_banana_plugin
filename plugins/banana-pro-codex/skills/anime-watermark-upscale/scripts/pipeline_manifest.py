#!/usr/bin/env python3
"""Create and update manifests for the anime/watermark/upscale workflow."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import time
from pathlib import Path

SUPPORTED = {".png", ".jpg", ".jpeg", ".webp"}
TERMINAL = {"succeeded", "failed", "canceled", "skipped"}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def describe(path: Path) -> dict:
    item = {"path": str(path.resolve()), "name": path.name, "bytes": path.stat().st_size,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
    try:
        item["file_type"] = subprocess.run(["file", "-b", str(path)], capture_output=True,
                                            text=True, check=False).stdout.strip()
    except OSError:
        item["file_type"] = "unknown"
    return item


def init(args: argparse.Namespace) -> int:
    path = Path(args.manifest).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {"workflow": "anime-style-transfer -> watermark-removal -> upscale",
            "created_at": int(time.time()),
            "config": {"upscale_model": args.model, "scale": args.scale},
            "items": []}
    for raw in args.inputs:
        source = Path(raw).expanduser().resolve()
        data["items"].append({"input": describe(source) if source.is_file() else {"path": str(source)},
                              "stages": {"anime": {"status": "pending"},
                                         "watermark": {"status": "pending"},
                                         "upscale": {"status": "pending"}},
                              "status": "pending"})
    save(path, data)
    print(path)
    return 0


def set_stage(args: argparse.Namespace) -> int:
    path = Path(args.manifest).expanduser().resolve()
    data = load(path)
    if not 0 <= args.item < len(data["items"]):
        raise SystemExit(f"item index out of range: {args.item}")
    item = data["items"][args.item]
    stage = item["stages"].setdefault(args.stage, {})
    stage["status"] = args.status
    stage["updated_at"] = int(time.time())
    if args.job_id:
        stage["job_id"] = args.job_id
    if args.output:
        output = Path(args.output).expanduser().resolve()
        stage["output"] = describe(output) if output.is_file() else {"path": str(output)}
    if args.error:
        stage["error"] = args.error
    item["status"] = "failed" if args.status == "failed" else ("succeeded" if all(
        s.get("status") == "succeeded" for s in item["stages"].values()) else "running")
    save(path, data)
    print(json.dumps(stage, ensure_ascii=False, indent=2))
    return 0


def qa(args: argparse.Namespace) -> int:
    path = Path(args.manifest).expanduser().resolve()
    data = load(path)
    report = {"manifest": str(path), "ok": True, "checked": []}
    for item in data["items"]:
        stage = item["stages"].get(args.stage, {})
        raw = stage.get("output", {}).get("path")
        output = Path(raw) if raw else None
        valid = bool(output and output.is_file() and output.stat().st_size > 0 and
                     output.suffix.lower() in SUPPORTED)
        checked = {"input": item["input"].get("name"), "output": str(output) if output else None,
                   "ok": valid}
        if valid:
            checked.update(describe(output))
        report["checked"].append(checked)
        report["ok"] = report["ok"] and valid
    output = Path(args.report).expanduser().resolve() if args.report else path.with_name("qa-report.json")
    save(output, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["ok"] else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("init"); p.add_argument("manifest"); p.add_argument("inputs", nargs="+")
    p.add_argument("--model", default="Upscayl Standard"); p.add_argument("--scale", default="2X"); p.set_defaults(func=init)
    p = sub.add_parser("set-stage"); p.add_argument("manifest"); p.add_argument("item", type=int)
    p.add_argument("stage", choices=["anime", "watermark", "upscale"]); p.add_argument("status", choices=sorted(TERMINAL | {"pending", "running"}))
    p.add_argument("--job-id"); p.add_argument("--output"); p.add_argument("--error"); p.set_defaults(func=set_stage)
    p = sub.add_parser("qa"); p.add_argument("manifest"); p.add_argument("--stage", default="upscale", choices=["anime", "watermark", "upscale"]); p.add_argument("--report"); p.set_defaults(func=qa)
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
