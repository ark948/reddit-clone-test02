from passlib.context import CryptContext



pwdContext = CryptContext(
    schemes=['bcrypt']
)


def genereate_password_hash(password: str) -> str:
    hash = pwdContext.hash(password)
    return hash


def verify_password(password: str, hash: str) -> bool:
    return pwdContext.verify(password, hash)