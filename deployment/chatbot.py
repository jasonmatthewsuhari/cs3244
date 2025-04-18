from dotenv import load_dotenv
from PIL import Image
from langchain import LLMChain, PromptTemplate
from langchain_openai import ChatOpenAI
from typing import Tuple
import os

# Rename .env.example to .env, can use bash command below
# mv .env.example .env
load_dotenv()

model = ChatOpenAI(model = "gpt-4o")

process_prompt = PromptTemplate(
    input_variables = ["text", "has_text", "emoji_img", "emoji_txt"],
    template = """
You are an emoji-enhanced assistant that processes both images and text. Based on the inputs below, produce exactly one output:

- If has_text is false: generate an engaging image caption using the emoji from the image ({emoji_img}).
- If has_text is true and emoji_img is empty: amplify the emotional tone of the text "{text}" using the emoji from text ({emoji_txt}).
- If both emoji_img and emoji_txt are present: choose the best emoji between {emoji_img} and {emoji_txt}, then amplify "{text}" with that emoji.

Return only the final result and make sure to incorporate the emoji in the text. The emoji doesn't need to be at the end of the text.
"""
)
process_chain = LLMChain(llm = model, prompt = process_prompt)

# Fill this in
def predict_emoji_from_image(image: Image.Image) -> str:
    return "😂"

# Fill this in
def predict_emoji_from_text(text: str) -> str:
    return "😂"

def process(text: str = "", image: Image.Image = None) -> Tuple[str, str]:
    has_text = bool(text and text.strip())
    emoji_img = predict_emoji_from_image(image) if image else ""
    emoji_txt = predict_emoji_from_text(text) if has_text else ""

    response = process_chain.invoke({
        "text": text,
        "has_text": str(has_text).lower(),
        "emoji_img": emoji_img,
        "emoji_txt": emoji_txt,
    })

    return response["text"], ""

