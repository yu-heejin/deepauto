from fastapi import APIRouter
from src.agent import data_collector_agent, itinerary_builder_agent, budget_manager_agent, report_generator_agent

agent_api = APIRouter(
    prefix="/workflows",
    tags=["workflow"]
)

@agent_api.get("/")
def test_deepauto_ai():
    data_collector_agent()
    # TODO: 비동기 처리
    itinerary_builder_agent()
    budget_manager_agent()
    report_generator_agent()