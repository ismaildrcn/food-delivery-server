import os
import jwt
import datetime

from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from dotenv import load_dotenv

from db.models.user import User
from db.session import get_db
from api.utils.password import password_hash, password_verify

load_dotenv()
TOKEN_SECRET_KEY = os.getenv("TOKEN_SECRET_KEY")

class UserLogin(BaseModel):
    email: str
    password: str


class UserCreate(BaseModel):
    username: str = ""
    email: str
    first_name: str = ""
    last_name: str = ""
    country_code: int = 90
    phone_number: str = ""
    password: str


router = APIRouter()

# Token oluşturma fonksiyonu
def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, TOKEN_SECRET_KEY, algorithm="HS256")
    return encoded_jwt


@router.post("/auth/login")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
    else:
        if not password_verify(db_user.password, user.password):
            raise HTTPException(status_code=401, detail="Geçersiz şifre")

        access_token = create_access_token(data={"sub": user.email})

        return {"access_token": access_token, "token_type": "bearer"}

    
@router.post("/auth/register")
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    response = db.query(User).filter(User.email == user.email).first()
    if response:
        raise HTTPException(status_code=400, detail="Kullanıcı zaten var")
    else:
        db_user = User(
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            country_code=user.country_code,
            phone_number=user.phone_number,
            password=password_hash(user.password)
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
