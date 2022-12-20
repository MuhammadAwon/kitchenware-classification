import os
import requests
from dotenv import load_dotenv

load_dotenv()

# # Local host url (with docker image for aws lambda)
# url = 'http://localhost:8080/2015-03-31/functions/function/invocations'

# # API url
# api_url = os.getenv('API_URL')


# Image data to send with POST request
data = {'url': 'https://target.scene7.com/is/image/Target/GUEST_10f0fb6f-05d7-4a1d-9cae-2fa12a691741?wid=800&hei=800&qlt=80&fmt=pjpeg'}

# Parse POST request of the data to JSON
result = requests.post(api_url, json=data).json()
print(result)

