from random import choice
from string import ascii_letters
from passlib.context import CryptContext

ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"])


def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def generate_random_string(length: int = 64):
    return "".join(choice(ascii_letters) for i in range(length))
