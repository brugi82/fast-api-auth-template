from datetime import datetime
from sqlalchemy.orm import Session
from app.auth import models, schemas
from app.auth.crypto import generate_random_string, get_password_hash
from app.utils import email
import os

APP_BASE_URL = os.environ.get("FAAUTH_APP_BASE_URL")


def get_user(db: Session, user_id: int) -> models.User | None:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> models.User | None:
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_type(
    db: Session, user_type: models.UserType
) -> models.UserTypeModel | None:
    return (
        db.query(models.UserTypeModel)
        .filter(models.UserTypeModel.name == user_type)
        .first()
    )


def create_new_user(
    db: Session,
    user: schemas.CreateUser,
    user_type: models.UserType = models.UserType.Regular,
):
    hashed_password = get_password_hash(user.password)
    secret = generate_random_string()
    user_model_args = user.dict()
    user_model_args.pop("password")

    user_type_model = get_user_type(db, user_type)
    db_user = models.User(**user_model_args, hashed_password=hashed_password)
    db.add(db_user)
    db_user.confirmations.append(
        models.Confirmation(secret=secret, issued_at=datetime.utcnow())
    )
    db_user.user_type = user_type_model
    email.send_invitation_email(
        user.email, user.first_name, f"{APP_BASE_URL}/registration/?secret={secret}"
    )
    db.commit()

    db.refresh(db_user)
    return db_user


def confirm_user_email(db: Session, secret: str):
    confirmation = (
        db.query(models.Confirmation)
        .filter(models.Confirmation.secret == secret)
        .first()
    )
    if confirmation == None:
        raise Exception("Invalid confirmation link")
    if confirmation.used == True:
        raise Exception("Confirmation is already used")
    if (datetime.utcnow() - confirmation.issued_at) > 24:
        raise Exception("Confirmation link expired.")
    confirmation.used = True
    confirmation.used_at = datetime.utcnow()
    confirmation.user.confirmed = True
    db.commit()
