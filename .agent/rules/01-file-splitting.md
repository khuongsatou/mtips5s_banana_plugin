# Rule: Splitting File & Context

Khi file vượt khoảng 300 dòng, có từ 3 trách nhiệm khác nhau, hoặc task chạm nhiều domain, phải tách thành file/module nhỏ theo trách nhiệm. Mỗi file có mục đích rõ, interface ổn định và người sở hữu. Với task lớn, tách theo requirement → implementation → test → feedback → release; không dồn toàn bộ nội dung vào một file hoặc một prompt gây tràn context. Cập nhật index/README nếu việc tách làm thay đổi điểm vào.

