from fastapi import APIRouter, WebSocket

from app.utils.websocket import connect

websocket_api = APIRouter(
    tags=["websocket"]
)

@websocket_api.websocket("/ws/{workflow_id}")
async def deepauto_ai_websocket(websocket: WebSocket, workflow_id: int):
    await connect(websocket, workflow_id)