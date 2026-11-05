from celery import Celery
from app.config import Config

def make_celery():
    celery = Celery("antifraude", broker=Config.REDIS_URL, backend=Config.REDIS_URL)
    celery.conf.update(task_serializer="json", accept_content=["json"],
                       result_serializer="json", timezone="America/Sao_Paulo",
                       task_track_started=True)
    return celery

celery = make_celery()
