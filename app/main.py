from fastapi import FastAPI

from app.api.api import agent_api
from app.api.websocket import websocket_api
from app.db.db import engine, Base
from app.models.workflow import Workflow
from app.models.workflow_agent import WorkflowAgent
from app.models.workflow_agent_response import WorkflowAgentResponse

Base.metadata.create_all(bind=engine)

app = FastAPI(
    docs_url = "/api/docs",
    openapi_url = "/api/openapi.json",
)

app.include_router(agent_api, prefix = "/api/v1")
app.include_router(websocket_api)