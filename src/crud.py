from src.model import Workflow
from src.status import WorkflowStatus
from src.db import connect_database
    
def update_workflow_status(workflow_id: int, status: WorkflowStatus):
    with connect_database() as db:
        workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()

        if workflow:
            workflow.status = status.value

            db.commit()
            db.refresh(workflow)