# 🗣️ Ứng dụng Chuyển Giọng Nói Thành Văn Bản (Tiếng Việt)

> Phiên bản V1.1: Cải tiến để tải lên và xử lý các tệp âm thanh m4a có thời lượng tối đa 20 phút


<b>Hiện tại bạn có thể sử dụng phiên bản trực tuyến tại: https://speech-to-text-5567.onrender.com/</b><br>
Và bạn cũng có thể đọc <a href="https://hackmd.io/@trhgtung/speech-to-text-trhgtung" target="_blank">tài liệu hướng dẫn ngay tại đây</a><br>

Ứng dụng này giúp bạn:
- Ghi âm bằng micro trực tiếp trên trình duyệt
- Tải lên file âm thanh `.m4a` (ghi âm từ iPhone)
- Nhận kết quả văn bản Tiếng Việt
- Tải về file `.txt` kết quả

---
Dưới đây là hướng dẫn dành cho máy tính Windows:
(Nếu bất đắc dĩ có lỗi chặn xảy ra từ phía Windows Defender, hãy tắt Windows Defender / Windows Security hoặc các trình AntiVirus đi)

## 🧩 BƯỚC 1: Cài đặt Python

1. Truy cập: https://www.python.org/downloads/
2. Tải về **Python 3.11**
3. Khi cài đặt:
   - ✅ Tích vào ô **Add Python to PATH**
   - Nhấn **Install Now**
4. Mở một cửa sổ Command Prompt mới, nhập lệnh `python3 --version` -> Enter : nếu Command Prompt phản hồi bạn với nội dung "Python 3.11" thì bạn đã cài đặt đúng phiên bản của Python (cài Python thành công)
5. Nếu đã cài đúng, bạn có thể đóng cửa sổ Command Prompt này lại. Nếu chưa cài được, thì cài lại.

---

## 🧩 BƯỚC 2: Tải mã nguồn ứng dụng


- Truy cập trang mã nguồn: https://github.com/TrHgTung/Speech-To-Text
- Trong phần Release: nhấn tải xuống source code
- Ghi nhớ vị trí thư mục lưu source code trong máy tính của bạn


## 🧩 BƯỚC 3: Cài đặt môi trường cần thiết

- Mở Windows Explorer (truy cập tới thư mục chứa source code)
- Trên thanh tìm kiếm, xóa sạch địa chỉ và nhập cmd và nhấn Enter
- Ngay lập tức, một cửa sổ dòng lệnh xuất hiện, nhập lần lượt các lệnh sau (tức là sau khi nhập từng câu lệnh rồi Enter, đợi hiển thị kết quả rồi mới tiếp tục tới câu lệnh kế tiếp)
    + `python3 --version` -> Enter : nếu hiển thị Python 3.11 thì bạn đã cài đặt đúng phiên bản của Python
    + `python3 -m venv venv` -> Enter: đợi một lúc để python tự tạo môi trường ảo trong thư mục source code
    + `venv\Scripts\activate` -> Enter: dùng để kích hoạt chế độ môi trường ảo của Pythong trong thư mục source code. Kể từ giờ, mọi câu lệnh trong cửa sổ dòng lệnh đều thực thi trong môi trường ảo của Python. Bạn dễ dàng nhận ra khi có tiền tố (venv) nằm trước câu lệnh
    + `pip install -r requirements.txt`-> Enter: Dùng để cài đặt toàn bộ thư viện cần thiết để source code có thể hoạt động được. Quá trình cài đặt này mất khá nhiều thời gian (trong khoảng 5 - 10 phút tùy kết nối mạng và cấu hình phần cứng máy tính)

- Cài đặt phần mềm xử lý âm thanh (FFmpeg) cho Windows:
    + Truy cập tại: https://www.gyan.dev/ffmpeg/builds/ffmpeg-git-full.7z để tải công cụ FFmpeg cho Windows
    + Sau khi tải về, giải nén file ffmpeg-git-full.7z. Sau đó, vào thư mục ffmpeg-git-full > rồi vào thư mục bin
    + Copy đường dẫn của thư mục đó (copy địa chỉ dẫn tới thư mục bin trên thanh địa chỉ của cửa sổ Windows Explorer). VD: đường dẫn mà bạn copy được kiểu kiểu như: C:\Users\TênCủaBạn(Admin)\Downloads\ffmpeg-git-full\bin


