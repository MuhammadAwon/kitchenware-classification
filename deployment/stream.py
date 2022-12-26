import os
import requests
import base64
import numpy as np
import streamlit as st

from PIL import Image
from PIL.Image import Resampling
from io import StringIO 
from dotenv import load_dotenv
from requests.exceptions import MissingSchema



# Load environment variable
load_dotenv()
# API url
api_endpoint = os.getenv('API_URL')


# Title and subtitles
st.markdown('<h1 style="color:black;">Kitchenware Image Classification</h1>', unsafe_allow_html=True)
st.markdown('<h2 style="color:gray;">The image classification model classifies image into following categories:</h2>', unsafe_allow_html=True)
st.markdown('<h3 style="color:gray;"> cup, fork, glass, knife, plate, spoon</h3>', unsafe_allow_html=True)
# Hide the first pre-selected radio button
st.markdown('<style>div[role="radiogroup"]>:first-child{display: none !important;}</style>', unsafe_allow_html=True)


# # Function to return predicted class of image from local machine
# def request_path_pred(img_path, url=api_endpoint):
#     # Check for image path
#     if img_path.type == 'image/jpeg' or img_path.type == 'image/png':
#         # Convert streamlit UploadedFile object into python string
#         img_str = img_path.name
#         if img_str.endswith('.jpg') or img_str.endswith('.png'):
#             with open(img_str, 'rb') as f:
#                 image_data = f.read()
#             image_data = base64.b64encode(image_data).decode('utf-8')
#             headers = {'Content-Type': 'application/json'}
#             data = {'image_data': image_data}
#             # Send POST request
#             response = requests.post(url, json=data, headers=headers)

#     # Parse response into JSON
#     return response.json()





# Function to return predicted class from image url
def request_url_pred(img_url, url=api_endpoint):
    # Check for image url
    if img_url.startswith('https') or img_url.startswith('http'):
        headers = {'Content-Type': 'application/json'}
        data = {'image_url': img_url}       
        # Send POST request
        response = requests.post(url, json=data, headers=headers)
    
    # Parse response into JSON
    return response.json()


# Function to get image from path or from input url
def get_image(upload_image_clicked, image_url_clicked, upload_image, image_url):
    if upload_image_clicked:
        # Set the session state of the upload_image button to True
        # and the image_url button to False
        st.session_state['upload_image_clicked'] = True
        st.session_state['image_url_clicked'] = False
        # Return the image from the upload_image button
        return upload_image
    elif image_url_clicked:
        # Set the session state of the image_url button to True
        # and the upload_image button to False
        st.session_state['image_url_clicked'] = True
        st.session_state['upload_image_clicked'] = False
        # Return the image from the image_url button
        return image_url
    else:
        # If neither button was clicked, return None
        return None


# Function to check image source
def check_image_source(image, upload_image_clicked, image_url_clicked):
    if image is not None:
        if upload_image_clicked:
            return 'Upload image'
        elif image_url_clicked:
            return 'Input image'
    else:
        return 'No image'
# ###################################################################
# ## EXPERIMENTING
# # Radio button function to selection image url or ask user for custom url for prediction
# def radio_button_function():
#     # Create a radio button for each option (empty string to hide first radio button)
#     selected_option = st.radio('Choose an option for prediction:',
#                               ('', 'Knife', 'Fork', 'Spoon', 'Cup', 'Glass', 'Plate'),
#                               index=0, key='radio_button')

#     # Set the default URL for each option
#     url_map = {
#         '': None,
#         'Knife': 'https://m.media-amazon.com/images/I/71FtjejRbvL._AC_UL320_.jpg',
#         'Fork': 'https://m.media-amazon.com/images/I/51j88-h2NZL.jpg',
#         'Spoon': 'https://m.media-amazon.com/images/I/51Dvu6GiM8L._AC_UL320_.jpg',
#         'Cup': 'https://m.media-amazon.com/images/I/61Bq3L4gbSL._AC_UL320_.jpg',
#         'Glass': 'https://m.media-amazon.com/images/I/81B88+ZiRIL._AC_UL320_.jpg',
#         'Plate': 'https://m.media-amazon.com/images/I/A14F1QVaPNL._AC_UL320_.jpg'
#     }

#     # Default URL for the selected option
#     url = url_map[selected_option]

#     # Add a reset button to return the radio button to its initial state
#     if st.button('Reset'):
#         selected_option = None

#     # Display the selected option
#     if selected_option:
#         st.write(f'You selected the option: {selected_option}')

#     return url


# # Call the radio funciton
# image = radio_button_function()



# #####################################














# Create an 'upload_image' to add an image from the local computer 
# and 'upload_image_button' to indicate when the image is uploaded
upload_image = st.file_uploader('Upload an image', type=['png', 'jpg'])
upload_image_button = st.button('Upload image')

# Create an 'image_url' to get image url from the user
# and 'image_url_button' to indicate when the url is provided
image_url = st.text_input('Enter an image URL')
image_url_button = st.button('Enter url')

# Set the default values of the button clicked flags to False 
st.session_state['upload_image_clicked'] = False
st.session_state['image_url_clicked'] = False

if upload_image_button:
    # Set the upload_image_clicked flag to True
    upload_image_clicked = True
else:
    upload_image_clicked = False

if image_url_button:
    # Set the image_url_clicked flag to True
    image_url_clicked = True
else:
    image_url_clicked = False



# Get the image from the clicked button
image = get_image(upload_image_clicked, image_url_clicked, upload_image, image_url)

# Check the source of the image
image_source = check_image_source(image, upload_image_clicked, image_url_clicked)


###############

# # Function to return predicted class of image from local machine
# def request_path_pred(img_path, url=api_endpoint):
#     # Check for image path
#     if img_path.type == 'image/jpeg' or img_path.type == 'image/png':
#         # Convert streamlit UploadedFile object into python string
#         img_str = img_path.name
#         if img_str.endswith('.jpg') or img_str.endswith('.png'):
#             with open(img_str, 'rb') as f:
#                 image_data = f.read()
#             image_data = base64.b64encode(image_data).decode('utf-8')
#             headers = {'Content-Type': 'application/json'}
#             data = {'image_data': image_data}
#             # Send POST request
#             response = requests.post(url, json=data, headers=headers)

#     # Parse response into JSON
#     return response.json()

def request_path_pred(img_path, url=api_endpoint):
    img = img_path.name
    with open(img, 'rb') as image:
        image_data = image.read()
    image_data_b64 = base64.b64encode(image_data).decode('utf-8')
    data = {'image_data': image_data_b64}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, json=data, headers=headers)
    return response.json()


# st.write(image_source)
# st.write(request_path_pred(image))

# st.write(image.name)

##############


# Function to display image and its predicted class
def main():
    # Create two columns to display
    c1, c2 = st.columns(2)
    if image is not None:
        if image_source == 'Upload image':
            img = Image.open(image)
            img = img.resize((300, 350))
            c1.header('Input Image')
            c1.image(img)
            pred = request_path_pred(image)
        else:
            response = requests.get(image, stream=True).raw
            img = Image.open(response)
            img = img.resize((300, 350))
            c1.header('Input Image')
            c1.image(img)
            pred = request_url_pred(image)

        # Display prediction on second column
        c2.header('Output')
        c2.write(pred)

if __name__=='__main__':
    main()










