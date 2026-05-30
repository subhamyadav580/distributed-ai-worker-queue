from celery import Celery
from config.settings import Settings

settings = Settings()


celery = Celery(
    "worker",
    broker=settings.rabbitmq_url,
    backend=None,
    include=["tasks.summary_tasks"],
)

celery.conf.task_routes = {
    "tasks.summary_tasks.*": {
        "queue": "summary"
    }
}