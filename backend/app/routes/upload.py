from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException
from app.services.forwarder import forward_image
from app.services.uploader import ImageUploader
import os
from typing import List
from dotenv import load_dotenv
from pydantic import BaseModel
import base64

router = APIRouter()
load_dotenv(override=True)

# Aerospike configuration
AEROSPIKE_CONFIG = {
    'hosts': [(os.getenv("AEROSPIKE_HOST"), int(os.getenv("AEROSPIKE_PORT")))]
}
NAMESPACE = os.getenv("NAMESPACE")
SET_NAME = os.getenv("SET_NAME")
IMAGE_DIRECTORY = os.getenv("IMAGE_DIRECTORY")

# Initialize the uploader
uploader = ImageUploader(AEROSPIKE_CONFIG, NAMESPACE, SET_NAME, image_folder=IMAGE_DIRECTORY)

class ImageData(BaseModel):
    name: str
    value: str

class ImageDataUpload(BaseModel):
    msg: str
    bins: List[ImageData]


@router.get("/upload")
async def upload_image():
    return {"message": "Status is okay!"}

@router.post("/upload")
async def upload_image(data: List[ImageDataUpload]):
    try:
        for chunk in data:
            if chunk.msg == "delete":
                continue

            chunk_info = {bin_entry.name: bin_entry.value for bin_entry in chunk.bins}

            required_keys = ['image_data']
            missing_keys = [key for key in required_keys if key not in chunk_info]
            if missing_keys:
                raise HTTPException(status_code=400, detail=f"Missing keys: {missing_keys}")
            image_data = chunk_info['image_data']
            image_data = base64.b64decode(image_data)
            # ✅ Forward image data to WebSocket clients
            await forward_image(image_data)
        return {"message": "Image forwarded"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload-test")
async def upload_image(file: UploadFile = File(...)):
    """Receive an image and forward it to WebSocket clients."""
    image_data = await file.read()  # Read binary image data
    await forward_image(image_data)  # Immediately send to WebSockets
    return {"message": "Image forwarded"}

@router.post("/start-stream")
async def start_upload(background_tasks: BackgroundTasks):
    """Starts uploading images asynchronously from the configured folder."""
    uploader.connect()
    background_tasks.add_task(uploader.process_image_directory)
    return {"message": "Upload started"}

@router.post("/stop-stream")
async def stop_upload():
    """Stops the image upload process."""
    uploader.stop_uploading()
    return {"message": "Upload stopping..."}