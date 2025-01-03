from passlib.context import CryptContext
import logging

pwdContext = CryptContext(
    schemes=['pbkdf2_sha256', 'bcrypt']
)


def generate_password_hash(password: str) -> str:
    hash = pwdContext.hash(password)
    return hash


def verify_password(password: str, hash: str) -> bool:
    logging.getLogger('passlib').setLevel(logging.ERROR)
    return pwdContext.verify(password, hash)
