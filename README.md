# Trò Chơi Ô Ăn Quan - Game Dân Gian Việt Nam

## 1. Ngôn ngữ lập trình và Công cụ sử dụng
- **Ngôn ngữ cốt lõi:** Python (Khuyến nghị chạy trên Python 3.8 đến 3.12). Python được sử dụng vì tính linh hoạt, syntax rõ ràng, dễ dàng triển khai logic phức tạp cho các dạng board game.
- **Thư viện đồ họa:** `pygame` (phiên bản 2.x). Đây là bộ toolkit 2D standard của Python, sử dụng đa luồng (Event Loop) nhằm kết xuất khung hình, tương tác con trỏ chuột, xử lý timer, load âm thanh và textures.
- **Mô hình lập trình:** Mã nguồn đợc tổ chức theo kiến trúc modular hóa:
  - `game.py`: Nền tảng cốt lõi chứa logic (State-machine, luật ăn sỏi, quy tắc rải).
  - `ui.py` & `play_ui.py`: Backend giao diện, Animation Loop và Game render.
  - `ai.py`: Xử lý AI, sử dụng thuật toán Minimax kết hợp hàm lượng giá (Heuristic Evaluation) để tạo lối đánh thông minh.
  - Thư mục `test`: Hệ thống Unit Test tự động (sử dụng thư viện `unittest` mặc định).

## 2. Hướng dẫn cài đặt và khởi chạy
### Yêu cầu hệ thống
- Môi trường: Windows, MacOS hoặc Linux.
- Đã cài đặt [Python](https://www.python.org/downloads/) và có biến môi trường hỗ trợ gọi `python` cùng `pip`.

### Thiết lập môi trường (Khuyến nghị)
Sử dụng Virtual Environment (venv) trên Terminal (với Windows Powershell):
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Sau khi Terminal báo ảo hóa thành công, bạn cập nhật pip và cài đặt thư viện:
```powershell
python -m pip install --upgrade pip
pip install pygame
```

### Chạy Game
Tại thư mục chứa dự án, khởi chạy script chính để mở Menu trò chơi:
```cmd
python main.py
```

---

## 3. Hướng dẫn chơi Game Ô Ăn Quan

### Mục Tiêu
Bàn cờ gồm 10 ô Dân (chia đôi 2 bờ) và 2 ô Quan (lớn nhất ở góc). Mục tiêu của bạn là tính toán để "Ăn" được tổng khối lượng dân và quan lớn hơn đối thủ. Sỏi (Dân) tính 1 điểm, Quan tính 10 điểm (được quy đổi sang hình ảnh dân tích lũy).

### Thao tác điều khiển chính
1. **Lựa Chọn:** 
   - Khi tới lượt, nhấn **chuột trái (Click)** vào một trong 5 ô Dân thuộc lãnh thổ của bạn để đếm sỏi. Ô đang chọn sẽ báo sáng (viền vàng).
2. **Chọn Hướng Đi:** 
   - Màn hình sẽ nổi 2 mũi tên điều hướng `<` và `>`. Dùng **chuột Click** vào mũi tên (hoặc ấn nhanh phím mũi tên Màn hình Trái/Phải của bàn phím) để Quyết định thả dọc chiều Kim đồng hồ hoặc Ngược chiều.

### Cơ chế & Luật lệ trong Game
- **Nguyên lý Rải:** Cầm x(n) viên sỏi, rải lần lượt từng cái một, đi qua các ô hướng tới.
- **Được đi tiếp:** Nếu sỏi cuối rụng ngay trước một ô Dân CÓ QUÂN. Lập tức túm gọn ô đấy và... tiếp tục hành trình rải đi!
- **Mất lượt (Chạm Quan):** Nếu sỏi cuối cùng chạm đất ngay trước mũi Ô QUAN, bạn không được bốc quan đi rải mà phải ngừng ngay lại lập tức để nhường lượt cho đối thủ.
- **Ăn Điểm (Ghi bàn):** Mấu chốt tựa game! Rải sỏi cuối cùng rơi trước 1 Ô TRỐNG, và liền kề bên kia của ô trống đó lại là một Ô CÓ QUÂN. Lập tức sỏi ở ô có quân kia chui hết vào túi bạn làm điểm!
- **Ăn Rền (Đỉnh cao):** Nếu đằng sau ô vừa bị ăn TRỐNG -> lại tiếp tục gặp ô CÓ QUÂN => Bạn sẽ cuốn sạch cả chặng đường (Ăn chuỗi liên hoàn)!
- **Tái thiết "Làng":** Nếu đến lượt và 5 ô nhà bạn trống trơn, hệ thống tự thanh toán 5 Điểm từ kho của bạn để thả 5 viên mồi vô 5 ô để chơi tiếp.
- **Vơ Vét & Hết Game:** Ngay khi 2 Ô Quan hoàn toàn "mất tích" sỏi. Trò chơi chốt sổ! Các tiểu Dân còn lang thang bên bờ ruộng nhà ai thì chạy tuột về làm điểm của nhà đó. Đếm tài sản là biết AI WIN!

**Chúc bạn có những màn đấu trí tuổi thơ đầy cuốn hút cùng PyGame!**