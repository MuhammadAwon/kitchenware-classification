import os
import io
import requests
import base64
import numpy as np
import streamlit as st

from PIL import Image
from PIL.Image import Resampling
from dotenv import load_dotenv
from deta import Deta
from requests.exceptions import MissingSchema



# Load environment variables
load_dotenv()

# Initialize project (Deta)
project_key = os.getenv('PROJECT_KEY')
project = Deta(project_key)

# Define Deta drive to store image
drive_name = 'images'
drive = project.Drive(drive_name)

# Lambda API Gateway
api_endpoint = os.getenv('API_URL')


# Title and subtitles
st.markdown('<h1 style="color:black;">Kitchenware Image Classification</h1>', unsafe_allow_html=True)
st.markdown('<h2 style="color:gray;">The image classification model classifies image into following categories:</h2>', unsafe_allow_html=True)
st.markdown('<h3 style="color:gray;"> cup, fork, glass, knife, plate, spoon</h3>', unsafe_allow_html=True)
# Hide the first pre-selected radio button
st.markdown('<style>div[role="radiogroup"]>:first-child{display: none !important;}</style>', unsafe_allow_html=True)


# Function to return predicted class of image from local machine
def request_path_pred(img_path, url=api_endpoint):
    # Encode the image data
    image_data = base64.b64encode(img_path).decode('utf-8')
    # Headers and data information for POST request
    headers = {'Content-Type': 'application/json'}
    data = {'image_data': image_data}
    # Send POST request
    response = requests.post(url, json=data, headers=headers)

    # Parse response into JSON
    return response.json()


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


# Function to get image from path or from user input url
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


# Function to check image source (path or url)
def check_image_source(image, upload_image_clicked, image_url_clicked):
    if image is not None:
        if upload_image_clicked:
            return 'Upload image'
        elif image_url_clicked:
            return 'Input image'
    else:
        return 'No image'


# Function to save and load image from Deta drive
def upload_and_retrieve_image(image):
    # Upload image
    if image is not None:
        # Get the bytes value of the image
        bytes_data = image.getvalue()        
        # Upload image to the Deta Drive
        drive.put(image.name, data=bytes_data)
    
    # Download image
    if image is not None:
        # Retrieve image from the Deta Drive
        download_image = drive.get(image.name)
        # Read the image data from download_image
        image_data = download_image.read()

        return image_data


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


# Create a button 'upload_image' to add an image from the local computer 
# and 'upload_image_button' to indicate when the image is uploaded
upload_image = st.file_uploader('Upload an image', type=['png', 'jpg', 'jpeg'])
upload_image_button = st.button('Upload image')

# Create a button 'image_url' to get image url from the user
# and 'image_url_button' to indicate when the url is provided
image_url = st.text_input('Enter an image URL')
image_url_button = st.button('Enter url')

# Set the session states with the default values of the button to False 
st.session_state['upload_image_clicked'] = False
st.session_state['image_url_clicked'] = False

# When 'Upload image' button is clicked
if upload_image_button:
    # Set the upload_image_clicked flag to True
    upload_image_clicked = True
else:
    upload_image_clicked = False

# When 'Enter url' button is clicked
if image_url_button:
    # Set the image_url_clicked flag to True
    image_url_clicked = True
else:
    image_url_clicked = False


# Get the image from the clicked button (from path or url)
image = get_image(upload_image_clicked, image_url_clicked, upload_image, image_url)

# Check the source of the image
image_source = check_image_source(image, upload_image_clicked, image_url_clicked)


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
            # If the image is coming from path
            img_path = upload_and_retrieve_image(image)
            pred = request_path_pred(img_path)
        else:
            # Image is from url
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







#########################

# if image is not None:
#     # get the bytes value of the image
#     bytes_data = image.getvalue()
#     # upload image to deta uring put with filename
#     drive.put(image.name, data=bytes_data)


# # download image
# download_image = drive.get(image.name)

# # read the downloaded image (returns image bytes)
# image_data = download_image.read()
# # dont run this (will crash page)
# image_data = base64.b64encode(image_data).decode('utf-8')


# st.write(type(image_data))

# # open image as PIL object
# img = Image.open(io.BytesIO(image_data))

# st.write(img.mode)
# st.write(img.format)
# st.image(img)


# # Function to upload and download image using Deta Drive
# def upload_and_retrieve_image(image):
#     # Upload image
#     if image is not None:
#         # Get the bytes value of the image
#         bytes_data = image.getvalue()        
#         # Upload image to the Deta Drive
#         drive.put(image.name, data=bytes_data)
    
#     # Download image
#     if image is not None:
#         # Retrieve image from the Deta Drive
#         download_image = drive.get(image.name)
#         # Read the image data from download_image
#         image_data = download_image.read()
#         # Create a stream from the image data
#         stream = io.BytesIO(image_data)
#         # Open image using PIL
#         img = Image.open(stream)

#         return img

# img = upload_and_retrieve_image(image)
# st.write(type(img))
# if img.format.lower() == 'jpeg':
#     st.write('correct')




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