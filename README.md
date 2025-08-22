# 📡 Mô phỏng mạng IoT sử dụng giao thức MQTT

---

## Mục lục
- [Giới thiệu](#giới-thiệu)
- [Tính năng chính](#tính-năng-chính)
- [Kiến trúc & Sơ đồ hệ thống](#kiến-trúc--sơ-đồ-hệ-thống)
- [Công nghệ sử dụng](#công-nghệ-sử-dụng)
- [Yêu cầu hệ thống](#yêu-cầu-hệ-thống)
- [Cài đặt](#cài-đặt)
- [Chạy nhanh (Quick Start)](#chạy-nhanh-quick-start)
- [Cấu hình (Broker/Topic)](#cấu-hình-brokertopic)
- [Cấu trúc thư mục](#cấu-trúc-thư-mục)
- [Kết quả kỳ vọng](#kết-quả-kỳ-vọng)
- [Khắc phục lỗi thường gặp](#khắc-phục-lỗi-thường-gặp)
- [Câu hỏi thường gặp (FAQ)](#câu-hỏi-thường-gặp-faq)
- [Ghi chú nộp bài](#ghi-chú-nộp-bài)
- [Thông tin](#thông-tin)
- [Giấy phép (tùy chọn)](#giấy-phép-tùy-chọn)

---

## Giới thiệu
Dự án mô phỏng mạng **IoT** sử dụng giao thức **MQTT** bằng Python.
- **Publisher**: sinh dữ liệu cảm biến ngẫu nhiên (nhiệt độ, độ ẩm) và gửi lên MQTT Broker.
- **Subscriber (Ứng dụng GUI)**: nhận dữ liệu, hiển thị **log** và **biểu đồ realtime**, đồng thời **lưu SQLite** để xem lại.

Use case: học tập/nghiên cứu nguyên lý hoạt động MQTT, demo cho báo cáo niên luận.

---

## Tính năng chính
- Kết nối tới broker công cộng `test.mosquitto.org` (hoặc broker nội bộ).
- Gửi/nhận dữ liệu 2 topic: `sensor/temperature`, `sensor/humidity`.
- Giao diện Tkinter + biểu đồ Matplotlib **realtime**.
- Lưu lịch sử vào SQLite (`sensor_data.db`).

---

## Kiến trúc & Sơ đồ hệ thống
Luồng hoạt động:
1. **Sensor (giả lập)** → tạo dữ liệu.
2. **Publisher** → publish dữ liệu lên **MQTT Broker**.
3. **Subscriber (GUI)** → subscribe topic, hiển thị log + biểu đồ, lưu DB.

---

## Công nghệ sử dụng
- **Python 3.10+**
- **paho-mqtt** (MQTT client)
- **Tkinter** (GUI)
- **matplotlib** (biểu đồ)
- **sqlite3** (lưu dữ liệu cục bộ)

---

## Yêu cầu hệ thống
- Python 3.10 trở lên (Windows/macOS/Linux).
- Kết nối Internet (nếu dùng broker công cộng).

---

## Cài đặt
Cài thư viện cần thiết:
```bash
pip install paho-mqtt matplotlib
```

Tkinter & sqlite3 đã tích hợp sẵn trong bản Python chính thức (Windows/macOS). Trên Linux, nếu thiếu Tkinter, cài thêm theo distro (ví dụ Ubuntu: `sudo apt-get install python3-tk`).

---

## Chạy nhanh (Quick Start)

### 1) Chạy Subscriber (giao diện hiển thị dữ liệu)
```bash
python subscriber_app.py
```

### 2) Chạy Publisher (gửi dữ liệu giả lập)
```bash
python publisher.py
```

### 3) Quan sát
- Log hiển thị bản tin MQTT nhận được.
- Biểu đồ cập nhật **theo thời gian thực**.
- CSDL `sensor_data.db` xuất hiện trong cùng thư mục.

---

## Cấu hình (Broker/Topic)
Mặc định code kết nối:
```python
client.connect("test.mosquitto.org", 1883, 60)
```
- Đổi sang broker cục bộ: thay `"test.mosquitto.org"` bằng IP máy chạy broker (ví dụ `"192.168.1.10"`).
- Topic mặc định: `sensor/temperature`, `sensor/humidity`. Có thể đổi trong code publisher/subscriber cho đồng nhất.

---

## Cấu trúc thư mục
Gợi ý cấu trúc repo:
```
mqtt-iot-simulation/
├─ subscriber_app.py        # Ứng dụng GUI: log + biểu đồ + SQLite
├─ publisher.py             # Sinh & publish dữ liệu giả lập
├─ README.md                # Tệp hướng dẫn (file này)
└─ assets/                  # Ảnh minh họa (tự tạo folder này)
   ├─ system_diagram.png    # Sơ đồ hệ thống (tùy chọn)
   └─ app_screenshot.png    # Ảnh chụp giao diện (tùy chọn)
```

---

## Kết quả kỳ vọng
- Kết nối thành công tới broker công cộng **test.mosquitto.org**.
- Log nhận dữ liệu đều đặn mỗi vài giây.
- Biểu đồ hiển thị 2 đường: **Temperature (°C)** và **Humidity (%)**.
- Dữ liệu được lưu xuống **SQLite** để phân tích sau.

---

## Khắc phục lỗi thường gặp

**1) `python: command not found` / không nhận lệnh `python`**
- Cài Python từ https://www.python.org/ (nhớ tick **Add python.exe to PATH** trên Windows).
- Hoặc dùng `py` (Windows): `py subscriber_app.py`.

**2) `ModuleNotFoundError: No module named 'paho'`**
- Chưa cài thư viện. Chạy:
  ```bash
  pip install paho-mqtt
  ```

**3) Mở được app nhưng biểu đồ trống (không có 2 đường đỏ/xanh)**  
- Bạn **chưa chạy publisher**, hoặc publisher không publish đúng topic.
- Mở 2 terminal: một chạy `subscriber_app.py`, một chạy `publisher.py`.

**4) Không kết nối được broker công cộng**
- Broker công cộng có thể tạm quá tải. Thử lại sau hoặc dùng broker nội bộ (Mosquitto).

**5) Tkinter lỗi trên Linux**
- Cài bổ sung: `sudo apt-get install python3-tk` (Ubuntu/Debian).

---

## Câu hỏi thường gặp (FAQ)

**Q: Có cần cài SQLite riêng không?**  
A: Không. `sqlite3` tích hợp sẵn trong Python.

**Q: Có cần internet?**  
A: Nếu dùng broker công cộng → CÓ. Broker nội bộ trong LAN thì không cần internet.

**Q: Làm sao đổi tần suất gửi dữ liệu?**  
A: Mở `publisher.py`, chỉnh `time.sleep(5)` sang số giây mong muốn.

**Q: Lưu file DB ở đâu?**  
A: Cùng thư mục với code, tên `sensor_data.db` (có thể đổi trong `subscriber_app.py`).


---

## Thông tin
- **Sinh viên**: Lê Thị Khánh Ly
- **Mã sinh viên**: 22T1020661
- **Môn học**: Thực tập viết niên luận
- **Đề tài**: Mô phỏng mạng IoT sử dụng giao thức MQTT

---
- Nếu không yêu cầu: có thể bỏ trống phần này.
- Nếu muốn công khai: tham khảo giấy phép **MIT**.
