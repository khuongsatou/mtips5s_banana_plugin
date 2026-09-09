#!/usr/bin/env python3
"""Resolve Banana Pro environment URLs without exposing secrets."""

from __future__ import annotations

import argparse
import os
from dataclasses import dataclass
from typing import Mapping
from urllib.parse import urlsplit, urlunsplit

PRODUCTION_BASE_URL = "https://bb.1nutnhan.com"
DEV_HOST = "127.0.0.1"
DEFAULT_DEV_PORT = 8000


@dataclass(frozen=True)
class EnvironmentConfig:
    environment: str
    base_url: str
    mcp_url: str
    dev_port: int | None


def _validate_port(value: str | int | None) -> int:
    if value is None or value == "":
        return DEFAULT_DEV_PORT
    try:
        port = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("BANANA_PRO_DEV_PORT must be an integer") from exc
    if not 1 <= port <= 65535:
        raise ValueError("BANANA_PRO_DEV_PORT must be between 1 and 65535")
    return port


def validate_base_url(value: str, environment: str) -> str:
    """Validate and normalize an environment base URL."""
    candidate = value.rstrip("/")
    parsed = urlsplit(candidate)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("base URL must use http/https and include a hostname")
    if parsed.username or parsed.password or parsed.query or parsed.fragment:
        raise ValueError("base URL must not contain credentials, query, or fragment")
    if environment == "dev":
        if parsed.scheme != "http" or parsed.hostname != DEV_HOST:
            raise ValueError("dev base URL must use http://127.0.0.1")
    return urlunsplit((parsed.scheme, parsed.netloc, parsed.path.rstrip("/"), "", ""))


def resolve_config(
    env: Mapping[str, str] | None = None,
    cli_environment: str | None = None,
    cli_port: int | None = None,
) -> EnvironmentConfig:
    values = os.environ if env is None else env
    environment = (cli_environment or values.get("BANANA_PRO_ENV") or "production").strip().lower()
    if environment not in {"production", "dev"}:
        raise ValueError("BANANA_PRO_ENV must be production or dev")

    if environment == "production":
        base_url = validate_base_url(
            values.get("BANANA_PRO_BASE_URL") or PRODUCTION_BASE_URL,
            environment,
        )
        if base_url != PRODUCTION_BASE_URL:
            raise ValueError("production base URL must be https://bb.1nutnhan.com")
        return EnvironmentConfig(environment, base_url, base_url + "/mcp", None)

    port = _validate_port(cli_port if cli_port is not None else values.get("BANANA_PRO_DEV_PORT"))
    requested = values.get("BANANA_PRO_BASE_URL")
    base_url = validate_base_url(requested, environment) if requested else f"http://{DEV_HOST}:{port}"
    parsed = urlsplit(base_url)
    if parsed.port != port:
        raise ValueError("dev base URL port must match BANANA_PRO_DEV_PORT")
    return EnvironmentConfig(environment, base_url, base_url + "/mcp", port)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--print", dest="field", choices=("environment", "base_url", "mcp_url"), required=True)
    parser.add_argument("--environment", dest="cli_environment")
    parser.add_argument("--port", dest="cli_port", type=int)
    args = parser.parse_args()
    config = resolve_config(cli_environment=args.cli_environment, cli_port=args.cli_port)
    print(getattr(config, args.field))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
