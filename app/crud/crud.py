from app.models.workflow import Workflow
from app.models.workflow_status_type import WorkflowStatusType
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