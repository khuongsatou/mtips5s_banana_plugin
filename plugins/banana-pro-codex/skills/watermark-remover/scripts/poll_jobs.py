#!/usr/bin/env python3
"""Poll async job status through an explicit local adapter command.

The adapter must print one JSON object per invocation. This keeps MCP
authentication and tool schemas outside the helper; no private endpoint is
guessed and no token is logged.
"""
from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
import time
from pathlib import Path

DEFAULT_TERMINAL = {"completed", "complete", "succeeded", "success", "failed", "error", "cancelled", "canceled"}


def value_at(payload: object, path: str) -> object:
    current = payload
    for part in path.split(".") if path else []:
        if isinstance(current, dict):
            current = current.get(part)
        else:
            return None
    return current


def fetch(command_template: str, job_id: str) -> dict:
    parts = [part.replace("{job_id}", job_id) for part in shlex.split(command_template)]
    if not parts or all("{job_id}" not in part for part in shlex.split(command_template)):
        raise ValueError("--status-command must contain the {job_id} placeholder")
    result = subprocess.run(parts, capture_output=True, text=True, check=False)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or f"adapter exited {result.returncode}")
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise ValueError(f"adapter did not print valid JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError("adapter JSON must be an object")
    return payload


def poll_one(job_id: str, args: argparse.Namespace) -> dict:
    started = time.time()
    delay = args.interval
    attempts = 0
    history: list[dict] = []
    terminal = {item.strip().lower() for item in args.terminal.split(",") if item.strip()} or DEFAULT_TERMINAL
    while True:
        attempts += 1
        try:
            payload = fetch(args.status_command, job_id)
            raw_status = value_at(payload, args.status_path)
            status = str(raw_status or "unknown").lower()
            event = {"attempt": attempts, "time": int(time.time()), "status": status}
            if args.include_payload:
                event["payload"] = payload
            history.append(event)
            print(f"{job_id}: {status} (attempt {attempts})", flush=True)
            if status in terminal:
                return {"job_id": job_id, "status": status, "ok": status in {"completed", "complete", "succeeded", "success"}, "attempts": attempts, "history": history}
        except (OSError, ValueError, RuntimeError) as exc:
            history.append({"attempt": attempts, "time": int(time.time()), "error": str(exc)})
            print(f"{job_id}: adapter error: {exc}", file=sys.stderr, flush=True)
        if time.time() - started >= args.timeout:
            return {"job_id": job_id, "status": "timeout", "ok": False, "attempts": attempts, "history": history}
        time.sleep(delay)
        delay = min(args.max_interval, delay * args.backoff)


def main() -> int:
    parser = argparse.ArgumentParser(description="Poll watermark/MCP jobs through a local JSON adapter")
    parser.add_argument("job_ids", nargs="+", help="job IDs returned by the MCP tool")
    parser.add_argument("--status-command", required=True, help="command printing JSON; include {job_id}")
    parser.add_argument("--status-path", default="status", help="dotted JSON path, e.g. data.status")
    parser.add_argument("--terminal", default=",".join(sorted(DEFAULT_TERMINAL)))
    parser.add_argument("--interval", type=float, default=2.0)
    parser.add_argument("--max-interval", type=float, default=20.0)
    parser.add_argument("--backoff", type=float, default=1.5)
    parser.add_argument("--timeout", type=float, default=900.0)
    parser.add_argument("--include-payload", action="store_true")
    parser.add_argument("--report", help="JSON report path")
    args = parser.parse_args()
    if args.interval <= 0 or args.max_interval <= 0 or args.backoff < 1 or args.timeout <= 0:
        parser.error("interval/max-interval/timeout must be > 0 and backoff must be >= 1")
    results = [poll_one(job_id, args) for job_id in args.job_ids]
    report = {"created_at": int(time.time()), "results": results, "ok": all(item["ok"] for item in results)}
    if args.report:
        path = Path(args.report).expanduser().resolve()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
        print(f"report: {path}")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
