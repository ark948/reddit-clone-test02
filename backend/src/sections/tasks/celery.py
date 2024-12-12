from celery import Celery




client = Celery(backend='redis://localhost:6379/0', broker='redis://localhost:6379/0')
client.config_from_object("src.configs.settings")