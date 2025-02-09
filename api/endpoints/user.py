from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from db.models.user import User
from db.session import get_db


class UserCreate(BaseModel):
    username: str
    email: str
    first_name: str = ""
    last_name: str = ""
    country_code: int = 90
    phone_number: str = ""
    password: str


router = APIRouter()

@router.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        country_code=user.country_code,
        phone_number=user.phone_number,
        password=user.password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user