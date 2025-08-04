from fastapi import FastAPI
from src.agent import data_collector_agent, itinerary_builder_agent

app = FastAPI()

@app.get("/")
def test_deepauto_ai():
    data_collector_agent()
    itinerary_builder_agent()