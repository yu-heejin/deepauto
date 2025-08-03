from fastapi import FastAPI
from src.deepauto_service import ask_deepauto_ai
import json

app = FastAPI()

@app.get("/")
def test_deepauto_ai():
    chat_completion = ask_deepauto_ai()

    for chat in chat_completion:
        if chat.choices[0].delta.content is not None:
            print(chat.choices[0].delta.content, end="")