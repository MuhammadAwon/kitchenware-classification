#!/usr/bin/env python
# coding: utf-8

# Required libraries
import tflite_runtime.interpreter as tflite
from img_preprocessor import image_from_url, image_from_path



# List of classes the model was trained to predict
classes = ['cup', 'fork', 'glass', 'knife', 'plate', 'spoon']


# Initalize interpreter
interpreter = tflite.Interpreter(model_path='./kitchenware-model.tflite')
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


# Lambda function to receives an image from url or local path as JSON object
def lambda_handler(event, context):
    image_url = event.get('image_url')
    image_data_b64 = event.get('image_data')

    if image_url:
        preds = predict(image_url)
    elif image_data_b64:
        preds = predict(image_data_b64)
    else:
        raise ValueError('No image path or URL provided')

    # Extract the class name with highest probability
    pred_class = max(preds, key=preds.get)
    return pred_class

