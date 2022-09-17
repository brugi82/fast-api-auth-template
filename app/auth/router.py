from fastapi import APIRouter, Depends, status, Response
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth import schemas, models
from app.db import get_db
from app.auth.services import get_user_by_email, create_new_user, confirm_user_email
from app.auth.dependencies import (
    CryptoConfig,
    get_crypto_config,
    authenticate_user,
    create_user_access_token,
    get_current_user,
)

router = APIRouter(prefix="/auth/users")


@router.get("/me", response_model=schemas.UserBase)
def me(user: models.User = Depends(get_current_user)):
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", response_model=schemas.User)
def create_user(user: schemas.CreateUser, session: Session = Depends(get_db)):
    db_user = get_user_by_email(session, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email is already registered")
    new_user = create_new_user(session, user)
    return new_user


@router.post("/login", response_model=schemas.Token)
def user_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    crypto_config: CryptoConfig = Depends(get_crypto_config),
    db: Session = Depends(get_db),
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_user_access_token(user, crypto_config)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/protected")
def protected(user: models.User = Depends(get_current_user)):
    msg = f"You are on protected route. User email {user.email}"
    return msg


@router.post("/confirm")
def confirm_email(confirmation: schemas.Confirmation, db: Session = Depends(get_db)):
    confirm_user_email(db, confirmation.secret)
    return Response(status_code=status.HTTP_200_OK)
