from fastapi import APIRouter, BackgroundTasks, WebSocket, WebSocketDisconnect

from app.utils.agent import start_workflow
from app.utils.websocket import connect

agent_api = APIRouter(
    prefix="/workflows",
    tags=["workflow"]
)

@agent_api.post("/")
def test_deepauto_ai(background_task: BackgroundTasks):
    id = start_workflow(background_task)
    return { "status": 201, "data": { "id": id } }

@agent_api.websocket("/ws/{workflow_id}")
async def deepauto_ai_websocket(websocket: WebSocket, workflow_id: int):
    await connect(websocket, workflow_id)