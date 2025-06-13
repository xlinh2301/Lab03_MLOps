import io
import torch
from fastapi import FastAPI, File, UploadFile, HTTPException
from PIL import Image
import uvicorn 
from contextlib import asynccontextmanager 
from prometheus_fastapi_instrumentator import Instrumentator
import time
from prometheus_client import Counter, Histogram, Gauge, REGISTRY
import os
import psutil
import GPUtil
import logging

from my_model_definition import ImageClassifier, transform_image_for_prediction, device

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

MODEL_PATH = "model.pth" 

# System metrics
cpu_usage = Gauge('system_cpu_usage_percent', 'CPU usage percentage')
gpu_usage = Gauge('system_gpu_usage_percent', 'GPU usage percentage', ['gpu_id'])
gpu_memory = Gauge('system_gpu_memory_usage_bytes', 'GPU memory usage in bytes', ['gpu_id'])
ram_usage = Gauge('system_ram_usage_bytes', 'RAM usage in bytes')
disk_usage = Gauge('system_disk_usage_bytes', 'Disk usage in bytes', ['mount'])
disk_io_read = Counter('system_disk_io_read_bytes', 'Total bytes read from disk')
disk_io_write = Counter('system_disk_io_write_bytes', 'Total bytes written to disk')
network_io_sent = Counter('system_network_io_sent_bytes', 'Total bytes sent over network')
network_io_recv = Counter('system_network_io_recv_bytes', 'Total bytes received over network')

# Metrics
request_count = Counter('model_requests_total', 'Total number of requests')
error_count = Counter('model_errors_total', 'Total number of errors')
inference_time = Histogram('model_inference_time_seconds', 'Time spent processing inference')
confidence_score = Gauge('model_confidence_score', 'Confidence score for each class', ['class_name'])

# Additional metrics for better monitoring
prediction_count = Counter('model_predictions_total', 'Total number of predictions', ['class_name'])
batch_size = Gauge('model_batch_size', 'Current batch size being processed')
model_memory_usage = Gauge('model_memory_usage_bytes', 'Memory usage of the model in bytes')
model_load_time = Gauge('model_load_time_seconds', 'Time taken to load the model')
prediction_latency = Histogram('model_prediction_latency_seconds', 'Latency of predictions', ['class_name'])

# Separate CPU and GPU inference time
cpu_inference_time = Histogram('model_cpu_inference_time_seconds', 'CPU time spent processing inference')
gpu_inference_time = Histogram('model_gpu_inference_time_seconds', 'GPU time spent processing inference')

# Thêm biến toàn cục ở đầu file
last_sent = 0
last_recv = 0

def update_system_metrics():
    global last_sent, last_recv
    # CPU usage
    cpu_usage.set(psutil.cpu_percent())
    
    # RAM usage
    ram_usage.set(psutil.virtual_memory().used)
    
    # Disk usage
    for partition in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_usage.labels(mount=partition.mountpoint).set(usage.used)
        except:
            continue
    
    # Disk IO
    disk_io = psutil.disk_io_counters()
    disk_io_read.inc(disk_io.read_bytes)
    disk_io_write.inc(disk_io.write_bytes)
    
    # Network IO
    net_io = psutil.net_io_counters()
    if last_sent != 0:
        network_io_sent.inc(max(0, net_io.bytes_sent - last_sent))
    if last_recv != 0:
        network_io_recv.inc(max(0, net_io.bytes_recv - last_recv))
    last_sent = net_io.bytes_sent
    last_recv = net_io.bytes_recv
    
    # GPU usage (if available)
    try:
        gpus = GPUtil.getGPUs()
        for gpu in gpus:
            gpu_usage.labels(gpu_id=str(gpu.id)).set(gpu.load * 100)
            gpu_memory.labels(gpu_id=str(gpu.id)).set(gpu.memoryUsed)
    except:
        pass

