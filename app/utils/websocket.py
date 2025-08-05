import json
import asyncio

from datetime import datetime
from typing import Dict, List, Any
from fastapi import WebSocket, WebSocketDisconnect

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
    
    # workflow_id별로 연결 관리
    if workflow_id not in active_connections:
        active_connections[workflow_id] = []
    active_connections[workflow_id].append(websocket)
    
    print(f"WebSocket connected for workflow {workflow_id}")
    
    # 연결 시 기존 데이터 전송
    await send_existing_data(websocket, workflow_id)
    
    try:
        # 연결 유지를 위한 무한 루프
        while True:
            # 클라이언트로부터 메시지를 기다림 (연결 유지용)
            await websocket.receive_text()
    except WebSocketDisconnect:
        # 연결 종료 시 정리
        await disconnect(websocket, workflow_id)

async def disconnect(websocket: WebSocket, workflow_id: int):
    """
    WebSocket 연결을 종료하고 관리 목록에서 제거
    """
    if workflow_id in active_connections:
        if websocket in active_connections[workflow_id]:
            active_connections[workflow_id].remove(websocket)
            logger.info(f"WebSocket disconnected for workflow {workflow_id}")
        
        # 해당 workflow_id에 더 이상 연결이 없으면 키 삭제
        if not active_connections[workflow_id]:
            del active_connections[workflow_id]

async def send_existing_data(websocket: WebSocket, workflow_id: int):
    """
    기존에 저장된 workflow 데이터를 전송
    """
    try:
        workflow = get_workflow_status(workflow_id)
        agents = get_workflow_agent_response(workflow_id)

        data = {
            "workflow_status": workflow,
            "agent_responses": agents
        }

        await websocket.send_text(json.dumps(data, ensure_ascii=False))
    except Exception as e:
        print(f"Error sending existing data: {e}")

async def broadcast_to_workflow(workflow_id: int, data: Dict[str, Any]):
    """
    특정 workflow_id에 연결된 모든 클라이언트에게 데이터를 broadcast
    """
    if workflow_id not in active_connections:
        return
    
    # 연결이 끊어진 WebSocket을 추적하기 위한 리스트
    disconnected_sockets = []
    
    for websocket in active_connections[workflow_id]:
        try:
            await websocket.send_text(json.dumps(data, ensure_ascii=False))
        except Exception as e:
            print(f"Error broadcasting to websocket: {e}")
            disconnected_sockets.append(websocket)
    
    # 끊어진 연결들을 제거
    for websocket in disconnected_sockets:
        if websocket in active_connections[workflow_id]:
            active_connections[workflow_id].remove(websocket)
    
    # 더 이상 연결이 없으면 키 삭제
    if not active_connections[workflow_id]:
        del active_connections[workflow_id]

async def broadcast_agent_status(workflow_id: int, agent_id: int, agent_name: str, status: str):
    """
    Agent 상태 변경을 broadcast
    """
    data = {
        "agent_name": agent_name,
        "status": status,
        "timestamp": datetime.now().isoformat()
    }
    await broadcast_to_workflow(workflow_id, data)

async def broadcast_agent_response_chunk(workflow_id: int, agent_id: int, agent_name: str, chunk: str):
    """
    Agent 응답 스트림 chunk를 broadcast
    """
    data = {
        "agent_name": agent_name,
        "chunk": chunk,
        "timestamp": datetime.now().isoformat()
    }
    await broadcast_to_workflow(workflow_id, data)

async def broadcast_agent_complete_response(workflow_id: int, agent_id: int, agent_name: str, response_data: Any):
    """
    Agent 완전한 응답을 broadcast
    """
    data = {
        "agent_name": agent_name,
        "response_data": response_data,
        "timestamp": datetime.now().isoformat()
    }
    await broadcast_to_workflow(workflow_id, data)

async def broadcast_workflow_status(workflow_id: int, status: str):
    """
    Workflow 상태 변경을 broadcast
    """
    data = {
        "status": status,
        "timestamp": datetime.now().isoformat()
    }
    await broadcast_to_workflow(workflow_id, data)