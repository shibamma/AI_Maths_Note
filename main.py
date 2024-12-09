import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import base64
import openai
from streamlit_drawable_canvas import st_canvas
import numpy as np

# Initialize OpenAI client
openai.api_key = 'key'

# Function to encode image to base64
def encode_image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# Function to check if the image is not empty
def is_image_empty(image):
    return not np.array(image).any()

# Function to calculate using OpenAI's API
def calculate(image_base64):
    response = openai.ChatCompletion.create(
    model="gpt-4",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Give the answer to this math equation. Only respond with the answer. Only respond with numbers. NEVER Words. Only answer unanswered expressions. Look for equal sign with nothing on the right of it. If it has an answer already. DO NOT ANSWER it."},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{image_base64}",},
                        },
                    ],
                }
            ],
            max_tokens=300,
        )

    answer = response.choices[0].message['content'].strip()
    return answer

# Streamlit UI

# Load the image
image = Image.open('hehe.png')

# Calculate the new dimensions based on the scale factor
scale_factor = 0.25  # 25% of the original size

# Calculate the new width and height
new_width = int(image.width * scale_factor)
new_height = int(image.height * scale_factor)

# Resize the image
resized_image = image.resize((new_width, new_height))

st.image(resized_image)
st.title("AI Math Notes")

# Drawing canvas
canvas_result = st_canvas(
    fill_color="rgba(255, 255, 255, 1)",  # Fixed fill color with some opacity (white background)
    stroke_width=5,
    stroke_color="#000000",  # Black text color
    background_color="#FFFFFF",  # White background
    width=1200,
    height=800,
    drawing_mode="freedraw",
    key="canvas",
)

# Buttons
if st.button("Clear"):
    st.rerun()

if st.button("Calculate"):
    if canvas_result.image_data is not None:
        try:
            # Convert the canvas image data to a PIL image
            image_data = canvas_result.image_data
            image = Image.fromarray(np.uint8(image_data))
            
            # Encode image to base64
            image_base64 = encode_image_to_base64(image)

            # Calculate the result
            answer = calculate(image_base64)
            st.markdown(f"<h1 style='font-size:48px;'>Answer from MEGAT: {answer}</h1>", unsafe_allow_html=True)
            if not answer:
                st.error("No answer returned. Please check the input or try again.")
            else:
                # Draw the answer on the image
                draw = ImageDraw.Draw(image)
                font = ImageFont.load_default()
                draw.text((50, 50), answer, font=font, fill="black")
                
                # Display the image with the answer
                st.image(image)
        except Exception as e:
            st.error(f"Error occurred: {e}")


# Save the image to show the answer
if 'image' in st.session_state:
    st.image(st.session_state['image'])