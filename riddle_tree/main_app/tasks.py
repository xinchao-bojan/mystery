from celery import shared_task
from main_app.models import CustomUser


@shared_task
def update_attempts():
    CustomUser.objects.filter(is_staff=False).update(attempts=3)
