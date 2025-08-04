from fastapi import FastAPI
from src.agent import data_collector_agent

app = FastAPI()

@app.get("/")
def test_deepauto_ai():
    data_collector_agent()