- Thêm FFmpeg vào Biến môi trường hệ thống Windows (System Environment Variables):
    + Mở menu Start, gõ Environment Variables và chọn mục: Edit the system environment variables
    + Trong hộp thoại hiện ra, nhấn nút Environment Variables...
    + Ở phần System variables: Tìm dòng tên là Path → Nhấn Edit
    + Trong cửa sổ mới hiện ra: Nhấn New -> Dán đường dẫn thư mục bin bạn đã sao chép ở bước trên vào
    (ví dụ:  C:\Users\TênCủaBạn(Admin)\Downloads\ffmpeg-git-full\bin)
    + Nhấn OK tất cả các cửa sổ để lưu lại.


- Kiểm tra FFmpeg đã được thêm hay chưa?
    + Mở một cửa sổ Command Prompt khác (gõ cmd trong Start menu)
    + Gõ lệnh sau: `ffmpeg -version` -> Enter: Nếu bạn thấy các dòng thông tin phiên bản hiện ra (ví dụ "ffmpeg version 6.0 ...") thì FFmpeg đã được cài đặt toàn cục
    + Nếu chưa thấy gì thì cài lại, còn thấy version rồi thì đóng cửa sổ này lại

## 🧩 BƯỚC 4: Khởi chạy ứng dụng
- Quay lại cửa sổ Command Prompt ban đầu (hãy đảm bảo vẫn còn môi trường ảo - bằng cách nhìn thấy tiền tố (venv) ở đằng trước câu lệnh)
- Nhập lệnh: `python3 app.py` -> Enter: đợi một lúc và ứng dụng sẽ chạy ở địa chỉ http://127.0.0.1:10000
- Bạn mở trình duyệt bất kỳ, truy cập: http://127.0.0.1:10000 để sử dụng các tính năng
- Trong lần đầu chạy, hãy cấp quyền truy cập micro và quyền truy cập tệp tin (nếu bạn vô tình chặn)

## 🧩 Sau này mỗi lần muốn chạy ứng dụng ở máy tính cá nhân (local) - bạn chỉ cần:
- Truy cập đến thư mục chứa source code, tại đây mở một cửa sổ Command Prompt mới
- Kích hoạt môi trường ảo: trong cửa sổ Command Prompt hãy nhập lệnh `venv\Scripts\activate` -> Enter : sau đó môi trường ảo sẽ được kích họat - bạn kiểm tra bằng cách nhìn thấy tiền tố (venv) ở đằng trước câu lệnh.
- Nhập lệnh: `python3 app.py` -> Enter: đợi một lúc và ứng dụng sẽ chạy ở địa chỉ http://127.0.0.1:10000
- Bạn mở trình duyệt bất kỳ, truy cập: http://127.0.0.1:10000 để sử dụng các tính năng
- Trong trường hợp mất quyền truy cập micro trên trình duyệt, hãy cấp quyền truy cập micro

### Khả năng dùng chung nhiều thiết bị
** <b>Yêu cầu</b>: Các thiết bị muốn sử dụng chung tính năng, phải có cùng kết nối Internet với máy tính của bạn (để thiết lập thành một mạng cục bộ - LAN) . Và đồng thời trên máy tính của bạn (tạm gọi là máy chủ) phải đang chạy source (tức đã chạy lệnh `python3 app.py` và luôn chạy liên tục, không dừng / không sleep / không shutdown)
- Đối với các máy đã có cùng kết nối wifi với máy tính của bạn:
    - Trên các thiết bị dùng chung (smartphone, tablet, PC khác): truy cập đến địa chỉ: `http://192.168.1.10:10000` (không cần gõ `http://` -- Và nhắc một lần nữa: phải chung wifi với máy chủ, và trên máy chủ phải đang chạy source)
    - Tính năng trên các thiết bị dùng chung vẫn tương tự như trên máy chủ

- Trong trường hợp trên máy chủ, bạn đã tắt Command Prompt / shutdown hoặc Sleep máy: việc này đồng nghĩa với đã tắt source, thì tính năng sẽ không còn khả dụng trên máy chủ lẫn các thiết bị dùng chung.

### Các thư viện được sử dụng
- Flask, pydub, SpeechRecognition, TailwindCSS
- Được triển khai với Render (https://render.com/ - Cloud Application Flatform - Render)

> Hoàng Tùng | Ứng dụng chuyển đổi giọng nói thành văn bản | Lần cập nhật cuối 13/4/2025

> Dựa trên đơn yêu cầu của X** P*** Studio (giấu tên)