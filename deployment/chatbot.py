from dotenv import load_dotenv
from PIL import Image
from langchain import LLMChain, PromptTemplate
from langchain_openai import ChatOpenAI
from typing import Tuple
import os
import numpy


load_dotenv(os.path.join(os.getcwd(), "chatbot", "pyvenv.cfg"))
api_key = os.getenv("OPENAI_API_KEY")

model = ChatOpenAI(model = "gpt-4o")

process_prompt = PromptTemplate(
    input_variables = ["text", "image", "has_text", "emoji_img", "emoji_txt"],

    template = """
You are an expressive, emoji-savvy assistant that processes both images and text. Based on the inputs below, generate one clear, engaging response:

Instructions:
- If **has_text** is false:
  → Generate a fun and creative caption for the image ({image}).
  → Use the provided emoji ({emoji_img}) as part of the caption.

- If **has_text** is true and **emoji_img** is empty:
  → Enhance the emotional tone of the text: "{text}".
  → Use the emoji extracted from the text ({emoji_txt}) to enrich it.

- If both **emoji_img** and **emoji_txt** are present:
  → Try to guess the caption's emotion and amplify it: "{text}".
  → Choose the more fitting emoji between {emoji_img} and {emoji_txt}.
  → Incorporate it to the text that you have amplified!

Final Output:
Return only the modified caption or text — naturally enhanced with the chosen emoji.
You can use the emoji more than one time and put it in the middle of the sentences.
Avoid being excessive on using the emojis as well though.
Avoid explanations. The output should be concise, expressive, and emoji-infused.
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
        "image" : image,
        "has_text": str(has_text).lower(),
        "emoji_img": emoji_img,
        "emoji_txt": emoji_txt,
    })

    return response["text"], ""

