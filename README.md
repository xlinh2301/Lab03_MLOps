<!-- Banner -->
<p align="center">
  <a href="https://www.uit.edu.vn/" title="Trường Đại học Công nghệ Thông tin" style="border: none;">
    <img src="https://i.imgur.com/WmMnSRt.png" alt="Trường Đại học Công nghệ Thông tin | University of Information Technology">
  </a>
</p>

<h1 align="center"><b>MLops</b></h1>

<div align="center">
  <table>
    <thead>
      <tr>
        <th>STT</th>
        <th>MSSV</th>
        <th>Họ và Tên</th>
        <th>Chức vụ</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>1</td>
        <td>22520646</td>
        <td>Nguyễn Quốc Khánh</td>
        <td>Nhóm trưởng</td>
      </tr>
      <tr>
        <td>2</td>
        <td>22520775</td>
        <td>Nguyễn Xuân Linh</td>
        <td>Thành viên</td>
      </tr>
      <tr>
        <td>3</td>
        <td>22521677</td>
        <td>Nguyễn Thế Vĩnh</td>
        <td>Thành viên</td>
      </tr>
      <tr>
        <td>4</td>
        <td>22521671</td>
        <td>Lưu Khánh Vinh</td>
        <td>Thành viên</td>
      </tr>
    </tbody>
  </table>
</div>

# GIỚI THIỆU KHÓA HỌC
* **Tên Khóa Học:** MLOps - Phát triển và vận hành hệ thống máy học.
* **Mã Lớp:** CS317.P21.
* **Năm Học:** HK2 (2024 - 2025).
* **Giảng Viên**: Th.S Đỗ Văn Tiến, Lê Trần Trọng Khiêm

# Bài Lab 2: Phục vụ Mô hình và Giám sát

Dự án này thiết lập một API phục vụ mô hình học máy với giám sát sử dụng Prometheus và Grafana.

## Cấu trúc Dự án

```
cs317-lab2/
├── monitoring/
│   ├── alertmanager.yml
│   ├── grafana-docker-compose.yml
│   ├── prometheus-3.4.1.linux-amd64/
│   │   ├── prometheus.yml
│   │   └── alert.rules.yml
│   └── promtail-config.yaml
└── service-api/
    ├── main.py
    ├── Dockerfile
    ├── requirements.txt
    └── model.pth
```

## Thiết lập

### Yêu cầu

*   Docker
*   Docker Compose

## Tải xuống và Cài đặt Prometheus và Promtool

Vì các tệp nhị phân `prometheus` và `promtool` có kích thước lớn, chúng không được bao gồm trong kho lưu trữ. Bạn có thể tải chúng xuống riêng bằng các bước sau:

1. **Tải xuống Prometheus:**
   - Truy cập [trang tải xuống Prometheus](https://prometheus.io/download/).
   - Tải xuống phiên bản phù hợp với hệ điều hành của bạn.
   - Giải nén tệp đã tải xuống và sao chép tệp nhị phân `prometheus` vào `monitoring/prometheus-3.4.1.linux-amd64/`.

2. **Tải xuống Promtool:**
   - Tệp nhị phân `promtool` được bao gồm trong cùng một tệp nén với Prometheus.
   - Sao chép tệp nhị phân `promtool` vào `monitoring/prometheus-3.4.1.linux-amd64/`.

Đảm bảo cả hai tệp nhị phân đều có thể thực thi và nằm trong thư mục đúng trước khi khởi động các dịch vụ.

### Cài đặt

1.  **Clone kho lưu trữ:**
    ```bash
    git clone https://github.com/xlinh2301/Lab03_MLOps.git
    cd Lab03_MLOps
    ```

2.  **Xây dựng và chạy các dịch vụ:**
    ```bash
    cd monitoring
    docker-compose -f grafana-docker-compose.yml up -d --build
    ```
    Lệnh này sẽ xây dựng hình ảnh Docker cho dịch vụ FastAPI và khởi động tất cả các dịch vụ được định nghĩa trong `grafana-docker-compose.yml` ở chế độ nền. Các dịch vụ bao gồm:
    *   **fastapi:** API phục vụ mô hình.
    *   **prometheus:** Máy chủ thu thập số liệu.
    *   **grafana:** Bảng điều khiển giám sát.
    *   **loki:** Hệ thống tổng hợp log.
    *   **promtail:** Bộ thu thập log cho Loki.
    *   **alertmanager:** Xử lý cảnh báo từ Prometheus.

## Sử dụng

### Các Điểm cuối API

*   **Tài liệu API:** `http://localhost:8000/docs`
*   **Điểm cuối Dự đoán:** `http://localhost:8000/predict/` (yêu cầu POST)

Bạn có thể sử dụng công cụ như `curl` hoặc Postman để gửi yêu cầu POST với tệp hình ảnh đến điểm cuối dự đoán.

### Bảng điều khiển Giám sát

Thiết lập `docker-compose` bao gồm một ngăn xếp giám sát đầy đủ.

1.  **Grafana:**
    *   Truy cập bảng điều khiển Grafana tại `http://localhost:3000`.
    *   Đăng nhập với thông tin mặc định:
        *   **Tên người dùng:** admin
        *   **Mật khẩu:** admin

2.  **Prometheus:**
    *   Truy cập giao diện Prometheus tại `http://localhost:9090`.
    *   Bạn có thể xem các số liệu và cảnh báo đã thu thập.

3.  **Loki:**
    *   Truy cập hệ thống tổng hợp log Loki tại `http://localhost:3100`. Bạn có thể truy vấn log từ dịch vụ `fastapi` tại đây, và nó đã được cấu hình sẵn làm nguồn dữ liệu trong Grafana.

4.  **Alertmanager:**
    *   Truy cập giao diện Alertmanager tại `http://localhost:9093`.

### Chạy script giả lập traffic request 

Để mô phỏng lưu lượng đến API, bạn có thể chạy một script gửi nhiều yêu cầu. Dưới đây là một ví dụ sử dụng thư viện `requests` của Python.

Đầu tiên, cài đặt thư viện cần thiết:
```bash
pip install requests
```

Sau đó, chạy file `traffic_simulation.py`:
```python
cd monitoring
python traffic_simulation.py
```
**Lưu ý:** Hãy chắc chắn thay thế "path/to/your/images" bằng đường dẫn thực tế đến thư mục chứa hình ảnh bạn muốn sử dụng để kiểm tra.

## Dừng các dịch vụ

Để dừng tất cả các dịch vụ đang chạy, sử dụng lệnh sau:
```bash
docker-compose down
```

7. ## Video demo:

[Link Video](https://drive.google.com/file/d/1YCmn9TK6C8lRWEhOqIlUwcSmNjEeWSsF/view)

