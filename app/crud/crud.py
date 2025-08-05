import asyncio
from app.models.workflow import Workflow
from app.models.workflow_agent import WorkflowAgent
from app.models.workflow_agent_response import WorkflowAgentResponse
from app.models.workflow_status_type import WorkflowStatusType
from app.models.workflow_agent_type import WorkflowAgentType
from app.db.db import connect_database

def create_workflow_status():
    workflow = Workflow(status=WorkflowStatusType.STARTED.value)

    with connect_database() as db:
        # workflow 시작 상태 저장
        db.add(workflow)
        db.commit()
        db.refresh(workflow)

    return workflow.id
    
def update_workflow_status(workflow_id: int, status: WorkflowStatusType):
    with connect_database() as db:
        workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()

        if workflow:
            workflow.status = status.value

            db.commit()
            db.refresh(workflow)

def create_workflow_agent(workflow_id: int, agent_name: WorkflowAgentType, status: WorkflowStatusType = WorkflowStatusType.STARTED):
    workflow_agent = WorkflowAgent(
        workflow_id=workflow_id,
        agent_name=agent_name.value,
        status=status.value
    )
    
    with connect_database() as db:
        db.add(workflow_agent)
        db.commit()
        db.refresh(workflow_agent)
    
    return workflow_agent.id

def update_workflow_agent_status(agent_id: int, status: WorkflowStatusType):
    with connect_database() as db:
        agent = db.query(WorkflowAgent).filter(WorkflowAgent.id == agent_id).first()
        
        if agent:
            agent.status = status.value
            db.commit()
            db.refresh(agent)

def create_workflow_agent_response(workflow_id: int, workflow_agent_id: int, response_data: dict):
    agent_response = WorkflowAgentResponse(
        workflow_id=workflow_id,
        workflow_agent_id=workflow_agent_id,
        response=response_data
    )
    
    with connect_database() as db:
        db.add(agent_response)
        db.commit()
        db.refresh(agent_response)
    
    return agent_response.id

def get_workflow_status(workflow_id: int):
    with connect_database() as db:
        workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()

    results = {
        "status": workflow.status,
        "start_at": workflow.created_at.isoformat(),
        "updated_at": workflow.updated_at.isoformat()
    }

    return results

def get_workflow_agent_response(workflow_id: int):
    with connect_database() as db:
        # 해당 워크플로우에 해당하는 모든 에이전트 목록들을 반환한다.
        agents = db.query(WorkflowAgentResponse).filter(WorkflowAgentResponse.workflow_id == workflow_id).all()

    results = [
        {
            "response": agent.response,
            "start_at": agent.created_at.isoformat(),
            "updated_at": agent.updated_at.isoformat()
        }
        for agent in agents
    ]

    return results