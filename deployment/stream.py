import os
import requests
import base64
import streamlit as st

from PIL import Image
from dotenv import load_dotenv
from deta import Deta



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
st.markdown('<h1 style="color:white;">Kitchenware Image Classification</h1>', unsafe_allow_html=True)
st.markdown('<h2 style="color:lightgray;">The image classification model classifies image into following categories:</h2>', unsafe_allow_html=True)
st.markdown('<h3 style="color:lightgray;"> cup, fork, glass, knife, plate, spoon</h3>', unsafe_allow_html=True)


# ChatGPT generated definition of predicted classes (for fun)
def_knife = """
A kitchen knife is a tool used in the kitchen for preparing food.
It typically has a sharp blade and a handle, and is used for cutting, chopping, and slicing a variety of ingredients.
There are many different types of kitchen knives, each with a specific purpose.

For example, a chef's knife is a versatile knife with a wide, sharp blade that can be used for a variety of tasks,
including chopping, dicing, and mincing. A paring knife is a small, sharp knife with a pointed tip,
which is useful for peeling and trimming fruits and vegetables.
A bread knife has a serrated edge that is effective for slicing through bread and other baked goods.

Other types of kitchen knives include utility knives, boning knives, and cleavers.
In addition to these traditional knives, there are also specialized knives designed for specific tasks,
such as filleting fish or carving meats.
"""

def_fork = """
An eating fork is a utensil that is used for consuming food. It is a pointed,
pronged tool that is used to spear, hold, or lift food to the mouth.
It is typically made of metal, although it can also be made of other materials such as plastic or wood.
Eating forks are commonly used in Western cultures, and they are typically used in combination with a knife and a spoon.
They are used to eat a variety of foods, including meats, vegetables, and grains.
In some cultures, forks are used to scoop up food, while in others, they are used to hold food in place while it is cut with a knife.
"""

def_spoon = """
A spoon is a utensil consisting of a small shallow bowl, oval or round, at the end of a handle.
A spoon is used primarily for stirring, scooping, and serving food and drink.
It is a common utensil in many cultures and is used in both formal and informal dining.
Spoons are made from a variety of materials, such as wood, metal, and plastic, and come in many different sizes and shapes.
They can be used to mix, stir, and scoop a variety of foods, including soups, cereals, sauces, and desserts.
Some spoons, such as teaspoon and tablespoon sizes, are specifically designed for measuring ingredients when cooking or baking.
"""

def_cup = """
A drinking cup is a small, open container typically used for drinking liquids such as water, coffee, or tea.
It is usually made of a material such as ceramic, glass, or plastic, and has a handle or grip to allow for easy handling.
Drinking cups can range in size and shape, and can be designed for use in different settings, such as at home, at work, or on the go.
They are commonly used for consuming beverages, and may also be used for storing or serving small amounts of food or other liquids.
"""

def_glass = """
A drinking glass is a container made of glass or other transparent material, such as plastic or crystal,
that is used for holding liquids, typically water, juice, or other beverages.
Drinking glasses come in a variety of shapes and sizes, and can be made from a range of materials,
including glass, plastic, and crystal. They are typically used for drinking,
either by holding the glass in the hand or by placing it on a table or other surface and
raising it to the mouth to take sips of the liquid contained within. Drinking glasses can be used in a variety of settings,
including at home, in restaurants and other dining establishments, and at social events.
"""

def_plate = """
A plate is a flat, circular dish used for serving food.
Plates are typically made of ceramic, plastic, glass, or metal and come in a variety of sizes and shapes.
They are used to hold, serve, and eat food, and are often used in combination with other tableware such as
forks, knives, and spoons. Plates are an essential part of the table setting at formal dinners and
are also commonly used in everyday meals. In addition to serving food, plates can also be used for decorative purposes,
such as displaying food at a buffet or displaying a collection of decorative plates on a wall.
"""

# Background Image
filename = '../assets/bg-image.jpg'

# # Store background image on Deta drive
# with open(filename, 'rb') as image_file:
#     drive.put(filename, image_file)

# Function to get background image from Deta drive
@st.cache(allow_output_mutation=True)
def get_bg_image(bin_file):
    # Download background image
    download_image = drive.get(bin_file)
    # Read image data
    image_data = download_image.read()
    return base64.b64encode(image_data).decode()


