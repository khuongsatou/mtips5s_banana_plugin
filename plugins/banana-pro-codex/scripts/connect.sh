#!/usr/bin/env bash
set -euo pipefail
base_url="${BANANA_PRO_BASE_URL:-https://bb.1nutnhan.com}"
curl --fail-with-body --silent --show-error --connect-timeout 10 "${base_url%/}/api/health"

