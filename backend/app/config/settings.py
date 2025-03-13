import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    IMAGE_FOLDER = os.getenv("IMAGE_FOLDER", "images")
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))

settings = Settings()
