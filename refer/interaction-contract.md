# Interaction Contract

Lifecycle mặc định: checked → connected → input_staged → configured → confirmed → running → completed → qc_passed → delivered.

Text-to-image với prompt đã đủ dùng lifecycle rút gọn: checked → connected → configured → running → completed → qc_passed → delivered.

Lỗi: offline, missing extension, missing flow key, invalid input, confirmation required, failed, cancelled.

Với text-to-image, yêu cầu tạo ảnh ban đầu là quyền submit và các trường không nêu dùng mặc định; không hiển thị confirmation card. Các capability khác không coi yêu cầu ban đầu là confirmation cuối và vẫn xin xác nhận theo skill tương ứng.
