from pydantic import BaseModel, Field
from uuid import UUID

class UserViewModel(BaseModel):
    id: UUID
    user_name: str
    first_name: str
    last_name: str
    is_active: bool
    is_admin: bool
    company_id: UUID
    email: str
    class Config:
        orm_mode: True
    

class UserCreateOrUpdateModel(BaseModel):
    email: str = Field(min_length=1)
    first_name: str = Field(min_length=1)
    last_name: str = Field()
    is_active: bool = Field()
    is_admin: bool = Field()
    password: str = Field()
    company_id: UUID = Field()
    user_name: str = Field(min_length=1)
    