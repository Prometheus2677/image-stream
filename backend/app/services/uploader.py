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
        self.image_folder = image_folder  # Folder where images are stored
        self.stop_upload = False  # Flag to control upload process

    def connect(self):
        """Connect to Aerospike server."""
        try:
            self.client = aerospike.client(self.aerospike_config).connect()
            logging.info("✅ Successfully connected to Aerospike.")
        except ex.AerospikeError as e:
            logging.error("❌ Failed to connect to Aerospike: %s", e)
            raise

    def close(self):
        """Close connection to Aerospike."""
        if self.client:
            self.client.close()
            logging.info("✅ Closed connection to Aerospike.")

    def store_image(self, image_path):
        """Reads an image file and stores it in Aerospike as a single record."""
        if self.stop_upload:
            logging.info("⏹️ Upload process stopped. Skipping %s", image_path)
            return
        
        image_id = str(uuid.uuid4())  # Generate a unique image ID
        logging.info("📤 Processing image '%s' with ID: %s", image_path, image_id)

        try:
            with open(image_path, "rb") as file:
                img_data = file.read()

            key = (self.namespace, self.set_name, image_id)
            record = {
                "image_data": img_data,
            }

            try:
                self.client.put(key, record)
                logging.info("✅ Successfully stored image %s in Aerospike.", os.path.basename(image_path))
            except ex.AerospikeError as e:
                logging.error("❌ Failed to store image in Aerospike: %s", e)
        except Exception as e:
            logging.error("❌ Error processing image '%s': %s", image_path, e)

    def process_image_directory(self):
        """Reads images from the 'images' folder and uploads them to Aerospike at 24 FPS."""
        self.stop_upload = False  # Reset stop flag

        image_files = sorted(
            [f for f in os.listdir(self.image_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]
        )

        if not image_files:
            logging.warning("⚠️ No images found in '%s' directory.", self.image_folder)
            return

        logging.info("🚀 Starting image upload. Total images: %d", len(image_files))

        for filename in image_files:
            if self.stop_upload:
                logging.warning("⏹️ Upload process stopped before processing all files.")
                break

            file_path = os.path.join(self.image_folder, filename)

            if os.path.isfile(file_path):
                logging.info("📂 Uploading image file: %s", filename)
                self.store_image(file_path)

                # ⏳ Maintain 24 FPS (1/24s = ~41.67ms delay)
                time.sleep(1 / 24)
            else:
                logging.debug("🔍 Skipping non-image file: %s", filename)

    def stop_uploading(self):
        """Stops the upload process."""
        logging.warning("⏹️ Stopping upload process...")
        self.stop_upload = True