def load_model():
    logging.info(f"Đang tải mô hình từ: {MODEL_PATH}")
    logging.info(f"Sử dụng device: {device}")
    start_time = time.time()
    try:
        model_instance = ImageClassifier()
        model_instance.load_state_dict(torch.load(MODEL_PATH, map_location=device))
        model_instance.eval()
        model_instance = model_instance.to(device)
        
        # Record model load time
        load_time = time.time() - start_time
        model_load_time.set(load_time)
        
        # Record model memory usage
        if hasattr(model_instance, 'parameters'):
            total_params = sum(p.numel() for p in model_instance.parameters())
            model_memory_usage.set(total_params * 4)  # Assuming 4 bytes per parameter
        
        logging.info("Model đã được tải thành công.")
        return model_instance
    except FileNotFoundError:
        logging.error(f"Lỗi: Không tìm thấy file mô hình tại '{MODEL_PATH}'")
        return None
    except Exception as e:
        logging.error(f"Lỗi khi tải mô hình: {e}")
        return None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load model on startup
    global model
    try:
        model = load_model()
        if model is None:
            print("Không thể tải model. Kiểm tra lại đường dẫn và file model.")
            app.state.model = None
        else:
            print("Model đã được tải thành công.")
            app.state.model = model
    except Exception as e:
        print(f"Lỗi khi tải model: {e}")
        app.state.model = None
    
    # Start system metrics update loop
    import asyncio
    async def update_metrics():
        while True:
            update_system_metrics()
            await asyncio.sleep(1)  # Update every second
    
    # Start metrics update task
    asyncio.create_task(update_metrics())
    
    yield
    
    # Cleanup on shutdown
    if model is not None:
        del model
        print("Model đã được dọn dẹp.")

# Create FastAPI app
app = FastAPI(title="Image Classification API", version="1.0.0", lifespan=lifespan)
Instrumentator().instrument(app).expose(app)  # expose /metrics

@app.get("/", summary="Endpoint gốc", description="Trả về thông điệp chào mừng.")
def read_root():
    if not hasattr(app.state, 'model') or app.state.model is None:
        return {"message": "Chào mừng bạn đến với API! LƯU Ý: Mô hình chưa được tải thành công, kiểm tra logs."}
    return {"message": "Chào mừng bạn đến với API phục vụ mô hình phân loại ảnh!"}

@app.post("/predict/", summary="Dự đoán lớp của ảnh", description="Tải lên một ảnh và nhận về lớp dự đoán cùng xác suất.")
async def predict_image(file: UploadFile = File(..., description="File ảnh cần phân loại.")):
    logging.info(f"Nhận request dự đoán file: {file.filename}")
    request_count.inc()
    if not hasattr(app.state, 'model') or app.state.model is None:
        raise HTTPException(status_code=503, detail="Mô hình chưa sẵn sàng hoặc tải thất bại. Vui lòng kiểm tra logs server.")
    
    current_model = app.state.model 

    try:
        image_bytes = await file.read()
        input_tensor = transform_image_for_prediction(image_bytes)
        input_tensor = input_tensor.to(device)

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"Lỗi xử lý ảnh: {str(ve)}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Lỗi tiền xử lý ảnh: {str(e)}")

    try:
        with torch.no_grad():
            start_time = time.time()
            # Record CPU time
            cpu_start = time.process_time()
            output_logits = current_model(input_tensor) 
            cpu_time = time.process_time() - cpu_start
            cpu_inference_time.observe(cpu_time)
            
            # Record GPU time if available
            if torch.cuda.is_available():
                gpu_start = torch.cuda.Event(enable_timing=True)
                gpu_end = torch.cuda.Event(enable_timing=True)
                gpu_start.record()
                output_logits = current_model(input_tensor)
                gpu_end.record()
                torch.cuda.synchronize()
                gpu_time = gpu_start.elapsed_time(gpu_end) / 1000  # Convert to seconds
                gpu_inference_time.observe(gpu_time)
            
            inference_time.observe(time.time() - start_time)

        probabilities = torch.softmax(output_logits[0], dim=0)
        predicted_score, predicted_idx = torch.max(probabilities, 0)

        # Record confidence score for each class
        for idx, prob in enumerate(probabilities):
            confidence_score.labels(class_name=str(idx)).set(prob.item())

        class_names = {0: "Lớp 0", 1: "Lớp 1"}
        predicted_class_name = class_names.get(predicted_idx.item(), "Không xác định")

        # Update prediction metrics
        prediction_count.labels(class_name=str(predicted_idx.item())).inc()
        prediction_latency.labels(class_name=str(predicted_idx.item())).observe(time.time() - start_time)

        return {
            "filename": file.filename,
            "predicted_class_index": predicted_idx.item(),
            "predicted_class_name": predicted_class_name,
            "confidence_score": predicted_score.item(),
            "all_class_probabilities": probabilities.tolist()
        }
    except Exception as e:
        logging.error(f"Lỗi trong quá trình dự đoán: {e}")
        error_count.inc()
        raise HTTPException(status_code=500, detail=f"Lỗi máy chủ nội bộ trong quá trình dự đoán: {str(e)}")

logging.info("App started")
