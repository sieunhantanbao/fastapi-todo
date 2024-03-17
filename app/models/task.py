from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

from schemas.base_entity import Priority, TaskStatus

class TaskViewModel(BaseModel):
    id: UUID
    summary: str
    description: str
    status: TaskStatus
    priority: Priority
    user_id: UUID
    created_at: datetime
    class Config:
        orm_mode: True

class TaskCreateOrUpdateModel(BaseModel):
    summary: str = Field()
    description: str = Field()
    status: TaskStatus = Field(default=TaskStatus.NEW)
    priority: Priority = Field(default=Priority.MEDIUM)
    
    