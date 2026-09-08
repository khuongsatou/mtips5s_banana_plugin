$ErrorActionPreference = "Stop"
$baseUrl = if ($env:BANANA_PRO_BASE_URL) { $env:BANANA_PRO_BASE_URL } else { "https://bb.1nutnhan.com" }
Invoke-RestMethod -Method Get -Uri ($baseUrl.TrimEnd("/") + "/api/health")

