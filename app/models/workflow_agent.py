from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.dialects.mysql import ENUM as MySQLEnum

from app.db.db import Base
from app.models.workflow_status_type import WorkflowStatusType

class WorkflowAgent(Base):
    __tablename__ = "workflow_agent"

    id = Column(Integer, primary_key=True, autoincrement=True)
    workflow_id = Column(
        Integer,
        ForeignKey("workflow.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    agent_name = Column(String(100), nullable=False, index=True)
    status = Column(
        MySQLEnum(*[e.value for e in WorkflowStatusType], name="workflow_status_enum"),
        nullable=False,
        default=WorkflowStatusType.STARTED.value,
        index=True,
    )
    created_at = Column(DateTime, default = datetime.now)
    # onupdate 옵션: 해당 레코드가 업데이트될 때마다 자동으로 현재 시각으로 필드값 갱신
    updated_at = Column(DateTime, default = datetime.now, onupdate = datetime.now)