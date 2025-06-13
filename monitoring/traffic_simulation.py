import requests
import time
import os
import random

IMAGE_PATH_OR_DIR = "/mnt/c/Users/USER/Downloads/1.jpg"
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