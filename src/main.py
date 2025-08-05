from fastapi import FastAPI

from src.api import agent_api
from src.db import engine, Base
from src.model import Workflow

app = FastAPI(
    docs_url = "/api/docs",
    openapi_url = "/api/openapi.json",
)

Base.metadata.create_all(bind=engine)

app.include_router(agent_api, prefix = "/api/v1")