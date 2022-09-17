from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime
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


class Confirmation(Base):
    __tablename__ = "confirmations"

    id = Column(Integer, primary_key=True, index=True)
    secret = Column(String, index=True)
    used = Column(Boolean, default=False)
    used_at = Column(DateTime)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="confirmations")
