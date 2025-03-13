import aerospike
import uuid
import logging
import os
import time
from aerospike import exception as ex

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ImageUploader:
    def __init__(self, aerospike_config, namespace, set_name, image_folder="images"):
        self.namespace = namespace
        self.set_name = set_name
        self.client = None
        self.aerospike_config = aerospike_config
        self.image_folder = image_folder
        self.stop_upload = False

    def connect(self):
        """Connect to Aerospike server."""
        try:
            self.client = aerospike.client(self.aerospike_config).connect()
            logging.info("Connected to Aerospike.")
        except ex.AerospikeError as e:
            logging.error("Failed to connect to Aerospike: %s", e)
            raise

    def close(self):
        """Close connection to Aerospike."""
        if self.client:
            self.client.close()
            logging.info("Connection to Aerospike closed.")

    def store_image(self, image_path):
        """Reads an image file and stores it in Aerospike."""
        if self.stop_upload:
            return

        image_id = str(uuid.uuid4())
        try:
            with open(image_path, "rb") as file:
                img_data = file.read()

            key = (self.namespace, self.set_name, image_id)
            self.client.put(key, {"image_data": img_data})
        except ex.AerospikeError as e:
            logging.error("Error storing image %s: %s", image_path, e)
        except Exception as e:
            logging.error("Error processing image %s: %s", image_path, e)

    def process_image_directory(self):
        """Reads images from the directory and uploads them to Aerospike at 24 FPS."""
        self.stop_upload = False
        image_files = sorted(
            [f for f in os.listdir(self.image_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]
        )

        if not image_files:
            logging.warning("No images found in %s", self.image_folder)
            return

        logging.info("Uploading %d images...", len(image_files))
        for filename in image_files:
            if self.stop_upload:
                break
            self.store_image(os.path.join(self.image_folder, filename))
            time.sleep(1 / 24)

    def stop_uploading(self):
        """Stops the upload process."""
        self.stop_upload = True
