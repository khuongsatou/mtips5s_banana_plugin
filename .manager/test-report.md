# Test Report

- **Status:** Passed with runtime gate
- **Scope:** Kiểm tra số lượng file, JSON hợp lệ, header/template bắt buộc và liên kết state.
- **Result:** 6 skills, 8 rules, 6 workflows; đủ 7 file state trong `.manager`; đủ 5 file `.feedback`; `qa_coverage.json` parse hợp lệ và có giá trị `{}`; đủ 3 header bắt buộc.
- **Note:** Kiểm tra nội dung và cấu trúc đã đạt. Lệnh `find -printf` không tương thích macOS nhưng không ảnh hưởng kết quả; file tồn tại đã được xác nhận bằng `find`/`rg` tương thích.
- **Plugin tests:** 2/2 passed; JSON manifests valid; plugin validator passed.
- **Health probe:** BB reachable, MCP enabled; runtime not ready because extension clients require version `0.2.6`.
