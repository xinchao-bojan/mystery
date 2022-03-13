from rest_framework import serializers
from .models import Question, Answer, CustomUser, Prompt, Promocode


class CustomUserSerializer(serializers.ModelSerializer):
    promocode = serializers.SlugRelatedField(slug_field='text', read_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', 'attempts', 'promocode')
        read_only_fields = ('id', 'email', 'first_name', 'last_name', 'promocode')


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id', 'question', 'text')
        # fields = '__all__'
        read_only_fields = ('id',)
        extra_kwargs = {'question': {'write_only': True}}


class AnswerAdminSerializer(serializers.ModelSerializer):
    subsequent_question = serializers.SlugRelatedField(slug_field='slug', queryset=Question.objects.all())
    user_list = CustomUserSerializer(many=True)

    class Meta:
        model = Answer
        fields = ('id', 'question', 'text', 'subsequent_question', 'user_list')
        read_only_fields = ('id', 'user_list')
        extra_kwargs = {'question': {'write_only': True}}

    def validate(self, attrs):
        if attrs.get('subsequent_question') == attrs.get('question'):
            raise serializers.ValidationError('Subsequent_question and question must be different')
        return attrs


class PreviousAnswerSerializer(serializers.ModelSerializer):
    question = serializers.SlugRelatedField(slug_field='slug', read_only=True)

    class Meta:
        model = Answer
        fields = ('text', 'question')


class QuestionSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display')
    previous_answer = PreviousAnswerSerializer()

    class Meta:
        model = Question
        fields = ('id', 'text', 'supporting_image', 'slug', 'status', 'previous_answer')
        read_only_fields = ('id',)


class QuestionAdminSerializer(serializers.ModelSerializer):
    answers = AnswerAdminSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'text', 'supporting_image', 'slug', 'answers', 'status')
        read_only_fields = ('id',)


class UserCodeSerializer(serializers.ModelSerializer):
    promocode = serializers.SlugRelatedField(slug_field='text', read_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', 'promocode')
        read_only_fields = ('id', 'email', 'first_name', 'last_name', 'promocode')


class PromptSerializer(serializers.ModelSerializer):
    question = serializers.SlugRelatedField(slug_field='slug', queryset=Question.objects.all())

    class Meta:
        model = Prompt
        fields = ('id', 'question', 'text', 'file')
        read_only_fields = ('id',)


class PromocodeSerializer(serializers.ModelSerializer):
    sale = serializers.SlugRelatedField(slug_field='text', read_only=True)
    user = serializers.SlugRelatedField(slug_field='email', read_only=True)

    class Meta:
        model = Promocode
        fields = ('id', 'text', 'sale', 'user')
        read_only_fields = ('id',)
