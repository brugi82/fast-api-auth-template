from sqlite3 import Date
import enum
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship

from app.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    confirmed = Column(Boolean, default=False)
    confirmations = relationship("Confirmation", back_populates="user")
    user_type_id = Column(Integer, ForeignKey("user_types.id"))

    user_type = relationship("UserTypeModel", back_populates="users")


class Confirmation(Base):
    __tablename__ = "confirmations"

    id = Column(Integer, primary_key=True, index=True)
    secret = Column(String, index=True)
    used = Column(Boolean, default=False)
    issued_at = Column(DateTime)
    used_at = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="confirmations")


class UserType(enum.Enum):
    Admin = 1
    Regular = 2
    Anonimous = 3


class UserTypeModel(Base):
    __tablename__ = "user_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Enum(UserType))

    users = relationship("User", back_populates="user_type")
