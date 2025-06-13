<!-- Banner -->
<p align="center">
  <a href="https://www.uit.edu.vn/" title="Trường Đại học Công nghệ Thông tin" style="border: none;">
    <img src="https://i.imgur.com/WmMnSRt.png" alt="Trường Đại học Công nghệ Thông tin | University of Information Technology">
  </a>
</p>

<h1 align="center"><b>Information Retrieval</b></h1>

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

# COURSE INTRODUCTION
* **Course Name:** MLOps - Phát triển và vận hành hệ thống máy học.
* **Class Code:** CS317.P21.
* **Academic Year:** HK2 (2024 - 2025).
* **Lecturer**: Th.S Đỗ Văn Tiến, Lê Trần Trọng Khiêm

# Lab 2: Model Serving and Monitoring

This project sets up a machine learning model serving API with monitoring using Prometheus and Grafana.

## Project Structure

```
cs317-lab2/
├── docker-compose.yml
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

## Setup

### Prerequisites

*   Docker
*   Docker Compose

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd cs317-lab2
    ```

2.  **Build and run the services:**
    ```bash
    docker-compose up -d --build
    ```
    This command will build the Docker image for the FastAPI service and start all the services defined in `docker-compose.yml` in detached mode. The services include:
    *   **fastapi:** The model serving API.
    *   **prometheus:** The metrics collection server.
    *   **grafana:** The monitoring dashboard.
    *   **loki:** The log aggregation system.
    *   **promtail:** The log collector for Loki.
    *   **alertmanager:** Handles alerts from Prometheus.

## Usage

### API Endpoints

*   **API Documentation:** `http://localhost:8000/docs`
*   **Prediction Endpoint:** `http://localhost:8000/predict/` (POST request)

You can use a tool like `curl` or Postman to send a POST request with an image file to the prediction endpoint.

### Monitoring Dashboard

The `docker-compose` setup includes a full monitoring stack.

1.  **Grafana:**
    *   Access the Grafana dashboard at `http://localhost:3000`.
    *   Login with the default credentials:
        *   **Username:** admin
        *   **Password:** admin

2.  **Prometheus:**
    *   Access the Prometheus UI at `http://localhost:9090`.
    *   You can view the collected metrics and alerts.

3.  **Loki:**
    *   Access the Loki log aggregation system at `http://localhost:3100`. You can query logs from the `fastapi` service here, and it is pre-configured as a data source in Grafana.

4.  **Alertmanager:**
    *   Access the Alertmanager UI at `http://localhost:9093`.

### Traffic Simulation

To simulate traffic to the API, you can run a script that sends multiple requests. Here is an example using Python's `requests` library.

First, install the required library:
```bash
pip install requests
```

Then, create a Python script `traffic_simulation.py` with the following content:
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
                print(f"Successfully predicted {os.path.basename(image_path)}: {response.json()}")
            else:
                print(f"Error predicting {os.path.basename(image_path)}: {response.status_code} {response.text}")
    except Exception as e:
        print(f"An error occurred with {os.path.basename(image_path)}: {e}")

if __name__ == "__main__":
    image_files = []
    if os.path.isdir(IMAGE_PATH_OR_DIR):
        print(f"Searching for images in directory: {IMAGE_PATH_OR_DIR}")
        image_files = [os.path.join(IMAGE_PATH_OR_DIR, f) for f in os.listdir(IMAGE_PATH_OR_DIR) if f.lower().endswith(('png', 'jpg', 'jpeg'))]
        if not image_files:
            print(f"No images found in '{IMAGE_PATH_OR_DIR}'.")
    elif os.path.isfile(IMAGE_PATH_OR_DIR):
        print(f"Using single image: {IMAGE_PATH_OR_DIR}")
        image_files = [IMAGE_PATH_OR_DIR]
    else:
        print(f"Path '{IMAGE_PATH_OR_DIR}' is not a valid file or directory.")

    if image_files:
        print(f"Found {len(image_files)} image(s) to send.")
        while True:
            image_path = random.choice(image_files)
            send_request(image_path)
            time.sleep(random.uniform(0.5, 2.0))
    else:
        print("No images to process. Exiting.") 
```
**Note:** Make sure to replace `"path/to/your/images"` with the actual path to a directory containing images you want to use for testing.

Run the script:
```bash
python traffic_simulation.py
```

## Stopping the services

To stop all running services, use the following command:
```bash
docker-compose down
```

7. ## Video demo:

[Link Video](https://drive.google.com/file/d/1DJ9JjSqxwKapUK1miyIhpDYmi2py5kIC/view)

## Download and Install Prometheus and Promtool

Since the `prometheus` and `promtool` binaries are large, they are not included in the repository. You can download them separately using the following steps:

1. **Download Prometheus:**
   - Visit the [Prometheus download page](https://prometheus.io/download/).
   - Download the appropriate version for your operating system.
   - Extract the downloaded archive and copy the `prometheus` binary to `monitoring/prometheus-3.4.1.linux-amd64/`.

2. **Download Promtool:**
   - The `promtool` binary is included in the same archive as Prometheus.
   - Copy the `promtool` binary to `monitoring/prometheus-3.4.1.linux-amd64/`.

Ensure both binaries are executable and located in the correct directory before starting the services.
