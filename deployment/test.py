import os
import requests

from dotenv import load_dotenv


load_dotenv()
api_endpoint = os.getenv('API_URL')


# # Local host endpoint
# host_url = 'http://localhost:8080/predict'

# Image url
data = {'url': 'https://m.media-amazon.com/images/I/61ACGi91bHL._AC_UL320_.jpg'} # spoon image

# Send POST request with data as json
response = requests.post(api_endpoint, json=data)
# Parse response from server in json
res = response.json()
print(res)