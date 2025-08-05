from sqlalchemy import Column, Integer, DateTime, Boolean
from datetime import datetime
from sqlalchemy.dialects.mysql import ENUM as MySQLEnum

from app.db.db import Base
from app.models.workflow_status import WorkflowStatus

class Workflow(Base):
    __tablename__ = "workflow"

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(
        MySQLEnum(*[e.value for e in WorkflowStatus], name="workflow_status_enum"),
        nullable=False,
        default=WorkflowStatus.STARTED.value,
        index=True,
    )
    created_at = Column(DateTime, default = datetime.now)
    # onupdate 옵션: 해당 레코드가 업데이트될 때마다 자동으로 현재 시각으로 필드값 갱신
    updated_at = Column(DateTime, default = datetime.now, onupdate = datetime.now)