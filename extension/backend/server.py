# backend/server.py
from fastapi import FastAPI
from pydantic import BaseModel
from catboost import CatBoostClassifier
import uvicorn
import os
import joblib
from transformers import BertTokenizer, BertModel
import torch
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "https://web.whatsapp.com",
    "http://localhost",
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

bert_model_name = 'bert-base-uncased'
tokenizer = BertTokenizer.from_pretrained(bert_model_name)
bert_model = BertModel.from_pretrained(bert_model_name)
bert_model.eval()

def get_bert_embedding(text):
    with torch.no_grad():
        inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=512)
        outputs = bert_model(**inputs)
        embeddings = outputs.last_hidden_state
        sentence_embedding = embeddings.mean(dim=1).squeeze().numpy()
        return sentence_embedding.reshape(1, -1)

emoji_map = {
    0: "😂", 1: "😭", 2: "😡", 3: "👍", 4: "🔥"
}

model_path = os.path.join(os.path.dirname(__file__), "../../models/CatBoost.pkl")
model = joblib.load(model_path)

class InputText(BaseModel):
    text: str

@app.post("/predict")
def predict_text(input: InputText):
    try:
        print(f"Received text: {input.text}")
        embedding = get_bert_embedding(input.text)
        prediction = model.predict(embedding)[0]
        emoji = emoji_map.get(int(prediction), "🤖")
        print(f"Prediction: {emoji}")
        return {"emoji": emoji}
    except Exception as e:
        print("❌ Prediction error:", str(e))
        return {"emoji": "💥"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

