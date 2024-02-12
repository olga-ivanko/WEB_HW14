from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from src.database.db import get_db
from libgravatar import Gravatar

from src.database.models import User
from src.schemas import UserModel


async def get_user_by_email(email: str, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == email).first()
    if db_user is None:
        raise HTTPException(
            status_code=404, detail=f"User with email: {email} was not found"
        )
    return db_user


async def create_user(user: UserModel, db: Session = Depends(get_db)):
    avatar = None
    try:
        g = Gravatar(user.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session = Depends(get_db)):
    user.refresh_token = token
    db.commit()
