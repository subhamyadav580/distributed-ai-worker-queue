from config.celery_app import celery
from services.summary_service import generate_ai_summary


@celery.task
def generate_summary_task(text: str):
    return generate_ai_summary(text)