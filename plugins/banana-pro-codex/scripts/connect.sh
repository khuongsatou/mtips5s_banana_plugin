#!/usr/bin/env bash
set -euo pipefail
script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
base_url="$(python3 "$script_dir/env_config.py" --print base_url)"
curl --fail-with-body --silent --show-error --connect-timeout 10 "${base_url%/}/api/health"
