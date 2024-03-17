from database import Base
from schemas.base_entity import BaseEntity, Priority, TaskStatus
from sqlalchemy import Column, String, Enum, Uuid, ForeignKey
from sqlalchemy.orm import relationship

class Task(Base, BaseEntity):
    __tablename__ = "tasks"
      
    summary = Column(String, nullable=False)
    description = Column(String, nullable=True)  
    status = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.NEW)
    priority = Column(Enum(Priority), nullable=False, default=Priority.MEDIUM)        
    user_id = Column(Uuid, ForeignKey("users.id"), nullable=False)
    user = relationship("User")