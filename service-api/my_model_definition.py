import io
import torch
from torch import nn
from torchvision import transforms
from PIL import Image
import numpy as np
from scipy.ndimage import gaussian_filter

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class ImageClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        
        self.conv_layers = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),

            # Second Conv Block
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),

            # Third Conv Block
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
        )
        self.fc_layers = nn.Sequential(
            nn.Flatten(),
            nn.Linear(128 * 28 * 28, 512), 
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(512, 2), 
            nn.Sigmoid() 
        )

    def forward(self, x):
        x = self.conv_layers(x)
        x = self.fc_layers(x)
        return x

def transform_image_for_prediction(image_bytes: bytes) -> torch.Tensor:
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    except Exception as e:
        raise ValueError(f"Không thể mở ảnh từ bytes: {e}")

    image_np = np.array(image)
    
    image_np_filtered = gaussian_filter(image_np, sigma=1, mode='reflect', truncate=4.0) 
    
    if image_np_filtered.dtype != np.uint8:
        image_np_filtered = image_np_filtered.astype(np.uint8)
    image_pil_filtered = Image.fromarray(image_np_filtered)

    transform_pipeline = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(), 
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]), 
    ])
    
    tensor_image = transform_pipeline(image_pil_filtered)
    return tensor_image.unsqueeze(0)