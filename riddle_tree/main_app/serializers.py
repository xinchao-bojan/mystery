from rest_framework import serializers
from .models import Question, Answer, CustomUser, Prompt, Promocode, Sale


class PromocodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promocode
        fields = ('id', 'text', 'qr')
        read_only_fields = ('id',)


class CustomUserSerializer(serializers.ModelSerializer):
    promocode = PromocodeSerializer(read_only=True)

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

    # user_list = CustomUserSerializer(many=True,read_only=True)

    class Meta:
        model = Answer
        fields = ('id', 'question', 'text', 'subsequent_question', 'user_list')
        read_only_fields = ('id', 'user_list')
        extra_kwargs = {'question': {'write_only': True}}

    def validate(self, attrs):
        if attrs.get('subsequent_question') == attrs.get('question'):
            raise serializers.ValidationError('Subsequent_question and question must be different')
        if attrs.get('question').status == Question.STATUS_FINAL:
            raise serializers.ValidationError('Final Question must not have an answer')
        if attrs.get('subsequent_question').status == Question.STATUS_FIRST:
            raise serializers.ValidationError('Subsequent_question must not lead to first question')
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
        lookup_field = "slug"


class QuestionListAdminSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display')
    previous_answer = PreviousAnswerSerializer()

    class Meta:
        model = Question
        fields = ('id', 'text', 'supporting_image', 'slug', 'status', 'previous_answer')
        read_only_fields = ('id', 'previous_answer')
        lookup_field = "slug"


class QuestionUpdateAdminSerializer(serializers.ModelSerializer):
    answers = AnswerAdminSerializer(many=True, read_only=True)
    previous_answer = PreviousAnswerSerializer(read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'text', 'supporting_image', 'answers', 'status', 'previous_answer', 'slug')
        read_only_fields = ('id', 'previous_answer', 'slug')
        lookup_field = "slug"


class QuestionRetrieveAdminSerializer(serializers.ModelSerializer):
    answers = AnswerAdminSerializer(many=True, read_only=True)
    previous_answer = PreviousAnswerSerializer(read_only=True)

    class Meta:
        model = Question
        fields = ('id', 'text', 'supporting_image', 'slug', 'answers', 'status', 'previous_answer')
        read_only_fields = ('id',)


class UserCodeSerializer(serializers.ModelSerializer):
    promocode = PromocodeSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'first_name', 'last_name', 'promocode')
        read_only_fields = ('id', 'email', 'first_name', 'last_name', 'promocode')


class PromptSerializer(serializers.ModelSerializer):
    question = serializers.SlugRelatedField(slug_field='slug', queryset=Question.objects.all())

    class Meta:
        model = Prompt
        fields = ('id', 'question', 'text', 'file', 'visible')
        read_only_fields = ('id',)
        extra_kwargs = {'visible': {'required': False}}

    # def validate(self, attrs):
    #     if Prompt.objects.filter(question=attrs.get('question')):
    #         raise serializers.ValidationError('Question already has prompt')
    #     return attrs


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ('id', 'text', 'max_users', 'slug')
        read_only_fields = ('id',)
