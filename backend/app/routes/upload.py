from fastapi import APIRouter, UploadFile, File
from app.services.forwarder import forward_image

router = APIRouter()

@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    """Receive an image and forward it to WebSocket clients."""
    image_data = await file.read()  # Read binary image data
    await forward_image(image_data)  # Immediately send to WebSockets
    return {"message": "Image forwarded"}
