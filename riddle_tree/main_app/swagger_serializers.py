from rest_framework import serializers
from .models import Question


class AdminQuestionPost(serializers.Serializer):
    text = serializers.CharField(min_length=1)
    slug = serializers.CharField(min_length=1, max_length=31)
    status = serializers.ChoiceField(choices=Question.STATUSES)
    supporting_image = serializers.ImageField(required=False)


class AnswerQuestion(serializers.Serializer):
    text = serializers.CharField(min_length=1, max_length=255)


class RestoreAttempts(serializers.Serializer):
    attempts = serializers.IntegerField()


class AddAnswer(serializers.Serializer):
    text = serializers.CharField(min_length=1, max_length=255)
    subsequent_question = serializers.CharField(min_length=1, max_length=31)


class AddPrompt(serializers.Serializer):
    text = serializers.CharField(min_length=1, max_length=255)
    file = serializers.ImageField()
    visible = serializers.BooleanField()