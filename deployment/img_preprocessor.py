# Required libraries
import base64
import numpy as np

from io import BytesIO
from urllib.request import urlopen
from urllib.error import HTTPError
from PIL import Image
from PIL.Image import Resampling



# Preprecess colored image
def preprocess_image(img, target_size):
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img = img.resize(target_size, resample=Resampling.NEAREST)
    x = np.array(img, dtype='float32')
    X = np.expand_dims(x, axis=0)
    return X

# Function to download image from url before preprocessing
def image_from_url(url, target_size=(256, 256)):
    try:
        with urlopen(url) as resp:
            buffer = resp.read()
        stream = BytesIO(buffer)
        img = Image.open(stream)
        return preprocess_image(img, target_size)
    except HTTPError as err:
        print(f'{err}. Please try another URL!')

# Function to read image from path before preprocessing
def image_from_path(path_b64, target_size=(256, 256)):
    # Decode the base64 image data back into a bytes object
    image_data = BytesIO(base64.b64decode(path_b64))
    img = Image.open(image_data)
    return preprocess_image(img, target_size)

