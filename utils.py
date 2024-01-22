import requests
from PIL import Image
from io import BytesIO
import base64

def resize_image(image_url, target_size):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    img_resized = img.resize(target_size, Image.LANCZOS) 
    resized_bytes_io = BytesIO()
    img_resized.save(resized_bytes_io, format='JPEG')
    resized_image = base64.b64encode(resized_bytes_io.getvalue()).decode('utf-8')
    return f"data:image/jpeg;base64,{resized_image}"