# Function to set background image
def set_img_as_page_bg(img_file):
    bin_str = get_bg_image(img_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/jpeg;base64,%s");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: scroll; # doesn't work
    }
    </style>
    ''' % bin_str

    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

# Call function to set the background image
set_img_as_page_bg(filename)


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


# Create a button 'upload_image' to add an image from the local computer 
# and 'upload_image_button' to indicate when the image is uploaded
with st.form('image from path', clear_on_submit=True):
        upload_image = st.file_uploader(':orange[Upload an image and press "UPLOAD IMAGE" button]', type=['png', 'jpg', 'jpeg'])
        upload_image_button = st.form_submit_button('UPLOAD IMAGE')

if upload_image_button and upload_image is not None:
    st.markdown('<h5 style="color:white;font-size:18px;">Making prediction on the image from path...</h5>', unsafe_allow_html=True)

# Create a button 'image_url' to get image url from the user
# and 'image_url_button' to indicate when the url is provided
with st.form('image from url', clear_on_submit=True):
        image_url = st.text_input(':orange[Enter custom URL and press "ENTER URL" button]')
        image_url_button = st.form_submit_button('ENTER URL')

if image_url_button and image_url is not None:
    st.markdown('<h5 style="color:white;font-size:18px;">Making prediction on the image from URL...</h5>', unsafe_allow_html=True)

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
            c1.markdown('<h2 style="color:white;font-size:40px;">Input</h2>', unsafe_allow_html=True)
            c1.image(img)
            # If the image is coming from path
            img_path = upload_and_retrieve_image(image)
            pred = request_path_pred(img_path)
        else:
            # Image is from url
            response = requests.get(image, stream=True).raw
            img = Image.open(response)
            img = img.resize((300, 350))
            c1.markdown('<h2 style="color:white;font-size:40px;">Input</h2>', unsafe_allow_html=True)
            c1.image(img)
            pred = request_url_pred(image)

        # Display prediction on second column
        c2.markdown('<h2 style="color:white;font-size:40px;">Output</h2>', unsafe_allow_html=True)
        if pred == 'knife':
            c2.markdown(f'<h3 style="color:white;font-size:32px;">The predicted class is {pred}. That\'s what ChatGPT has to say about it...😀</h3>', unsafe_allow_html=True)
            c2.markdown(f'<h5 style="color:lightgrey;font-size:18px;font-family: \'Roman\', sans-serif;">{def_knife}</h5>', unsafe_allow_html=True)
        if pred == 'fork':
            c2.markdown(f'<h3 style="color:white;font-size:32px;">The predicted class is {pred}. That\'s what ChatGPT has to say about it...😃</h3>', unsafe_allow_html=True)
            c2.markdown(f'<h5 style="color:lightgrey;font-size:18px;font-family: \'Roman\', sans-serif;">{def_fork}</h5>', unsafe_allow_html=True)
        if pred == 'spoon':
            c2.markdown(f'<h3 style="color:white;font-size:32px;">The predicted class is {pred}. That\'s what ChatGPT has to say about it...😄</h3>', unsafe_allow_html=True)
            c2.markdown(f'<h5 style="color:lightgrey;font-size:18px;font-family: \'Roman\', sans-serif;">{def_spoon}</h5>', unsafe_allow_html=True)
        if pred == 'glass':
            c2.markdown(f'<h3 style="color:white;font-size:32px;">The predicted class is {pred}. That\'s what ChatGPT has to say about it...😁</h3>', unsafe_allow_html=True)
            c2.markdown(f'<h5 style="color:lightgrey;font-size:18px;font-family: \'Roman\', sans-serif;">{def_glass}</h5>', unsafe_allow_html=True)
        if pred == 'cup':
            c2.markdown(f'<h3 style="color:white;font-size:32px;">The predicted class is {pred}. That\'s what ChatGPT has to say about it...😆</h3>', unsafe_allow_html=True)
            c2.markdown(f'<h5 style="color:lightgrey;font-size:18px;font-family: \'Roman\', sans-serif;">{def_cup}</h5>', unsafe_allow_html=True)
        if pred == 'plate':
            c2.markdown(f'<h3 style="color:white;font-size:32px;">The predicted class is {pred}. That\'s what ChatGPT has to say about it...😋</h3>', unsafe_allow_html=True)
            c2.markdown(f'<h5 style="color:lightgrey;font-size:18px;font-family: \'Roman\', sans-serif;">{def_plate}</h5>', unsafe_allow_html=True)
        


if __name__=='__main__':
    main()


# Delete image from local path that was stored in Deta drive
if image is not None:
    if (type(image) is not str and
       (image.type == 'image/png' or
       image.type == 'image/jpg' or
       image.type == 'image/jpeg')):
        drive.delete(image.name)


# Add kitchenware kaggle competition link in the footer
footer = """<style>
a:link , a:visited{
color: ligthblue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: white;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: absolute;
display:block;
padding:120px;
background-color: ligthgrey;
color: white;
text-align: center;
}
</style>
<div class="footer">
<p>To participate in the Kitchware Classification competition <a style='display: block; text-align: center;' href="https://www.kaggle.com/competitions/kitchenware-classification" target="_blank">Click here</a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)


