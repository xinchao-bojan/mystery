def is_question_enable(question=None, user=None):
    return (question.id == 1) or (user in question.previous_answer.user_list.all())

