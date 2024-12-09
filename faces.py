# Escriba (o pegue) aquí su solución
import io

import face_recognition
import numpy as np
import requests
from fastapi import FastAPI
from PIL import Image
from skimage.filters import gaussian
from starlette.responses import StreamingResponse

app = FastAPI()


def blur(image_arr, factor=3):
    """Difumina una imagen dada como una array 3D (RGB) NumPy usando factor"""
    try:
        # Según la versión, puede ser necesario el parámetro multichannel=True 
        return gaussian(image_arr, sigma=factor, multichannel=True, preserve_range=True)
    except:
        return gaussian(image_arr, sigma=factor, preserve_range=True)


@app.get("/")
def devuelve_imagen(url: str = None, factor: int = 3):
    try:
        response = requests.get(url)
        image_arr = np.array(Image.open(io.BytesIO(response.content)).convert("RGB"))
    except:
        return {"error": "Image not valid"}
    
    # Doc de face_locations -> Returns an array of bounding boxes of human faces in a image: (top, right, bottom, left)
    face_locations = face_recognition.face_locations(img = image_arr) 
    
    for vertices in face_locations:
        a, b, c, d = vertices[0:]
        image_arr[a:c, d:b] = blur(image_arr[a:c, d:b], factor)
    
    out = Image.fromarray(np.uint8(image_arr))
    bytes_arr = io.BytesIO()
    out.save(bytes_arr, format='PNG')
    bytes_arr.seek(0)
    return StreamingResponse(bytes_arr, media_type="image/png") 
