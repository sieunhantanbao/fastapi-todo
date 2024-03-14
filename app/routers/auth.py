
from datetime import timedelta
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db_context
from services import auth as auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/token")
async def get_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db_context)):
    user = auth_service.authenticate(form_data.username, form_data.password, db)
    if not user:
        raise auth_service.token_exception()
    access_token, expire = auth_service.create_access_token(user, timedelta(minutes=10))
    return {
            "access_token":  access_token,
            "token_type": "bearer",
            "expire_in": expire
            }