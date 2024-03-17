from datetime import timedelta
from datetime import datetime
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from schemas.user import User, verify_password
from jose import JWTError, jwt
from uuid import UUID

from settings import JWT_SECRET, JWT_ALGORITHM

oa2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token")

def authenticate(username: str, password: str, db: Session):
    user = db.query(User).filter(User.user_name == username).first()

    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def token_exception():
    return HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Invalid username or password",
        headers = {"WWW-Authenticate": "Bearer"}
    )

def create_access_token(user: User, expires: Optional[timedelta] = None):
    claims = {
        "sub": user.user_name,
        "id": str(user.id),
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_admin": user.is_admin,
        "is_active": user.is_active,
        "company_id": str(user.company_id)
    }
    expire = datetime.now() + expires if expires else datetime.now() + timedelta(minutes=10)
    claims.update({"exp": expire})
    return jwt.encode(claims, JWT_SECRET, algorithm=JWT_ALGORITHM), expire

def token_interceptor(token: str = Depends(oa2_bearer)) -> User:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user = User()
        user.user_name = payload.get("sub")
        user.id = UUID(payload.get("id"))
        user.first_name = payload.get("first_name")
        user.last_name = payload.get("last_name")
        user.is_admin = payload.get("is_admin")
        user.is_active = payload.get("is_active")
        user.company_id = UUID(payload.get("company_id"))
        
        if user.user_name is None or user.id is None or not user.is_active:
            raise token_exception()
        return user
    except JWTError:
        raise token_exception()