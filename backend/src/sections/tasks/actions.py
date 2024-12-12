from typing import List
from asgiref.sync import async_to_sync


# local imports
from src.sections.mail import mail, create_message
from src.sections.tasks.celery import client as celery_client


@celery_client.task
def send_email(recipient: List[str], subject: str, body: str):
    print("CALLING send_email TASK")
    try:
        message = create_message(recipient=recipient, subject=subject, body=body)
        print("CELERY OK (1) - Message created.")
    except Exception as error:
        print("CELERY Email was not CREATED.")

    try:
        async_to_sync(mail.send_message)(message)
        print("CELERY OK (2) - Message sent.")
    except Exception as error:
        print("CELERY Email was not SENT.")



# just a test task
@celery_client.task
def add(x, y):
    print("CELERY add TASK")
    return x + y