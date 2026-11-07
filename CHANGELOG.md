# Changelog

Những thay đổi đáng chú ý của AIMS-mini được ghi tại đây.
Tài liệu theo cấu trúc Keep a Changelog; phiên bản dùng Semantic Versioning.

## [Unreleased]

### Added

- `search_by_category(items, category)` tìm DVD theo tên thể loại khớp chính xác; thêm ba test cho danh sách kết quả, không khớp và đầu vào rỗng.
- `Cart.sort_by_title()` sắp xếp giỏ theo tên DVD tăng dần.
- `Cart.sort_by_cost()` sắp xếp giỏ theo giá tăng dần, giữ thứ tự tương đối khi giá bằng nhau.
- Bốn test cho sắp xếp theo tên, theo giá, giỏ trống và các DVD cùng giá.

## [1.0.0] - 2026-11-07

### Added

- `Cart.print_cart()` hiển thị danh sách DVD và tổng tiền; giỏ trống có thông báo riêng.
- `search_by_title(items, keyword)` tìm DVD theo từ khóa trong tên, hiện phân biệt hoa thường.
- `Cart.total_cost_with_discount(percent)` tính số tiền còn phải trả sau giảm giá.
- Thông báo tiếng Việt khi thêm DVD vào giỏ.
- Bốn unit test về giới hạn giỏ, công thức giảm giá, các giá trị biên và phần trăm không hợp lệ.
- Mẫu Pull Request, tài liệu use case và câu trả lời thảo luận Lab 02, Lab 03.
- Thông tin phiên bản `aims.__version__` và dòng giới thiệu phiên bản trong chương trình mẫu.

### Fixed

- Chặn DVD thứ 21 trong bài tập mô phỏng giới hạn giỏ; `add_dvd()` trả về `True` khi thêm thành công và `False` khi đầy (Issue #8, PR #9).
- Sửa công thức giảm giá để tổng 100 giảm 20% còn 80; từ chối phần trăm ngoài khoảng 0 đến 100 bằng `ValueError` (PR #10, #11).

### Changed

- Hoàn tác việc đưa tên DVD vào thông báo thêm đĩa bằng PR #14; giữ thông báo tiếng Việt không kèm tên DVD.
