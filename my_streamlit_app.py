# import streamlit as st
 
from clarifai.client.model import Model
from PIL import Image, ImageDraw, ImageFont
# from IPython.display import display
import textwrap
import re
import base64
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
from PIL import Image, ImageDraw, ImageFilter, ImageFont
load_dotenv()
import os

clarifai_pat = os.getenv("CLARIFAI_PAT")

 



def generate_dalle_image(user_description):
    # Use DALL-E API to generate an image based on the prompt
    prompt = f"You are a Professional Graphic Designer. You have to analyze the {user_description} and create a background image but don't add any text"
    inference_params = dict(quality="standard", size='1024x1024')
    model_prediction = Model("https://clarifai.com/openai/dall-e/models/dall-e-3").predict_by_bytes(prompt.encode(), input_type="text", inference_params=inference_params)
    output_base64 = model_prediction.outputs[0].data.image.base64
    with open('./images/image55.png', 'wb') as f:
      f.write(output_base64)
    return './images/image55.png'

def generate_gpt_turbo(prompt_data):
    # Use GPT-4 Turbo for prompt completion
        # Use GPT-4 Turbo for prompt completion
    prompt=f"""
    You are a Professional Content writer. create a summarizes content.You have to create text content for any kind of job for Like
     FacebooK ,Instagram , Linkedin , video Script etc according to :  {prompt_data} . Dont used emoji and * . Dont create
     any extra text . Just make it precise and simple according to client need.

    e.g1:  If user write like this I want create a job post for any job so  you must create content like below  example Dont make any extra content just make precise and limited content that require :

           We are hiring data engineers .
           Location : Karachi Pakistan
           Job Type : Hybrid
           Contact : mudassir@marketlytics


    e.g2: If user said create post write quotation Like "An apple of eye " so result just give this quote not
    extra content    


    e.g3 : If user said create log for me for my company so dont create any content   

    e.g4 :  If user  said i want weather picture or in there user prompt not specific information present so dont so keep content generation empty or null


    """

    inference_params = dict(temperature=0.2, max_tokens=150)  # Adjust max_tokens for longer text
    model_prediction = Model("https://clarifai.com/openai/chat-completion/models/gpt-4-turbo").predict_by_bytes(prompt.encode(),input_type="text",inference_params=inference_params)
    return model_prediction.outputs[0].data.text.raw



def remove_emojis_and_stars(text):
    # Regular expression pattern for emojis
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)

    # Remove emojis
    text = emoji_pattern.sub(r'', text)

    # Remove double asterisks
    text = text.replace('**', '')

    return text

def format_text(text, max_line_length=50, line_spacing=1):
    # Remove emojis and double asterisks
    text = remove_emojis_and_stars(text)

    # Wrap text to the specified line length
    wrapped_text = textwrap.wrap(text, width=max_line_length)

    # Add line spacing
    line_separator = '\n' * (line_spacing + 1)
    return line_separator.join(wrapped_text)

from PIL import Image, ImageDraw, ImageFilter, ImageFont

def text_edit_img(text,img_path):  
    # Open the image
    img = Image.open(img_path).convert("RGBA")
    background = Image.new("RGBA", img.size, (0,0,0,0))

    # Drawing rounded rectangle with transparency on transparency layer and combining it with the opened image.
    draw = ImageDraw.Draw(background)
    font = ImageFont.truetype('./Fonts/Roboto-Bold.ttf', 20)
    padding = 10  # Adjust padding as needed
    text_bbox = draw.textbbox((0, 0), text, font=font)
    print('textbbox ........',text_bbox)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    shape_size = max(text_width, text_height) + 2 * padding

    # Calculate the position to center the square within the image
    shape_x = (img.width - shape_size) // 2
    shape_y = (img.height - shape_size) // 2

    # Calculate the position to start the wrapped text so that it's centered in the square
    text_x = (img.width - text_width) // 2
    text_y = (img.height - text_height) // 2

    text_x = (img.width - text_width) // 2
    text_y = (img.height - text_height) // 2

    
    draw.rectangle([shape_x, shape_y, shape_x + shape_size, shape_y + shape_size],fill=(210,220,280,70), outline=None)
    new_img = Image.composite(background, img, background)
    draw2 = ImageDraw.Draw(new_img)
    # Add wrapped text to the new image
    draw2.multiline_text((text_x, text_y), text, font=font, fill=(254, 254, 250))

     
    
    # # Typing inspirational quote and author's name on the new image with rounded rectangle/
    # draw2 = ImageDraw.Draw(new_img)
    # draw2.multiline_text((text_x, text_y), text, font=font, fill=(254, 254, 250))

    new_img.save("./images/new_img.png")

    # new_img.show()

    # img.show()




 


 

 