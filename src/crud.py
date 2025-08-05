import asyncio
from fastapi import BackgroundTasks

from src.agent import data_collector_agent, itinerary_builder_agent, budget_manager_agent, report_generator_agent
from src.model import Workflow
from src.status import WorkflowStatus
from src.db import connect_database

def start_workflow(background_task: BackgroundTasks):
    """
    agent를 차례대로 실행하는 workflow를 실행시킨다.
    @return workflow id
    """
    workflow = Workflow(
        status=WorkflowStatus.STARTED.value
    )

    with connect_database() as db:
        # workflow 시작 상태 저장
        db.add(workflow)
        db.commit()
        db.refresh(workflow)

     # 2) 백그라운드에서 에이전트 실행 스케줄링
        background_task.add_task(run_agents, workflow.id)

    return workflow.id

async def run_agents(workflow_id: int):
    await data_collector_agent()
    
    await asyncio.gather(
        itinerary_builder_agent(),
        budget_manager_agent(),
    )

    await report_generator_agent()