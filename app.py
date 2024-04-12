import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image

load_dotenv() 



genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

def get_response(input_prompt, img):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_prompt,img[0]])
    return response.text

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
    
st.set_page_config(page_title='Calorism')

st.header('Gemini Calorie App')

up_file = st.file_uploader('Chose an Image..', type=['jpg','jpeg','png'])
image = ''

if up_file is not None:
    image = Image.open(up_file)
    st.image(image, caption='Uploaded Image',use_column_width=True)
    
c1, c2 = st.columns(2)

with c1:
    submit = st.button('Tell me the Calorie Breakdown')
with c2:
    cook = st.button('Know the Recipe')

input_prompt1 = """
You are an expert nutritionist where you need to see the food items from the image and 
calculate the total calories, also provide the details of every food items
with calories intake in below format

1. Item1 - no. of calories
2. Item2 - no. of calories
3. Item3 - no. of calories
----
----

Finally you can also mention whether the food is healthy or not in 2 lines.

"""

input_prompt2 = """
You are a professional chef where you need to see the food items from the given image and 
provide a step by step recipe for cooking it. Also with the required Ingredients. In below format

Required Items:
1. Item1
2. Item2
3. Item3
...

Recipe:
1. step 1
2. step 2
3. step 3
...

"""
if submit:
    image_data1 = image_setup(up_file)
    response1 = get_response(input_prompt=input_prompt1, img=image_data1)
    st.header('Calorie Breakdown')
    st.write(response1)
    
if cook:
    image_data1 = image_setup(up_file)
    response2 = get_response(input_prompt=input_prompt2, img=image_data1)
    st.header('Here is the Recipe')
    st.write(response2)
