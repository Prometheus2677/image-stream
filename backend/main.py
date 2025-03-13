from fastapi import FastAPI
from app.routes.websocket import router
from app.config.settings import settings
import uvicorn

app = FastAPI()

# Include WebSocket route
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
