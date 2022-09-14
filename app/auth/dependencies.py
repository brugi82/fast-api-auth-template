import os
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.db import get_db
from app.auth import models

from app.auth.schemas import CryptoConfig
from app.auth.crypto import ACCESS_TOKEN_EXPIRE_MINUTES, verify_password
from app.auth.services import get_user_by_email

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_crypto_config() -> CryptoConfig:
    secret_key = os.environ["FAMT_SECRET_KEY"]
    algo = os.environ["FAMT_ALGORITHM"]
    return CryptoConfig(secret_key=secret_key, algo=algo)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    crypto_config: CryptoConfig = Depends(get_crypto_config),
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, crypto_config.secret_key, algorithms=[crypto_config.algo]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(db, username)
    if not user:
        raise credentials_exception

    return user


def get_current_confirmed_user(user: models.User = Depends(get_current_user)):
    if user.confirmed == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please confirm your email address",
        )
    return user


def create_access_token(
    data: dict,
    crypto_config: CryptoConfig,
    expires_delta: timedelta | None,
):
    copied_data = data.copy()
    if expires_delta:
        exp = datetime.utcnow() + expires_delta
    else:
        exp = datetime.utcnow() + timedelta(minutes=15)
    copied_data.update({"exp": exp})
    encoded_token = jwt.encode(
        copied_data, crypto_config.secret_key, crypto_config.algo
    )
    return encoded_token


def create_user_access_token(user: models.User, crypto_config: CryptoConfig):
    claims = {"sub": user.email}
    print(claims)
    access_token = create_access_token(
        claims, crypto_config, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return access_token


def authenticate_user(username, password, db: Session):
    user = get_user_by_email(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
