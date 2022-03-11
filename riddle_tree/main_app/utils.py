import random
import string

from django.db.models import F, Count
from .models import Question, Sale, Promocode
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def is_question_enable(question=None, user=None):
    return (question.status == Question.STATUS_FIRST) or (user in question.previous_answer.user_list.all())


def generate_code(user, sales):
    try:
        if user.promocode:
            return
    except:
        pass
    Promocode.objects.create(text=''.join((random.choice(string.ascii_lowercase) for x in range(8))),
                             sale=sales.first(), user=user)
    try:
        html = render_to_string('email.html',
                                {'first_name': user.first_name, 'last_name': user.last_name,
                                 'promocode': user.promocode.text})
        text = strip_tags(html)
        email = EmailMultiAlternatives('mystery', text, settings.EMAIL_HOST_USER, [user.email])
        email.attach_alternative(html, 'text/html')
        email.send()
    except:
        print(f'Error in email sending with {user.email}')


def promocodes_available():
    sale = Sale.objects.annotate(promocode_user=Count('promocode')).filter(max_users__gt=F('promocode_user')).order_by(
        'max_users')
    return sale
