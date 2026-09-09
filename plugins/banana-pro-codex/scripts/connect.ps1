$ErrorActionPreference = "Stop"
$baseUrl = & python (Join-Path $PSScriptRoot "env_config.py") --print base_url
Invoke-RestMethod -Method Get -Uri ($baseUrl.TrimEnd("/") + "/api/health")
