from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from app.auth import schemas
from app.db import get_db
from app.auth.services import get_user, get_user_by_email, create_new_user

router = APIRouter(prefix="/auth/users")


@router.get("/me", response_model=schemas.User)
def me(session: Session = Depends(get_db)):
    db_user = get_user(session, 1)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/create", response_model=schemas.User)
def create_user(user: schemas.CreateUser, session: Session = Depends(get_db)):
    db_user = get_user_by_email(session, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email is already registered")
    new_user = create_new_user(session, user)
    return new_user
