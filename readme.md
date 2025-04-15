# 🗣️ Ứng dụng Chuyển Giọng Nói Thành Văn Bản (Tiếng Việt)

> Phiên bản V1.1: Cải tiến để tải lên và xử lý các tệp âm thanh m4a có thời lượng tối đa 20 phút


<b>Hiện tại bạn có thể sử dụng phiên bản trực tuyến tại: https://speech-to-text-5567.onrender.com/</b> (Lưu ý: đây là đường link cho <b> mục đích thử nghiệm</b>, không dùng cho production vì không đảm bảo tính ổn định về mặt chịu tải. Khuyến khích tải về và tự triển khai trên máy chủ riêng hoặc test trên máy cá nhân)<br>
Và bạn cũng có thể đọc <a href="https://hackmd.io/@trhgtung/speech-to-text-trhgtung" target="_blank">tài liệu hướng dẫn ngay tại đây</a><br>

Ứng dụng này giúp bạn:
- Ghi âm bằng micro trực tiếp trên trình duyệt
- Tải lên file âm thanh `.m4a` (ghi âm từ iPhone / iPad)
- Nhận kết quả văn bản Tiếng Việt
- Tải về file `.txt` kết quả

---
Dưới đây là hướng dẫn dành cho máy tính Windows:
(Nếu bất đắc dĩ có lỗi chặn xảy ra từ phía Windows Defender, hãy tắt Windows Defender / Windows Security hoặc các trình Anti-virus đi)

## 🧩 BƯỚC 1: Cài đặt Python

(Trong trường hợp máy bạn đã cài đặt sẵn Python phiên bản 3.11, thì bỏ qua bước này. Cách kiểm tra máy đã cài sẵn Python 3.11 hay chưa: Mở cửa sổ Command Prompt -> nhập `python3 --version` -> Enter -> Nếu màn hình hiển thị phiên bản Python 3.11 thì máy đã cài sẵn Python 3.11. Nếu chưa cài đặt thì màn hình sẽ hiển thị rằng Python là một lệnh mà Windows không hiểu được, và bạn phải thực hiện Bước 1 này)

1. Mở trình duyệt, truy cập: https://www.python.org/downloads/
2. Tải về **Python 3.11 dành cho Windows** theo hướng dẫn của Website
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
    - Đầu tiên: trên máy chủ phải đảm bảo đã thiết lập các môi trường cần thiết và đang chạy lệnh `python3 app.py`. Trên Command Prompt của máy chủ đang chạy lệnh, phải đang hiển thị các thông tin kiểu kiểu như sau:
    
    Command Prompt / Terminal:
    > (venv) hoangtung@hoangtung-ubuntu:~/speech_to_text_project$ python3 app.py 
    > * Serving Flask app 'app'
    > * Debug mode: off
    > WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
    > * Running on all addresses (0.0.0.0)
    > * Running on http://127.0.0.1:10000
    > * Running on http://192.168.1.10:10000
    > Press CTRL+C to quit
    - Bạn nhìn thấy dòng `Running on http://192.168.1.10:10000` chứ? Đây chính là địa chỉ dành cho các thiết bị khác muốn dùng chung tính năng của source code. Tùy vào kết nối của máy chủ trong hệ thống mạng nên địa chỉ này sẽ khác nhau, nhưng cùng chung một kiểu là `http://192.168.1.xxx:10000` (với xxx trải từ 1 đến 255 tùy máy chủ)
    - Trên các thiết bị dùng chung (smartphone, tablet, PC khác): truy cập đến địa chỉ: `http://192.168.1.xxx:10000` - Ví dụ của tôi: `http://192.168.1.10:10000` (Và nhắc một lần nữa: phải chung wifi với máy chủ, và trên máy chủ phải đang chạy source)
    - Tính năng trên các thiết bị dùng chung vẫn tương tự các tính năng như trên máy chủ: gồm tải lên tệp âm thanh và ghi âm trực tiếp.

- Trong trường hợp trên máy chủ, bạn đã tắt cửa sổ Command Prompt chạy source / shutdown máy hoặc Sleep máy: thì việc này đồng nghĩa với bạn đã tắt source, tính năng sẽ không còn khả dụng trên máy chủ lẫn các thiết bị dùng chung.

### Các thư viện được sử dụng
- Flask, pydub, SpeechRecognition, TailwindCSS
- Được triển khai với Render (https://render.com/ - Cloud Application Flatform - Render)

### Khác
- Hiện tại đã có thể chạy với Docker:
    + Cài Docker
    + Chạy docker build lần đầu: docker build -t speech-to-text-app .
    + Chạy ứng dụng: docker run -p 10000:10000 speech-to-text-app
    + Sau khi chạy, ứng dụng sẽ chạy trên `http://127.0.0.1:10000` và trên các thiết bị chung mạng wifi

- Nếu có thắc mắc gì với Repository này, hãy để lại ở phần Issues (GitHub). Rất mong nhận được sự đóng góp thêm của các bạn tại phần Pull requests (GitHub)
- Repository này đã được đồng ý để mở công khai.

> Hoàng Tùng (TrHgTung) | Ứng dụng chuyển đổi giọng nói thành văn bản | Lần cập nhật cuối 13/4/2025

> Dựa trên đơn yêu cầu của X** P*** Studio (giấu tên)