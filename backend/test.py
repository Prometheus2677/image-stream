import requests
import time
import os

UPLOAD_URL = "http://0.0.0.0:8000/upload-test"
IMAGE_FOLDER = "images"

image_files = sorted(
    [f for f in os.listdir(IMAGE_FOLDER) if f.endswith(('.jpg', '.png', '.jpeg'))]
)

def send_images():
    """Sends images as binary data to the relay server."""
    for img_file in image_files:
        img_path = os.path.join(IMAGE_FOLDER, img_file)

        with open(img_path, "rb") as file:
            img_data = file.read()

        response = requests.post(UPLOAD_URL, files={"file": img_data})

        if response.status_code == 200:
            print(f"✅ Sent {img_file}")
        else:
            print(f"❌ Failed to send {img_file}")

        time.sleep(1 / 24)  # Maintain 24 FPS

if __name__ == "__main__":
    send_images()
