from typing import List
from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from src.configs.settings import Config
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


config = ConnectionConfig(
    MAIL_USERNAME=Config.MAIL_USERNAME,
    MAIL_PASSWORD=Config.MAIL_PASSWORD,
    MAIL_FROM=Config.MAIL_FROM,
    MAIL_PORT=587,
    MAIL_SERVER=Config.MAIL_SERVER,
    MAIL_FROM_NAME=Config.MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(BASE_DIR, "templates")

)


mail = FastMail(
    config=Config
)


def create_message(recipient: List[str], subject: str, body: str):
    message = MessageSchema(
        recipients=recipient,
        subject=subject,
        body=body,
        subtype=MessageType.html
    )

    return message