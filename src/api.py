from fastapi import APIRouter, BackgroundTasks

from src.agent import start_workflow

agent_api = APIRouter(
    prefix="/workflows",
    tags=["workflow"]
)

@agent_api.post("/")
def test_deepauto_ai(background_task: BackgroundTasks):
    id = start_workflow(background_task)
    return { "status": 201, "data": { "id": id } }