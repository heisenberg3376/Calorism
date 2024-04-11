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
    
submit = st.button('Tell me the Calorie Breakdown')


input_prompt = """
You are an expert nutritionist where you need to see the food items from the image and 
calculate the total calories, also provide the details of every food items
with calories intake in below format

1. Item1 - no. of calories
2. Item2 - no. of calories
----
----

Finally you can also mention whether the food is healthy or not in 2 lines.

"""
if submit:
    image_data = image_setup(up_file)
    response = get_response(input_prompt=input_prompt, img=image_data)
    st.header('Your Response is')
    st.write(response)
