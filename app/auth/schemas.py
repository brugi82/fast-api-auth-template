from app.schemas import BaseSchema


class UserBase(BaseSchema):
    email: str
    first_name: str
    last_name: str


class CreateUser(UserBase):
    password: str


class User(UserBase):
    id: int
    confirmed: bool = False
