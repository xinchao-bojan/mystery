from rest_framework import serializers
from .models import Question, Answer, CustomUser, Prompt


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'question', 'text')
        # fields = '__all__'
        read_only_fields = ('id',)
        extra_kwargs = {'question': {'write_only': True}}


class AnswerAdminSerializer(serializers.ModelSerializer):
    subsequent_question = serializers.SlugRelatedField(slug_field='slug', queryset=Question.objects.all())

    class Meta:
        model = Answer
        fields = ('id', 'question', 'text', 'subsequent_question')
        read_only_fields = ('id',)
        extra_kwargs = {'question': {'write_only': True}}

    def validate(self, attrs):
        if attrs.get('subsequent_question') == attrs.get('question'):
            raise serializers.ValidationError('Subsequent_question and question must be different')
        return attrs


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'text', 'supporting_image', 'slug', 'answers', 'final')
        read_only_fields = ('id',)


class QuestionAdminSerializer(serializers.ModelSerializer):
    answers = AnswerAdminSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'text', 'supporting_image', 'slug', 'answers', 'final')
        read_only_fields = ('id',)


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', 'attempts', 'promocode')
        read_only_fields = ('id', 'email', 'first_name', 'last_name', 'promocode')


class UserCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', 'promocode')
        read_only_fields = ('id', 'email', 'first_name', 'last_name', 'promocode')


class PromptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prompt
        fields = ('id', 'question', 'text', 'file')
        read_only_fields = ('id',)
