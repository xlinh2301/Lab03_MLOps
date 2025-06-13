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

Sau đó, tạo một script Python `traffic_simulation.py` với nội dung sau:
```python
import requests
import time
import os
import random

IMAGE_PATH_OR_DIR = "path/to/your/images"
API_URL = "http://localhost:8000/predict/"

def send_request(image_path):
    try:
        with open(image_path, "rb") as f:
            files = {"file": (os.path.basename(image_path), f, "image/jpeg")}
            response = requests.post(API_URL, files=files)
            if response.status_code == 200:
                print(f"Dự đoán thành công {os.path.basename(image_path)}: {response.json()}")
            else:
                print(f"Lỗi khi dự đoán {os.path.basename(image_path)}: {response.status_code} {response.text}")
    except Exception as e:
        print(f"Đã xảy ra lỗi với {os.path.basename(image_path)}: {e}")

if __name__ == "__main__":
    image_files = []
    if os.path.isdir(IMAGE_PATH_OR_DIR):
        print(f"Tìm kiếm hình ảnh trong thư mục: {IMAGE_PATH_OR_DIR}")
        image_files = [os.path.join(IMAGE_PATH_OR_DIR, f) for f in os.listdir(IMAGE_PATH_OR_DIR) if f.lower().endswith(('png', 'jpg', 'jpeg'))]
        if not image_files:
            print(f"Không tìm thấy hình ảnh trong '{IMAGE_PATH_OR_DIR}'.")
    elif os.path.isfile(IMAGE_PATH_OR_DIR):
        print(f"Sử dụng hình ảnh đơn: {IMAGE_PATH_OR_DIR}")
        image_files = [IMAGE_PATH_OR_DIR]
    else:
        print(f"Đường dẫn '{IMAGE_PATH_OR_DIR}' không phải là tệp hoặc thư mục hợp lệ.")

    if image_files:
        print(f"Tìm thấy {len(image_files)} hình ảnh để gửi.")
        while True:
            image_path = random.choice(image_files)
            send_request(image_path)
            time.sleep(random.uniform(0.5, 2.0))
    else:
        print("Không có hình ảnh để xử lý. Thoát.") 
```
**Lưu ý:** Hãy chắc chắn thay thế "path/to/your/images" bằng đường dẫn thực tế đến thư mục chứa hình ảnh bạn muốn sử dụng để kiểm tra.

Chạy script:
```bash
python traffic_simulation.py
```

## Dừng các dịch vụ

Để dừng tất cả các dịch vụ đang chạy, sử dụng lệnh sau:
```bash
docker-compose down
```

7. ## Video demo:

[Link Video](https://drive.google.com/file/d/1DJ9JjSqxwKapUK1miyIhpDYmi2py5kIC/view)

