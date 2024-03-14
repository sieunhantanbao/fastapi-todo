from database import Base
from .base_entity import BaseEntity
from sqlalchemy import Column, String, Float
from sqlalchemy.orm import relationship
from schemas.user import User

class Company(Base, BaseEntity):
    __tablename__ = "companies"

    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    rating = Column(Float, nullable=True)    
    users = relationship("User", back_populates="company", lazy=True)