from sqlalchemy.orm import Session
from app.auth import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_new_user(db: Session, user: schemas.CreateUser):
    hashed_password = user.password + "123"
    user_model_args = user.dict()
    user_model_args.pop("password")
    db_user = models.User(**user_model_args, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user