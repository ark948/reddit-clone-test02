from celery import Celery




client = Celery(backend='redis://redis:6379/0', broker='redis://redis:6379/0')
client.config_from_object("backend.settings")