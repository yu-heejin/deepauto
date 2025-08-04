from fastapi import FastAPI
from src.deepauto_service import ask_deepauto_ai
import json

app = FastAPI()

@app.get("/")
def test_deepauto_ai():
    ask_deepauto_ai()