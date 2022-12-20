import os
import requests
import base64
import streamlit as st

from PIL import Image
from dotenv import load_dotenv
# Load environment variable
load_dotenv()

headers = {
    "authorization": st.secrets["auth_key"],
    "content-type": "application/json"
}


# Title and subtitles
st.markdown('<h1 style="color:black;">Kitchenware Image Classification</h1>', unsafe_allow_html=True)
st.markdown('<h2 style="color:gray;">The image classification model classifies image into following categories:</h2>', unsafe_allow_html=True)
st.markdown('<h3 style="color:gray;"> cup, fork, glass, knife, plate, spoon</h3>', unsafe_allow_html=True)
# Hide the first pre-selected radio button
st.markdown('<style>div[role="radiogroup"]>:first-child{display: none !important;}</style>', unsafe_allow_html=True)


# Utensils images url
knife_url = 'https://m.media-amazon.com/images/I/71FtjejRbvL._AC_UL320_.jpg'
fork_url = 'https://m.media-amazon.com/images/I/51j88-h2NZL.jpg'
spoon_url = 'https://m.media-amazon.com/images/I/51Dvu6GiM8L._AC_UL320_.jpg'
cup_url = 'https://m.media-amazon.com/images/I/61Bq3L4gbSL._AC_UL320_.jpg'
glass_url = 'https://m.media-amazon.com/images/I/81B88+ZiRIL._AC_UL320_.jpg'
plate_url = 'https://m.media-amazon.com/images/I/A14F1QVaPNL._AC_UL320_.jpg'


# Classes options to choose
# first element as empty string to hide preselected radio button
classes = ['', 'Knife', 'Fork', 'Spoon', 'Cup', 'Glass', 'Plate', 'Image URL']


# ChatGPT generated definition of predicted classes
def_knife = """
This is the image of knife. A kitchen knife is a tool used in the kitchen for preparing food.
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
This is the image of fork. An eating fork is a utensil that is used for consuming food. It is a pointed,
pronged tool that is used to spear, hold, or lift food to the mouth.
It is typically made of metal, although it can also be made of other materials such as plastic or wood.
Eating forks are commonly used in Western cultures, and they are typically used in combination with a knife and a spoon.
They are used to eat a variety of foods, including meats, vegetables, and grains.
In some cultures, forks are used to scoop up food, while in others, they are used to hold food in place while it is cut with a knife.
"""

def_spoon = """
This is the image of spoon. A spoon is a utensil consisting of a small shallow bowl, oval or round, at the end of a handle.
A spoon is used primarily for stirring, scooping, and serving food and drink.
It is a common utensil in many cultures and is used in both formal and informal dining.
Spoons are made from a variety of materials, such as wood, metal, and plastic, and come in many different sizes and shapes.
They can be used to mix, stir, and scoop a variety of foods, including soups, cereals, sauces, and desserts.
Some spoons, such as teaspoon and tablespoon sizes, are specifically designed for measuring ingredients when cooking or baking.
"""

def_cup = """
This is the image of cup. A drinking cup is a small, open container typically used for drinking liquids such as water, coffee, or tea.
It is usually made of a material such as ceramic, glass, or plastic, and has a handle or grip to allow for easy handling.
Drinking cups can range in size and shape, and can be designed for use in different settings, such as at home, at work, or on the go.
They are commonly used for consuming beverages, and may also be used for storing or serving small amounts of food or other liquids.
"""

def_glass = """
This is the image of glass. A drinking glass is a container made of glass or other transparent material, such as plastic or crystal,
that is used for holding liquids, typically water, juice, or other beverages.
Drinking glasses come in a variety of shapes and sizes, and can be made from a range of materials,
including glass, plastic, and crystal. They are typically used for drinking,
either by holding the glass in the hand or by placing it on a table or other surface and
raising it to the mouth to take sips of the liquid contained within. Drinking glasses can be used in a variety of settings,
including at home, in restaurants and other dining establishments, and at social events.
"""

def_plate = """
This is the image of plate. A plate is a flat, circular dish used for serving food.
Plates are typically made of ceramic, plastic, glass, or metal and come in a variety of sizes and shapes.
They are used to hold, serve, and eat food, and are often used in combination with other tableware such as
forks, knives, and spoons. Plates are an essential part of the table setting at formal dinners and
are also commonly used in everyday meals. In addition to serving food, plates can also be used for decorative purposes,
such as displaying food at a buffet or displaying a collection of decorative plates on a wall.
"""



# Function to get background image to streamlit
@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Function to set background image
def set_img_as_page_bg(img_file):
    bin_str = get_base64_of_bin_file(img_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    background-repeat: no-repeat;
    background-attachment: scroll; # doesn't work
    }
    </style>
    ''' % bin_str

    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

# Call function to set the background image
set_img_as_page_bg('bg-image.jpg')




# Define radio buttons for classes
radio_button = st.radio('Choose image class or enter image url to make prediction', classes)
# Function to create radio button for classes
def radio_func():
    if radio_button == '':
        url = None
    elif radio_button == 'Knife':
        url = knife_url
    elif radio_button == 'Fork':
        url = fork_url
    elif radio_button == 'Spoon':
        url = spoon_url
    elif radio_button == 'Cup':
        url = cup_url
    elif radio_button == 'Glass':
        url = glass_url
    elif radio_button == 'Plate':
        url = plate_url
    # enter customer url
    else:
        if radio_button == 'Image URL':
            url = st.text_input('Please enter image url')            
    return url

# Call radio buttons function 
img_url = radio_func()



# Function to make prediction from aws lambda and gateway api
def predict_class(url):
    API_URL = os.getenv('API_URL')
    data_url = {'url': url}
    result = requests.post(API_URL, json=data_url).json()
    return result



# Create two columns for display input image and output prediction
c1, c2 = st.columns(2)
if img_url: # display image in column 1
    response = requests.get(img_url, stream=True).raw
    img = Image.open(response)
    img = img.resize((300, 350))
    c1.header('Input Image')
    c1.image(img)

if img_url: # display prediction in column 2
    c2.header('Output')
    c2.subheader('ChatGPT generated definition of predicted class!')
    pred = predict_class(img_url)
    if pred == 'knife':
        c2.markdown(def_knife)
    elif pred == 'fork':
        c2.markdown(def_fork)
    elif pred == 'spoon':
        c2.markdown(def_spoon)
    elif pred == 'cup':
        c2.markdown(def_cup)
    elif pred == 'glass':
        c2.markdown(def_glass)
    elif pred == 'plate':
        c2.markdown(def_plate)



# Add kitchenware kaggle competition link in the footer
footer = """<style>
a:link , a:visited{
color: ligthblue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: blue;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: absolute;
display:block;
padding:120px;
background-color: ligthgrey;
color: darkblue;
text-align: center;
}
</style>
<div class="footer">
<p>To participate in the Kitchware Classification competition <a style='display: block; text-align: center;' href="https://www.kaggle.com/competitions/kitchenware-classification" target="_blank">Click here</a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)
