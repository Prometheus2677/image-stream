import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    IMAGE_FOLDER = os.getenv("IMAGE_FOLDER", "images")
    FASTAPI_HOST = os.getenv("HOST", "0.0.0.0")
    FASTAPI_PORT = int(os.getenv("PORT", 8000))

    AEROSPIKE_HOST = os.getenv("AEROSPIKE_HOST", 8000)
    AEROSPIKE_PORT = int(os.getenv("AEROSPIKE_PORT", 8000))
    NAMESPACE = os.getenv("NAMESPACE", 8000)
    SET_NAME = os.getenv("SET_NAME", 8000)

settings = Settings()
