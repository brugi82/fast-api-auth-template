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


class UserInDb(User):
    hashed_password: str


class CryptoConfig(BaseSchema):
    secret_key: str
    algo: str


class Token(BaseSchema):
    access_token: str
    token_type: str
