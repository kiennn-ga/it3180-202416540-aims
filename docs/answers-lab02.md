# Trả lời câu hỏi thảo luận Lab 02

- Họ và tên: Nguyễn Thanh Kiên
- MSSV: 202416540
- Bài thực hành: Feature/Topic flow và Pull Request.

## 1. Vì sao phải đồng bộ master trước khi gửi PR?

Nhánh tính năng có thể được tạo từ một phiên bản master cũ. Trong khi phát
triển, các PR khác đã được merge vào master. Đồng bộ giúp kiểm tra tính
năng cùng các thay đổi mới nhất, phát hiện xung đột và lỗi tích hợp trước
khi đề nghị merge. Hai nhánh sửa các file khác nhau vẫn có thể gây lỗi hành
vi khi chạy chung, nên merge không xung đột chưa đủ để kết luận chương
trình đúng.

Trong bài, Dev 2 tạo feature/search-by-title trước khi tính năng in giỏ hàng
được merge. Sau khi commit hàm tìm kiếm, Dev 2 thực hiện:

```powershell
git fetch origin
git merge origin/master
python main.py
```

`git fetch` cập nhật thông tin nhánh remote, còn `git merge origin/master`
đưa các thay đổi mới vào nhánh tính năng hiện tại. Sau đó cần kiểm tra
chương trình tích hợp trước khi push và gửi PR. Trong quy trình thực tế,
nếu master tiếp tục thay đổi trong lúc review thì có thể cần đồng bộ và
kiểm tra lại.

## 2. Khi nào không được rebase?

Không tự ý rebase các commit đã chia sẻ và đang được người khác dựa vào,
đặc biệt là lịch sử của master hoặc nhánh release. Rebase tạo lại commit
với mã băm mới, có thể làm lịch sử của các thành viên khác bị lệch và dẫn
đến việc phải force push để thay thế lịch sử remote.

Nếu cần rebase một nhánh đã chia sẻ, phải phối hợp rõ ràng với những người
liên quan và tuân thủ chính sách repository. Với nhánh tính năng chỉ dùng
cục bộ, chưa chia sẻ, rebase thường phù hợp để sắp xếp lại lịch sử trước
khi công bố. Trong bài, Dev 2 dùng merge để đồng bộ với origin/master.

Thao tác Rebase and merge của PR #6 tạo commit mới trên master theo hướng
tiến lên, không viết lại các commit vốn đã có trên master. Vì vậy, thao tác
này khác với việc tự rebase và force push để thay thế lịch sử master.

## 3. feature/* khác topic/* ra sao?

Đây là quy ước đặt tên theo mục đích, không phải hai loại nhánh có cơ chế
khác nhau trong Git.

- `feature/*` dùng cho chức năng của ứng dụng, ví dụ feature/cart-print và
  feature/search-by-title.
- `topic/*` dùng cho một chủ đề công việc cụ thể như tài liệu hoặc cấu hình
  quy trình, ví dụ topic/pr-template và topic/use-case-diagram.

Theo quy trình bài thực hành, cả hai đều là nhánh ngắn hạn, được tạo từ
master, đưa thay đổi về master qua PR và xóa sau khi merge. Mỗi nhánh nên
có một mục đích rõ ràng để dễ review và truy vết.

## 4. So sánh ba kiểu merge qua lịch sử thực hành

| Kiểu merge | Đặc điểm | Dẫn chứng trong bài |
| --- | --- | --- |
| Merge commit | Giữ các commit của nhánh và tạo commit merge có hai parent; thấy rõ điểm phân nhánh và gộp nhánh. | PR #4: af53fe7, giữ ba commit 43e1a3c, 47ff4da và 9fd7327. |
| Squash and merge | Gộp thay đổi của PR thành một commit mới trên nhánh đích; các commit gốc của nhánh không trở thành tổ tiên chỉ nhờ thao tác squash. | PR #5: 1fa3912, feat: add search_by_title (#5). |
| Rebase and merge | Đưa các commit của PR lên đầu nhánh đích với mã mới, không tạo merge commit; giữ lịch sử tuyến tính. | PR #6: 3c8b182 thay cho commit nhánh 5bea60e. |

Merge commit phù hợp khi cần giữ bối cảnh và lịch sử chi tiết của nhánh.
Squash phù hợp khi muốn mỗi PR thành một đơn vị thay đổi dễ đọc và hoàn
tác. Rebase and merge phù hợp khi muốn giữ các bước commit có ý nghĩa nhưng
vẫn có lịch sử tuyến tính.

Sau squash hoặc rebase merge, Git có thể không nhận diện nhánh cũ đã merge
bằng quan hệ tổ tiên. Chỉ xóa nhánh bằng `git branch -D` sau khi xác nhận PR
đã merge và không còn thay đổi cần giữ.

## 5. Vai trò của review và branch protection trong bài

Branch protection yêu cầu thay đổi đi qua PR và có approval của người có
quyền phù hợp. Tác giả PR không tự approve PR của mình. Việc không cho phép
bypass giúp quy trình áp dụng cả với người quản trị repository.

Trong PR #4, partner nhận xét print_cart cần xử lý giỏ hàng trống. Sau khi
bổ sung xử lý, commit 9fd7327 được push lên cùng nhánh nên PR tự cập nhật.
Partner kiểm tra và approve lại trước khi merge. Tùy chọn dismiss stale
approvals tránh dùng approval cũ cho một phiên bản mã đã thay đổi.

Kết quả kiểm tra sau khi sửa: giỏ trống in `The cart is empty`; giỏ mẫu có
ba DVD vẫn in tổng tiền `63.89 $`.
