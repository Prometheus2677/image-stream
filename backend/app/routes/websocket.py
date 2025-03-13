from fastapi import APIRouter, WebSocket
from app.services.streamer import send_images

router = APIRouter()

@router.websocket("/stream")
async def websocket_endpoint(websocket: WebSocket):
    await send_images(websocket)
