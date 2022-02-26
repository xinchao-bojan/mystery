from rest_framework import serializers
from .models import Question


class QuestionBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'text', 'supporting_image', 'slug')
        read_only_fields = ('id',)
