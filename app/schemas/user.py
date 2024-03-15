from database import Base
from schemas.base_entity import BaseEntity
from sqlalchemy import Column, String, Boolean, Uuid, ForeignKey
from sqlalchemy.orm import relationship
from passlib.context import CryptContext
from schemas.task import Task

bcrypt_context = CryptContext(schemes=["bcrypt"])

class User(Base, BaseEntity):
    __tablename__ = "users"

    email = Column(String, nullable=False, unique=True)
    user_name = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=True)    
    last_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=True)        
    is_active = Column(Boolean, nullable=True, default=True)    
    is_admin = Column(Boolean, nullable=True, default=False)    
    company_id = Column(Uuid, ForeignKey("companies.id"), nullable=False)
    company = relationship("Company")
    taks = relationship("Task", back_populates="user", lazy=True)
    
def get_hashed_password(password):
    return bcrypt_context.hash(password)

def verify_password(plain_text_pass, hashed_password):
    return bcrypt_context.verify(plain_text_pass, hashed_password)