import requests


# Local host endpoint
host_url = 'http://localhost:9696/predict'

# Image url
data = {'url': 'https://m.media-amazon.com/images/I/61ACGi91bHL._AC_UL320_.jpg'} # spoon image

# Send POST request with data as json
response = requests.post(host_url, json=data)
# Parse response from server in json
res = response.json()
print(res)