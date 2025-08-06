from enum import Enum as PyEnum

class WorkflowStatusType(PyEnum):
    STARTED = "STARTED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"