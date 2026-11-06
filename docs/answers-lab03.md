# Trả lời câu hỏi thảo luận Lab 03

- Họ và tên: Nguyễn Thanh Kiên
- MSSV: 202416540
- Bài thực hành: Bugfix flow, xung đột và hoàn tác.

## 1. Merge base là gì?

Merge base là tổ tiên chung tốt nhất của hai commit, được Git dùng làm mốc
để so sánh khi hợp nhất hai nhánh. Trong trường hợp thông thường, đó là
commit chung gần nhất trước khi hai nhánh phát triển tách biệt. Một lịch
sử phức tạp có thể có nhiều merge base.

Khi merge, Git so sánh mỗi phía với merge base để xác định thay đổi. Nếu hai
phía thay đổi cùng một vùng theo cách không thể tự kết hợp, Git báo xung đột
và yêu cầu người dùng lựa chọn hoặc kết hợp nội dung.

Có thể xem merge base bằng lệnh sau, với hai tham chiếu còn tồn tại:

```powershell
git merge-base <nhanh-thu-nhat> <nhanh-thu-hai>
```

Trong phần C, hai nhánh feature/vietnamese-messages và
feature/show-added-title cùng thêm thông báo tại một vị trí trong add_dvd.
Sau khi nhánh tiếng Việt vào master, merge master vào nhánh còn lại gây
xung đột. Nội dung được kết hợp thành:

```python
print(f"Đã thêm đĩa '{dvd.title}' vào giỏ hàng")
```

Commit c9ec418 ghi nhận việc giải quyết xung đột. Các dấu `<<<<<<<`, `=======`
và `>>>>>>>` được xóa, sau đó chạy bốn test thành công trước khi hoàn tất
merge và push. PR #13 được merge bằng merge commit 7021045.

## 2. Vì sao master và release/* phải dùng revert để hoàn tác lịch sử đã chia sẻ?

Master và các nhánh release là lịch sử dùng chung. Reset dịch chuyển con
trỏ nhánh; kết hợp với force push có thể thay thế lịch sử mà người khác đã
tải hoặc đang dựa vào. Việc này gây lệch lịch sử và làm mất dấu thay đổi
khỏi lịch sử nhánh.

Revert tạo commit mới đảo tác dụng của commit trước đó, giữ nguyên các
commit đã chia sẻ. Cả thay đổi gốc và quyết định hoàn tác đều truy vết được,
đồng thời có thể đưa qua PR để review và kiểm thử. Quy tắc này áp dụng khi
hoàn tác thay đổi đã chia sẻ; reset vẫn dùng được cho bài tập hoặc commit
cục bộ chưa công bố.

Trong bài, thay đổi của PR #13 được hoàn tác bằng:

```powershell
git switch -c bugfix/revert-show-added-title
git revert -m 1 --no-edit 7021045
```

Với commit merge, `-m 1` chọn parent thứ nhất làm dòng lịch sử chính để xác
định phần thay đổi cần đảo. Commit revert là 986e907. PR #14 đưa commit này
vào master qua merge commit 66e6026. Thông báo trở về tiếng Việt không kèm
tên DVD; bốn test vẫn thành công.

## 3. So sánh reset --soft, --mixed, --hard và vai trò reflog

| Lệnh | HEAD | Staging | Working directory |
| --- | --- | --- | --- |
| reset --soft | Chuyển tới commit đích | Giữ nguyên | Giữ nguyên |
| reset --mixed | Chuyển tới commit đích | Đặt lại theo commit đích | Giữ nguyên |
| reset --hard | Chuyển tới commit đích | Đặt lại theo commit đích | Đặt lại các file được theo dõi theo commit đích; thay đổi cục bộ có thể bị mất |

Trên nhánh topic/undo-practice không push, file undo-practice.txt được dùng
riêng cho bài tập. Sau soft reset, file ở staging với trạng thái `A`. Sau
mixed reset, vì file mới không có trong commit đích nên trở thành untracked
với trạng thái `??`. Sau khi commit lại và hard reset, file bị bỏ khỏi
working directory.

Reflog lưu các lần cập nhật tham chiếu trong repository cục bộ. Nhờ reflog,
commit 907038b đã được tìm lại và khôi phục trên nhánh nháp bằng:

```powershell
git reset --hard 907038b
```

File xuất hiện lại với nội dung `Lab 03 reset practice`. Reflog không phải
bản sao lưu vĩnh viễn: bản ghi có thể hết hạn và các đối tượng không còn
được tham chiếu có thể bị dọn dẹp. Nó cũng không tự khôi phục mọi thay đổi
chưa từng commit.

## 4. Bugfix từ master khác bugfix từ feature/* như thế nào?

Bugfix xuất phát từ master thường có PR đích là master. Bugfix xuất phát từ
một tính năng đang phát triển phải có PR đích là nhánh tính năng đó, để sửa
trong đúng bối cảnh và tránh đưa cả tính năng chưa hoàn chỉnh vào master.

- Phần A: bugfix/cart-limit-off-by-one xuất phát từ master, PR #9 vào master
  và tự đóng Issue #8 bằng từ khóa `Fixes #8`.
- Phần B: bugfix/discount-calculation xuất phát từ origin/feature/discount.
  PR #10 có base feature/discount. Sau khi nhận bản sửa, feature/discount
  mới được đưa vào master bằng PR #11.

## 5. Dẫn chứng test trước và sau khi sửa

Mã ban đầu của dự án đã chặn đúng DVD thứ 21 nhưng chưa trả về True/False.
Để làm đúng kịch bản bài tập, commit afae017 chuẩn bị lỗi mô phỏng bằng điều
kiện `>` và bổ sung giá trị trả về. Việc mô phỏng được ghi rõ trong Issue #8.

Commit 0783b48 thêm test trước commit sửa lỗi. Test thất bại vì DVD thứ 21
được chấp nhận và giỏ có 21 phần tử. Sau khi sửa điều kiện thành `>=`, test
thành công và giỏ giữ đúng 20 DVD.

Với giảm giá, công thức ban đầu trả về số tiền giảm thay vì số tiền còn
phải trả. Bản sửa f9ba0b8 dùng `total * (1 - percent / 100)` và kiểm tra
percent trong [0, 100]. Ba test bổ sung kiểm tra giảm 20%, các giá trị biên,
giỏ trống và percent không hợp lệ. Test cũ về giới hạn giỏ vẫn được giữ.

Trên master sau PR revert #14, lệnh sau cho kết quả `Ran 4 tests`, `OK`:

```powershell
python -m unittest discover -s tests -v
```

## 6. Theo dõi checklist nộp bài

- [x] Issue #8 đã Closed và liên kết PR #9.
- [x] Commit test tái hiện lỗi đứng trước commit sửa lỗi.
- [x] PR bugfix #10 có base feature/discount.
- [x] Master có bốn test thành công sau PR revert #14.
- [x] Xung đột đã được giải quyết và có PR revert #14.
- [ ] Đưa câu trả lời này vào master qua PR.
- [ ] Tạo và push release/lab03 từ master sau khi merge tài liệu.
