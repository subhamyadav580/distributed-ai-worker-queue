from celery import Celery
from config.settings import Settings

settings = Settings()


celery = Celery(
    "worker",
    broker=settings.rabbitmq_url,
    backend="rpc://"
)

# celery.conf.task_routes = {
#     "app.tasks.summary_tasks.*": {
#         "queue": "summary_queue"
#     }
# }