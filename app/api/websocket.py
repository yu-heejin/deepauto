from fastapi import APIRouter, BackgroundTasks, WebSocket, WebSocketDisconnect

from app.utils.agent import start_workflow
from app.utils.websocket import connect

agent_api = APIRouter(
    prefix="/workflows",
    tags=["workflow"]
)

@agent_api.post("/")
def test_deepauto_ai(background_task: BackgroundTasks):
    """workflow 실행 API"""
    id = start_workflow(background_task)
    return { "status": 201, "data": { "id": id } }