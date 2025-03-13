from fastapi import WebSocket
import asyncio
import os
from app.config.settings import settings

# Load and sort images
image_files = sorted(
    [f for f in os.listdir(settings.IMAGE_FOLDER) if f.endswith(('.jpg', '.png', '.jpeg'))]
)

async def send_images(websocket: WebSocket):
    """Stream images at 24 FPS as binary data (Blob)."""
    await websocket.accept()

    while True:
        for img_file in image_files:
            img_path = os.path.join(settings.IMAGE_FOLDER, img_file)

            # Read the image as binary
            with open(img_path, "rb") as file:
                img_data = file.read()

            await websocket.send_bytes(img_data)  # Send raw binary
            await asyncio.sleep(1 / 24)  # Maintain 24 FPS
