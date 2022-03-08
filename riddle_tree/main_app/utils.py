import random
import string
from .models import Question
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def is_question_enable(question=None, user=None):
    return (question.status == Question.STATUS_FIRST) or (user in question.previous_answer.user_list.all())


def generate_code(user):
    # if user.promocode:
    #     return
    user.promocode = ''.join((random.choice(string.ascii_lowercase) for x in range(8)))
    user.save()
    html = render_to_string('email.html',
                            {'first_name': user.first_name, 'last_name': user.last_name, 'promocode': user.promocode})
    text = strip_tags(html)
    email = EmailMultiAlternatives('mystery', text, settings.EMAIL_HOST_USER, [user.email])
    email.attach_alternative(html, 'text/html')
    email.send()
