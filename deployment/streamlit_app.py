from dotenv import load_dotenv
import streamlit as st
from PIL import Image
from chatbot import process
import warnings
load_dotenv()

warnings.filterwarnings("ignore", category=DeprecationWarning)


st.set_page_config(page_title = "Emoji-Enhanced Chatbot", layout = "centered")
st.title("Emoji-Enhanced Caption & Text Chatbot")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
user_text = st.text_input("Or enter text here:")

if st.button("Generate"):
    image = Image.open(uploaded_file) if uploaded_file else None
    output, _ = process(user_text, image)

    if image and not user_text:
        st.image(image, caption="Uploaded image", use_container_width=True)
        st.markdown(f"**Caption:** {output}")
    elif user_text and not image:
        st.markdown(f"**Amplified Text:** {output}")
    else:
        if image:
            st.image(image, caption="Uploaded image", use_container_width=True)
        st.markdown(f"**Output:** {output}")
else:
    st.info("Please upload an image or enter text, then click Generate.")