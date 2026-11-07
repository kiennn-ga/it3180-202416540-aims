# Trả lời câu hỏi thảo luận Lab 05

- Họ và tên: Nguyễn Thanh Kiên
- MSSV: 202416540
- Bài thực hành: Hotfix flow và bảo trì nhiều phiên bản.

## 1. So sánh upstream-first và release-first

Upstream-first sửa lỗi trên dòng phát triển chính trước, sau đó đưa bản sửa
về các nhánh phát hành còn cần bảo trì. Cách này giúp dòng phát triển mới
nhất nhận sửa lỗi sớm, tránh lỗi tái xuất hiện trong các bản tương lai.
Tuy nhiên, mã trên master có thể đã thay đổi nhiều, nên backport về bản cũ
có thể phải điều chỉnh và kiểm tra lại.

Release-first bắt đầu từ nhánh phát hành đang bị ảnh hưởng. Bản sửa được
kiểm tra trong đúng bối cảnh bản cũ rồi lan truyền tới master và các nhánh
release liên quan. Cách này phù hợp khi cần khắc phục một bản đã giao hoặc
đã nộp, nhưng phải theo dõi đầy đủ các nơi cần nhận bản sửa để tránh bỏ sót.

Lab 05 dùng release-first: tái hiện lỗi trên v1.0.0, tạo hotfix từ
origin/release/lab04, phát hành v1.0.1, rồi cherry-pick bản sửa sang master
và release/lab05. Không có một thứ tự luôn đúng cho mọi dự án; cần theo
chính sách phát hành và mức độ ảnh hưởng của lỗi.

## 2. Vì sao không merge cả nhánh hotfix vào master?

Nhánh hotfix có hai commit với mục đích khác nhau:

1. Sửa mã và thêm test hồi quy.
2. Đặt version 1.0.1 và cập nhật changelog của dòng bảo trì.

Master đang chuẩn bị 1.1.0. Merge cả nhánh có thể kéo số phiên bản 1.0.1 và
những thay đổi riêng của bản cũ sang dòng phát triển mới, gây xung đột hoặc
lùi version. Vì vậy chỉ cherry-pick commit sửa lỗi; changelog của master
được cập nhật riêng và version vẫn là 1.1.0.

Commit sửa gốc dùng trong bài:

```text
ddffa0a2792b6407cb195d54b990e3d6e4f91066
```

PR #22 đưa hotfix vào release/lab04. PR #23 đưa bản sửa được cherry-pick vào
master, còn PR #24 đưa bản sửa được cherry-pick vào release/lab05.

## 3. Vì sao dùng cherry-pick -x và tách commit nâng phiên bản?

Cherry-pick áp dụng thay đổi của một commit lên nhánh hiện tại và thường
sinh commit mới có mã khác. Tùy chọn -x ghi dòng nguồn trong thông điệp:

```text
(cherry picked from commit ddffa0a2792b6407cb195d54b990e3d6e4f91066)
```

Dòng này giúp truy vết bản sửa gốc khi các dòng phiên bản có lịch sử riêng.
Trong bài có hai commit mang truy vết đó: 23c111f trên dòng master và
23aa682 trên dòng release/lab05.

Tách commit nâng version giúp chỉ lan truyền thay đổi cần thiết. Bản 1.0.x
được nâng thành 1.0.1, trong khi master và Lab 05 vẫn giữ 1.1.0. Việc chọn
commit không thay thế kiểm thử: mỗi dòng vẫn cần kiểm tra tích hợp riêng.

## 4. Vì sao chưa gắn v1.1.0 trước khi nhận hotfix?

Release/lab05 được tạo sau khi chuẩn bị version 1.1.0 nhưng trước khi nhận
bản sửa tìm kiếm. Nếu gắn tag ngay, tag sẽ trỏ tới bản vẫn còn lỗi. Tag đã
chia sẻ không được di chuyển tùy tiện; khi đó muốn phát hành bản sửa cần
một phiên bản mới như 1.1.1.

Trong bài, sau khi PR #24 được merge và 14 test thành công mới gắn annotated
tag v1.1.0. Nhánh release/lab04 nhận bản vá và được đánh dấu v1.0.1; tag
v1.0.0 vẫn giữ nguyên phiên bản ban đầu còn lỗi.

## 5. Lệnh nào giúp phát hiện một dòng phiên bản chưa nhận bản sửa?

Có thể phối hợp nhiều phép kiểm tra:

```powershell
git log --all --oneline --grep="cherry picked from commit ddffa0a2792b6407cb195d54b990e3d6e4f91066"
git tag --contains ddffa0a2792b6407cb195d54b990e3d6e4f91066
git cherry -v origin/master origin/release/lab04
```

