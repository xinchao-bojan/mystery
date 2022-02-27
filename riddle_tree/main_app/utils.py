import random
import string


def is_question_enable(question=None, user=None):
    return (question.id == 1) or (user in question.previous_answer.user_list.all())


def generate_code(user):
    if not user.promocode:
        user.promocode = ''.join((random.choice(string.ascii_lowercase) for x in range(8)))
        user.save()
