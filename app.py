import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key="AIzaSyCGti29An-hTo9m-7D3hzzbb_fGCVPQnbM")

# Function to get response from Gemini
def get_response(input_prompt, img):
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content([input_prompt, img[0]])
    return response.text

# Function to process the uploaded image
def image_setup(img_file):
    if img_file is not None:
        bytes_data = img_file.getvalue()
        img_parts = [
            {
                'mime_type': img_file.type,
                'data': bytes_data
            }
        ]
        return img_parts
    else:
        raise FileNotFoundError('No file Found')

# Set up the Streamlit app
st.set_page_config(
    page_title='Calorism',
    page_icon="🍏",
    layout="centered",  # Makes the app responsive
)

# Custom CSS for mobile-friendly design
st.markdown(
    """
    <style>
    .stButton button {
        width: 100%;
        padding: 10px;
        font-size: 16px;
    }
    .stFileUploader {
        width: 100%;
    }
    .stImage {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# App header
st.header('🍏 Gemini Calorie App')

# File uploader
up_file = st.file_uploader('Choose an Image...', type=['jpg', 'jpeg', 'png'], key="file_uploader")

# Display the uploaded image
if up_file is not None:
    image = Image.open(up_file)
    st.image(image, caption='Uploaded Image', use_container_width=True)

# Buttons for actions
col1, col2 = st.columns(2)

with col1:
    submit = st.button('Tell me the Calorie Breakdown', key="calorie_button")

with col2:
    cook = st.button('Know the Recipe', key="recipe_button")

# Input prompts
input_prompt1 = """
You are an expert nutritionist where you need to see the food items from the image and 
calculate the total calories, also provide the details of every food items
with calories intake in below format

1. Item1 - no. of calories
2. Item2 - no. of calories
3. Item3 - no. of calories
----
----

Finally, you can also mention whether the food is healthy or not in 2 lines.
"""

input_prompt2 = """
You are a professional chef where you need to see the food items from the given image and 
provide a step-by-step recipe for cooking it. Also, include the required ingredients. In the format below:

Required Items:
1. Item1
2. Item2
3. Item3
...

Recipe:
1. Step 1
2. Step 2
3. Step 3
...
"""

# Handle button clicks
if submit:
    if up_file is not None:
        with st.spinner('Analyzing calorie breakdown...'):
            image_data = image_setup(up_file)
            response = get_response(input_prompt1, image_data)
            st.subheader('Calorie Breakdown')
            st.write(response)
    else:
        st.warning("Please upload an image first.")

if cook:
    if up_file is not None:
        with st.spinner('Generating recipe...'):
            image_data = image_setup(up_file)
            response = get_response(input_prompt2, image_data)
            st.subheader('Here is the Recipe')
            st.write(response)
    else:
        st.warning("Please upload an image first.")

