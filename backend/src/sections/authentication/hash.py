from passlib.context import CryptContext
from passlib.hash import bcrypt
from passlib.exc import UnknownHashError



pwdContext = CryptContext(
    schemes=['pbkdf2_sha256']
)


def generate_password_hash(password: str) -> str:
    hash = pwdContext.hash(password)
    return hash


def verify_password(password: str, hash: str) -> bool:
    try:
        pwdContext.verify(password, hash)
    except UnknownHashError:
        return bcrypt.verify(password, hash)
