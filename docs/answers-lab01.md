# Trả lời câu hỏi thảo luận Lab 01

- Họ và tên: Nguyễn Thanh Kiên
- MSSV: 202416540
- Bài thực hành: Thiết lập môi trường và Refactor flow với Git/GitHub.

## 1. Cấu hình `--global` được lưu ở đâu? Khác gì với `--local`?

Cấu hình `--global` thường được lưu trong file `~/.gitconfig`. Trên Windows,
đường dẫn thông thường là `C:\Users\ASUS\.gitconfig`. Git cũng hỗ trợ file
cấu hình người dùng tại `$XDG_CONFIG_HOME/git/config`, hoặc
`~/.config/git/config` nếu biến môi trường này chưa được đặt.

Cấu hình `--global` áp dụng cho các repository của tài khoản người dùng hiện
tại. Cấu hình `--local` được lưu trong `.git/config` của repository và chỉ áp
dụng cho repository đó. Nếu cùng một tùy chọn được đặt ở cả hai phạm vi thì
giá trị `--local` được ưu tiên hơn `--global`.

Ví dụ, có thể đặt tên và email mặc định bằng `--global`, sau đó dùng `--local`
để đặt email riêng cho một dự án. Có thể kiểm tra giá trị và nơi lưu bằng:

```powershell
git config --list --show-origin
```

## 2. Vì sao dùng `git mv`?

`git mv` chuyển hoặc đổi tên file, đồng thời cập nhật staging để Git ghi nhận
đường dẫn cũ bị bỏ và đường dẫn mới được thêm vào. Cách này thuận tiện và
giảm nguy cơ quên đưa một phần thay đổi vào staging so với di chuyển file thủ
công rồi chạy `git add`.

Trong bài thực hành, hai lệnh được dùng là:

```powershell
git mv dvd.py aims/dvd.py
git mv cart.py aims/cart.py
```

Git nhận diện việc đổi tên dựa trên độ tương đồng của nội dung; Git không lưu
một bản ghi đổi tên riêng chỉ vì dùng `git mv`. Vì vậy, di chuyển thủ công rồi
stage đúng các thay đổi vẫn có thể cho kết quả tương đương.

Lệnh sau cho phép xem lịch sử của `cart.py` qua lần đổi đường dẫn:

```powershell
git --no-pager log --oneline --follow -- aims/cart.py
```

Kết quả thực hành có cả commit `f0f7032` chuyển file và commit `eacf3c0` thêm
mã nguồn ban đầu, cho thấy vẫn có thể truy vết lịch sử trước khi refactor.

## 3. `release/lab01` có phải baseline không?

Có. Trong quy trình của bài thực hành, phiên bản đã hoàn thành và được chốt
trên nhánh `release/lab01` được dùng làm baseline của Lab 01. Đây là mốc tham
chiếu để nộp bài, so sánh thay đổi và tái tạo phiên bản khi cần kiểm tra.

Sau khi merge PR refactor vào `master`, nhánh `release/lab01` được tạo từ
`master` và đẩy lên GitHub. Tại thời điểm hoàn thành bài, lệnh:

```powershell
git rev-parse origin/master origin/release/lab01
```

trả về cùng một mã commit cho cả hai nhánh:

```text
5d4240e7fa19a419d14abb1b2cdf302cdf2cd8c7
5d4240e7fa19a419d14abb1b2cdf302cdf2cd8c7
```

Tuy nhiên, nhánh là một tham chiếu có thể dịch chuyển khi có commit mới.
Vì vậy, cần quản lý và bảo vệ nhánh release theo quy trình; mã commit cụ thể
mới xác định chính xác nội dung baseline. Khi học đến phần tag, có thể gắn
tag phát hành để đánh dấu rõ mốc này.

## 4. Vì sao không commit thẳng vào `master` dù làm một mình?

Sau bước khởi tạo ban đầu, dùng nhánh riêng và Pull Request giúp thực hiện
đúng quy trình kiểm soát thay đổi của bài thực hành. Mỗi nhánh có một mục
đích rõ ràng; `master` chỉ nhận thay đổi sau khi đã kiểm tra.

Pull Request tập hợp mục đích, các file thay đổi và kết quả kiểm thử ở cùng
một nơi. Khi làm một mình, đây vẫn là cơ hội tự xem lại mã nguồn trước khi
merge, phát hiện file thừa, import sai hoặc thay đổi ngoài phạm vi. Khi làm
nhóm, cùng quy trình này cho phép người khác review và phối hợp công việc.

Trong Lab 01, nhánh `refactor/apply-release-flow` chứa hai commit: chuyển mã
nguồn vào package `aims`, sau đó sửa import trong `main.py`. Chương trình
được kiểm tra và vẫn in `Total cost: 63.89 $`. PR #1 được merge vào `master`,
rồi nhánh refactor được xóa. Lịch sử commit và PR vẫn lưu lại thay đổi để
phục vụ truy vết.
