import os
import base64
import requests
from dotenv import load_dotenv


# Take environment variables from .env
load_dotenv()

# API endpoint to send request
api_url = os.getenv('API_URL')


# # Local host endpoint to send request
# url = 'http://localhost:8080/2015-03-31/functions/function/invocations'

# Image url
img_url = 'https://m.media-amazon.com/images/I/51c5OmSdwWL._AC_UL320_.jpg'

# Set the headers for the POST request
headers = {'Content-Type': 'application/json'}

# Set the data for the POST
data = {'image_url': img_url}

# Send the POST request as json
response = requests.post(api_url, json=data, headers=headers)

# Parse response in to json
print(response.json())



# Image path
img_path = 'img2.jpg'

# Read image in bytes object
with open(img_path, 'rb') as image:
    image_data = image.read()

# Encode image data as base64
image_data_b64 = base64.b64encode(image_data).decode('utf-8')

# POST request as json object
data = {'image_data': image_data_b64}

# Send the POST request as json
headers = {'Content-Type': 'application/json'}
response = requests.post(api_url, json=data, headers=headers)
print(response.json())