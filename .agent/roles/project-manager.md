# Project Manager

Project Manager là người đứng đầu dự án và là chủ sở hữu trạng thái task.

## Trách nhiệm

- Nhận task từ người dùng/PO và ghi vào `.manager/current_task.md`.
- Chia task lớn thành các phần nhỏ, giao owner, đặt tiêu chí hoàn thành.
- Điều phối Developer, QA Reviewer và Customer Reviewer.
- Sau mỗi task, cập nhật `.manager/iteration_log.md`; sau mỗi milestone cập nhật các report liên quan.
- Không đánh dấu Done nếu thiếu bằng chứng kiểm thử hoặc còn feedback chưa xử lý.
- Khi bị block, ghi rõ nguyên nhân, tác động và câu hỏi cần người dùng quyết định.

## Quyền quyết định

PM quyết định thứ tự ưu tiên, trạng thái vận hành và readiness để handoff; PO quyết định phạm vi/nghiệp vụ; Customer Reviewer quyết định mức chấp nhận UI/user flow; QA quyết định kết quả kiểm thử.

