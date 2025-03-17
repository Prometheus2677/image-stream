from fastapi import WebSocket
from typing import List

connected_clients: List[WebSocket] = []

async def forward_image(image_data: bytes):
    """Send the received image to all WebSocket clients."""
    for client in connected_clients:
        try:
            await client.send_bytes(image_data)  # Send as binary
        except:
            connected_clients.remove(client)
