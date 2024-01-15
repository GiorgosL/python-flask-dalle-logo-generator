import requests
from PIL import Image
from io import BytesIO
import base64
import logging
from logging.handlers import RotatingFileHandler

def resize_image(image_url, target_size):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    img_resized = img.resize(target_size, Image.LANCZOS) 
    resized_bytes_io = BytesIO()
    img_resized.save(resized_bytes_io, format='JPEG')
    resized_image = base64.b64encode(resized_bytes_io.getvalue()).decode('utf-8')
    return f"data:image/jpeg;base64,{resized_image}"


def setup_logging(app, log_file):
    log_level = logging.DEBUG if app.debug else logging.INFO
    app.logger.setLevel(log_level)

    handler = RotatingFileHandler(log_file, maxBytes=10240, backupCount=10)

    formatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s')
    handler.setFormatter(formatter)

    app.logger.addHandler(handler)