from typing import List
from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


config = ConnectionConfig(
    MAIL_USERNAME = "username",
    MAIL_PASSWORD = "something",
    MAIL_FROM = "test@email.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "mail.something.com",
    MAIL_FROM_NAME="Desired Name",
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)


mail = FastMail(
    config=config
)


def create_message(recipient: List[str], subject: str, body: str):
    message = MessageSchema(
        recipients=recipient,
        subject=subject,
        body=body,
        subtype=MessageType.html
    )

    return message