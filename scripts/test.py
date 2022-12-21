import requests


# Local host url (with docker image)
url = 'http://localhost:9696/predict'

# Image data to send with POST request
data = {'url': 'https://m.media-amazon.com/images/I/61b0ng0Gg5L._AC_UL320_.jpg'}


# Parse POST request of the data to JSON
result = requests.post(url, json=data).json()
print(result)
