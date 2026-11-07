# Trả lời câu hỏi thảo luận Lab 04

- Họ và tên: Nguyễn Thanh Kiên
- MSSV: 202416540
- Bài thực hành: Release flow và quản lý phiên bản phát hành.

## 1. Vì sao chuẩn bị phát hành trên master trước, không sửa trực tiếp trên nhánh release?

Version, CHANGELOG và mã nguồn cần được chuẩn bị cùng nhau trên một nhánh
chủ đề, kiểm tra và review qua PR vào master. Sau khi hoàn tất, tạo nhánh
release từ commit đã duyệt để chốt một baseline nhất quán, có thể tái tạo.

Nếu chỉ sửa version hoặc tài liệu trên release, master có thể thiếu những
thay đổi này. Việc phát triển tiếp sẽ khó đối chiếu với bản đã phát hành.
Trong bài, topic/prepare-release-1.0.0 đưa version, dòng giới thiệu và
CHANGELOG vào master qua PR #16 trước khi tạo release/lab04 và tag v1.0.0.

Nhánh release vẫn có thể nhận bản sửa bảo trì qua PR theo quy trình; nó
không phải nơi tiếp tục phát triển các tính năng mới của master.

## 2. Vì sao release/* không merge ngược vào master? So sánh với GitFlow

