from celery import shared_task
from main_app.models import CustomUser,Prompt


@shared_task
def update_attempts():
    CustomUser.objects.filter(is_staff=False).update(attempts=3)


@shared_task
def release_prompt():
    prompt = Prompt.objects.filter(visible=False).order_by('id')
    if prompt:
        prompt = prompt.last()
        prompt.visible = True
        prompt.save()
