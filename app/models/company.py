from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime

class CompapnyViewModel(BaseModel):
    id: UUID
    name: str
    description: str
    rating: float
    created_at: datetime | None = None
    class Config:
        orm_mode: True
        
        
class CompanyCreateOrUpdateModel(BaseModel):
    name: str = Field(min_length=3, title="Name")
    description: str = Field(title="Description")
    rating: int = Field(ge=1, le=5, title="Rating")
    