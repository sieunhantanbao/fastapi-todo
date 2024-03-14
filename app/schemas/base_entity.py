import enum
import uuid
from sqlalchemy import Column, Uuid, Time
from datetime import datetime

class CompanyMode(enum.Enum):
    PUBLIC = 'PUB'
    PRIVATE = 'PRV'

class TaskStatus(enum.Enum):
    NEW = 'NEW'
    IN_PROGRESS = 'INP'
    COMPLETED = 'CMP'
    
class Priority(enum.Enum):
    CRITICAL = 'CRT'
    HIGH = 'HIG'
    MEDIUM = 'MED'
    LOW = 'LOW'

class BaseEntity:
    id = Column(Uuid, primary_key=True, default=uuid.uuid4)
    created_at = Column(Time, nullable=False, default=datetime.now())
    updated_at = Column(Time, nullable=True)