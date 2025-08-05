import json
import asyncio

from typing import Dict, List
from fastapi import WebSocket

from app.crud.crud import get_workflow_status, get_workflow_agent_response



# workflow_id별로 연결된 WebSocket 클라이언트들을 관리
active_connections: Dict[int, List[WebSocket]] = {}
        
async def connect(websocket: WebSocket, workflow_id: int):
    """
    WebSocket 연결을 수락하고 workflow_id별로 관리
    @param websocket 연결하고자 하는 웹소켓
    @param workflow_id 자신이 실행한 workflow_id
    """
    await websocket.accept()

    if workflow_id not in active_connections:
        active_connections[workflow_id] = []
            
    active_connections[workflow_id].append(websocket)
    
    # 연결 시 기존 데이터 전송
    await send_existing_data(websocket, workflow_id)

async def send_existing_data(websocket: WebSocket, workflow_id: int):
    """
    기존에 저장된 workflow 데이터를 전송
    """
    workflow = get_workflow_status(workflow_id)
    agents = get_workflow_agent_response(workflow_id)

    data = {
        "status": workflow,
        "agent_responses": agents
    }

    await websocket.send_text(json.dumps(data))