Theo Release Flow của bài thực hành, master là dòng phát triển chính, còn
release/* là dòng giữ và bảo trì một bản đã chốt. Tính năng mới tiếp tục đi
vào master. Không merge toàn bộ release ngược lại master vì thay đổi riêng
của bản cũ, như số phiên bản và changelog bảo trì, có thể không phù hợp với
phiên bản đang phát triển.

Khi cần đưa một bản sửa từ release về master, quy trình Lab 05 sẽ tách commit
sửa lỗi và cherry-pick có truy vết qua nhánh, PR. Trong các tình huống khác,
việc chọn lọc bản sửa phải tuân theo chính sách dự án.

| Nội dung | Release Flow trong học phần | GitFlow thông thường |
| --- | --- | --- |
| Dòng phát triển chính | master | develop |
| Nhánh tính năng | Tạo từ master và PR vào master | Thường tạo từ develop và gộp vào develop |
| Nhánh release | Tạo từ master, giữ bản nộp/phát hành, không merge toàn bộ ngược về master | Tạo từ develop để ổn định bản phát hành, sau đó gộp vào main/master và develop |
| Hotfix | Trong bài, tạo từ release bị ảnh hưởng rồi lan truyền commit sửa cần thiết | Thường tạo từ main/master và tích hợp lại vào các dòng liên quan |

Đây là hai quy trình khác nhau; không áp dụng máy móc quy tắc gộp nhánh
release của GitFlow vào mô hình mà bài đang sử dụng.

## 3. Vì sao phát hành 1.0.0 thay vì 0.4.0?

Semantic Versioning có dạng MAJOR.MINOR.PATCH. Giai đoạn 0.y.z biểu thị phát
triển ban đầu, khi giao diện công khai có thể chưa ổn định. Phiên bản 1.0.0
đánh dấu mốc xác định giao diện công khai và bắt đầu cam kết ổn định theo
quy tắc quản lý phiên bản của dự án.

Trong học phần, các tag v0.1.0, v0.2.0 và v0.3.0 ghi nhận các mốc thực hành
ban đầu. Lab 04 chọn 1.0.0 làm bản phát hành chính thức đầu tiên, có version,
CHANGELOG, tag, GitHub Release và kiểm toán baseline. Không phải cứ hoàn
thành bài thứ tư thì phải dùng 0.4.0; số phiên bản thể hiện quyết định phát
hành và mức ổn định, không phải số thứ tự bài lab.

Sau 1.0.0, thêm tính năng tương thích có thể tăng MINOR thành 1.1.0; chỉ sửa
lỗi tương thích tăng PATCH thành 1.0.1; thay đổi không tương thích tăng MAJOR.

## 4. Tag khác nhánh release như thế nào?

Tag v1.0.0 đánh dấu chính xác một phiên bản đã phát hành và không được di
chuyển hoặc tạo đè sau khi chia sẻ theo quy trình bài. Annotated tag còn có
thông tin người tạo, thời điểm và thông điệp; có thể ký nếu cần.

Nhánh release/lab04 là tham chiếu có thể dịch chuyển khi nhận các commit
bảo trì đã được review. Tag v1.0.0 vẫn giữ bản gốc ngay cả khi nhánh release
nhận hotfix sau này. Git không tự đảm bảo tag bất biến nếu không có quy tắc
bảo vệ tương ứng; việc không sửa tag đã phát hành là yêu cầu quy trình.

Tag không tự được push chỉ vì push nhánh, nên phải push rõ tên tag. Trong
bài, cả v1.0.0 và origin/release/lab04 lúc phát hành cùng trỏ tới:

```text
b7d23fa79e3536b16ace33510f56835ec5365b57
```

Các tag v0.1.0, v0.2.0 và v0.3.0 được gắn vào đúng nhánh nộp Lab 01–03.

## 5. Ghi nhận trạng thái phát triển sau phát hành

Sau PR #17 thêm sắp xếp, master ở commit 92a53f1 và có tám test thành công.
Release v1.0.0 vẫn có bốn test, chưa có sort_by_title và sort_by_cost.

```powershell
git log --oneline release/lab04..master
git log --oneline master..release/lab04
git describe --tags
```

Tại thời điểm kiểm tra, lệnh đầu hiện commit tính năng 0eb003b và merge
commit 92a53f1; lệnh thứ hai không có kết quả. `git describe --tags` trả về
`v1.0.0-2-g92a53f1`: HEAD ở sau tag v1.0.0 hai commit theo cách đếm của Git,
với mã rút gọn 92a53f1. Sau khi thêm tài liệu, kết quả describe có thể đổi.

So sánh v0.3.0 với v1.0.0 cho thấy ba file thay đổi: CHANGELOG.md,
aims/__init__.py và main.py. So sánh v1.0.0 với master sau PR #17 cho thấy
thay đổi về sắp xếp, các test tương ứng và mục Unreleased trong CHANGELOG.

## 6. Kết quả tái tạo và kiểm toán cấu hình

- Detached HEAD tại v0.2.0: chương trình chạy đúng tổng tiền 63.89 $, sau đó
  quay lại master mà không tạo commit trên detached HEAD.
- Worktree tại v1.0.0: dòng đầu là AIMS-mini v1.0.0, tổng tiền 63.89 $ và
  bốn test OK.
- `git show v1.0.0:aims/__init__.py` hiển thị `__version__ = "1.0.0"`.
- `git ls-tree -r --name-only v1.0.0` không có __pycache__ hoặc file nháp.
- Đã dọn worktree thử và xuất aims-1.0.0.zip từ tag bằng git archive.
- GitHub Release AIMS-mini v1.0.0 đã xuất bản, dùng tag có sẵn v1.0.0.
- Rule release/* yêu cầu PR và approval, không cho bypass, force push hoặc
  xóa nhánh theo cấu hình đã thiết lập.
- Push commit rỗng trực tiếp vào release/lab04 bị từ chối với GH006 và
  thông báo Changes must be made through a pull request. Commit thử cục bộ
  được bỏ sau khi push bị từ chối; tag và nhánh phát hành vẫn cùng baseline.

## 7. Nơi lưu câu trả lời và bản phát hành

Câu trả lời này được bổ sung sau khi v1.0.0 đã phát hành, nên được đưa vào
master qua PR tài liệu. Không cập nhật release/lab04 từ master để tránh kéo
tính năng sắp xếp vào bản phát hành. Không di chuyển tag v1.0.0.

Khi nộp, dùng release/lab04 hoặc tag v1.0.0 để xác định mã nguồn phát hành,
kèm đường dẫn file trả lời trên master hoặc PR tài liệu tương ứng.
