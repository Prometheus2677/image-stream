from fastapi import FastAPI, WebSocket
import asyncio
import os
import base64
import cv2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Load settings from .env
IMAGE_FOLDER = os.getenv("IMAGE_FOLDER", "images")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))

# Load and sort image files
image_files = sorted([f for f in os.listdir(IMAGE_FOLDER) if f.endswith(('.jpg', '.png', '.jpeg'))])

async def send_images(websocket: WebSocket):
    """Stream images from folder at 24 FPS."""
    await websocket.accept()
    while True:
        for img_file in image_files:
            img_path = os.path.join(IMAGE_FOLDER, img_file)

            # Read and encode image
            img = cv2.imread(img_path)
            _, buffer = cv2.imencode('.jpg', img)
            encoded_string = base64.b64encode(buffer).decode('utf-8')

            await websocket.send_text(encoded_string)
            await asyncio.sleep(1/100)  # Maintain 24 FPS

@app.websocket("/stream")
async def websocket_endpoint(websocket: WebSocket):
    await send_images(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
