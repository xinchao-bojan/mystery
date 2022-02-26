from rest_framework import serializers
from .models import Question, Answer, CustomUser


class QuestionBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'text', 'supporting_image', 'slug')
        read_only_fields = ('id',)


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'question', 'text')
        # fields = '__all__'
        read_only_fields = ('id',)
        extra_kwargs = {'question': {'write_only': True}}


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', 'attempts')
        read_only_fields = ('id', 'email', 'first_name', 'last_name')
