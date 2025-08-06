from sqlalchemy import Column, Integer, DateTime, ForeignKey, JSON
from datetime import datetime

from app.db.db import Base
from app.models.workflow_status_type import WorkflowStatusType

class WorkflowAgentResponse(Base):
    __tablename__ = "workflow_agent_response"

    id = Column(Integer, primary_key=True, autoincrement=True)
    workflow_id = Column(
        Integer,
        ForeignKey("workflow.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    workflow_agent_id = Column(
        Integer,
        ForeignKey("workflow_agent.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    response = Column(JSON, nullable=True)
    created_at = Column(DateTime, default = datetime.now)
    # onupdate 옵션: 해당 레코드가 업데이트될 때마다 자동으로 현재 시각으로 필드값 갱신
    updated_at = Column(DateTime, default = datetime.now, onupdate = datetime.now)