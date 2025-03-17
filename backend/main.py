from fastapi import FastAPI
from app.routes.websocket import router as websocket_router
from app.routes.upload import router as upload_router
import uvicorn

app = FastAPI()

# Include routes
app.include_router(websocket_router)
app.include_router(upload_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
