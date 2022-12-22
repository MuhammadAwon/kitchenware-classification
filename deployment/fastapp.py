#!/usr/bin/env python
# coding: utf-8


# Required libraries
import os
import uvicorn
import numpy as np
import tflite_runtime.interpreter as tflite

from io import BytesIO
from urllib.request import urlopen
from urllib.error import HTTPError
from PIL import Image
from PIL.Image import Resampling
from fastapi import FastAPI
from pydantic import BaseModel



# Initialize model
MODEL_NAME = os.getenv('MODEL_NAME', './kitchenware-model.tflite')

# List of classes the model was trained to predict
classes = ['cup', 'fork', 'glass', 'knife', 'plate', 'spoon']


# Preprecess image
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
def image_from_path(path, target_size=(256, 256)):
    with Image.open(path) as img:
        return preprocess_image(img, target_size)


# Initalize interpreter
interpreter = tflite.Interpreter(model_path=MODEL_NAME)
# Allocate memory
interpreter.allocate_tensors()
# Get input index
input_index = interpreter.get_input_details()[0]['index']
# Get output index
output_index = interpreter.get_output_details()[0]['index']


# Function to make predictions on image
def predict(img):
    # Preprocess the image from url (https/http)
    if img.startswith('https') or img.startswith('http'):
        X = image_from_url(img)
    # Preprocess the image from path
    else:
        X = image_from_path(img)

    # Get image predictions from tensors
    interpreter.set_tensor(input_index, X)
    interpreter.invoke()
    preds = interpreter.get_tensor(output_index)[0]

    # Convert numpy array predictions into float type
    # for conversion we simply need to convert array to python list first
    float_preds = preds.tolist()    
    return dict(zip(classes, float_preds))


# Create fastapi app
app = FastAPI()


# Check data validity
class Data(BaseModel):
    url: str

# API endpoint for making prediction against the request received from client
@app.post('/predict')
async def request_handler(data: Data):
    # Convert JSON request data in to python dict
    data_dict = data.dict()
    # Extrant image url from data_dict
    img_url = data_dict['url']
    # Make predictions on image
    preds = predict(img_url)
    # Extract class name with highest probability in preds
    pred_class = max(preds, key=preds.get)
    # Return response back to the client
    return pred_class



if __name__=='__main__':
    uvicorn.run('fastapp:app', host='localhost', port=9696, reload=True)