- Log theo thông điệp nguồn tìm các lần cherry-pick có truy vết.
- Tag --contains kiểm tra quan hệ tổ tiên với commit gốc; không tự nhận ra
  một bản cherry-pick có mã khác nhưng cùng tác dụng.
- Git cherry so sánh patch-id: dấu - nghĩa là tìm thấy patch tương đương
  trong upstream; dấu + nghĩa là chưa nhận diện được patch tương đương.

Một dòng thiếu truy vết cần được kiểm tra thêm qua mã nguồn, lịch sử và
regression test. Không được kết luận chỉ dựa vào một lệnh hoặc một ký hiệu.

### Kết quả khác ví dụ trong slide

Trong repository này, git cherry hiển thị dấu + cho commit sửa gốc dù
master đã nhận sửa lỗi. Patch trên master có thêm ngữ cảnh hàm
search_by_category phía trên search_by_title, còn patch trên dòng 1.0.x
không có phần này. Ngữ cảnh diff khác nhau dẫn tới patch-id không trùng.

Đã đối chiếu mã nguồn, xác nhận nội dung test_search.py giống nhau và chạy
thử mã lấy trực tiếp từ v1.0.1, v1.1.0, origin/master. Cả ba đều tìm đúng
The Lion King với các từ khóa lion, LION và LiOn. Vì vậy dấu + trong trường
hợp này không chứng minh thiếu bản sửa và không phải lý do để cherry-pick
lại hoặc thay đổi tag.

## 6. Kết quả kiểm toán đa phiên bản

| Dòng phiên bản | Version | Unit test của dòng | Hành vi tìm lion |
| --- | --- | --- | --- |
| v1.0.0 | 1.0.0 | Baseline Lab 04 có 4 test | Không tìm thấy, dùng để tái hiện lỗi |
| v1.0.1 / release/lab04 | 1.0.1 | 7 test OK | Tìm thấy The Lion King |
| v1.1.0 / release/lab05 | 1.1.0 | 14 test OK | Tìm thấy The Lion King |
| master sau khi nhận hotfix | 1.1.0 | 14 test OK | Tìm thấy The Lion King |

Tag v1.0.1 và release/lab04 cùng trỏ tới 22d3134. Tag v1.1.0 và
release/lab05 cùng trỏ tới f0e4c2f tại thời điểm kiểm toán.

Diff từ v1.0.0 tới v1.0.1 chỉ có bốn file: aims/search.py,
tests/test_search.py, aims/__init__.py và CHANGELOG.md. Bản bảo trì không
nhận tính năng sắp xếp hoặc tìm theo thể loại của dòng 1.1.0.

Issue thực tế là #21, khác số minh họa #20 trong slide. PR vào master dùng
Fixes #21 để tự đóng Issue. Các PR vào nhánh release dùng tham chiếu Issue
để theo dõi việc áp dụng bản sửa.

## 7. CI kiểm soát thay đổi như thế nào?

PR #25 thêm .github/workflows/ci.yml. Workflow CI dùng Python 3.12, chạy
unittest cho PR vào master hoặc release/** và khi push vào master. Rule
master yêu cầu check test thành công trước khi merge, cùng với approval.
Workflow hiện được đưa vào master; không tự thêm vào các tag hoặc nhánh
release đã chốt. Bộ lọc sự kiện trong YAML không có nghĩa workflow đã tồn
tại trên mọi nhánh release.

Trên nhánh thử bugfix/ci-demo, commit 17407a7 cố ý cộng thêm 1 vào tổng tiền.
Bốn test thất bại. Trên GitHub, ngay cả sau khi partner approve, check
CI / test vẫn đỏ, được đánh dấu Required và nút merge bị khóa. Đây là minh
chứng CI chặn mã lỗi, độc lập với việc đã đủ approval.

PR thử chỉ phục vụ minh chứng, cần được đóng và không merge. Sau khi quay
lại master, toàn bộ 14 test thành công. Không đưa commit lỗi thử nghiệm vào
bản phát hành.

## 8. Ghi chú bài nộp

Giữ v1.0.1 trên dòng bảo trì Lab 04 và v1.1.0 trên dòng Lab 05. Không merge
ngược toàn bộ release vào master và không di chuyển các tag đã phát hành.
Câu trả lời được bổ sung vào master qua PR tài liệu sau khi chốt tag; nộp
kèm link tài liệu trên master hoặc PR tương ứng với nhánh release/lab05.
