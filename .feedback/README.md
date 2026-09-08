# `.feedback`

## Mục tiêu

Kênh trao đổi feedback giữa Codex, Antigravity, PM, QA và khách hàng; quản lý theo chuỗi inbox → response → action plan.

## Cấu trúc file

- `inbox.md`: feedback mới và context.
- `responses.md`: đánh giá và phản hồi gửi Antigravity.
- `action-plan.md`: việc cần làm, owner, priority, ETA, status.
- `qa_coverage.json`: coverage/traceability máy đọc được.

## Quy trình 4 bước

1. Ghi feedback mới vào Inbox với ID `FB-YYYYMMDD-AREA-001`.
2. PM/owner đánh giá và ghi response: Accept, Reject hoặc Need More Info.
3. Feedback được chấp nhận chuyển thành action plan có owner, priority, ETA.
4. Developer sửa, QA verify, cập nhật trạng thái và đóng log khi Done.

