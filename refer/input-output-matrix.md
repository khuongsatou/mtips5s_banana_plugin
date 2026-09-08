# Input / Output Matrix

| Capability | Input | Endpoint | Output |
|---|---|---|---|
| Health | Không | GET /api/health | Trạng thái an toàn |
| Text-to-image | Prompt, aspect | POST /api/images/generate | Task/output image |
| Image-to-image | Local image bytes, prompt | upload-bytes + generate | Task/output image |
| Media workflow | Manifest, assets, job IDs | API/MCP tools | Artifact + report |
| QA handoff | Output artifact | Local probe/review | Pass/Fail + path |

