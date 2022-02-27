from django.db.models import Q
from django.shortcuts import render
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404
from .models import Question, Answer, CustomUser, Prompt
from .utils import is_question_enable, generate_code
from .serializers import QuestionSerializer, AnswerSerializer, CustomUserSerializer, PromptSerializer, \
    QuestionAdminSerializer, AnswerAdminSerializer, UserCodeSerializer


class ListQuestionView(generics.ListAPIView):
    serializer_class = QuestionSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        questions = Question.objects.filter(previous_answer__user_list=request.user)
        q1 = Question.objects.filter(pk=1)
        questions = questions.union(q1)
        serializer = QuestionSerializer(questions.order_by('id'), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AnswerView(generics.CreateAPIView):
    serializer_class = AnswerSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, slug=None):
        question = get_object_or_404(Question, slug=slug)
        if is_question_enable(question, request.user):
            if request.user.enough_attempts():
                request.data_mutable = True
                data = request.data.copy()
                data['question'] = question.pk
                validator = AnswerSerializer(data=data)
                if validator.is_valid():
                    request.user.lose_attempt()
                    answer = question.answers.filter(text=validator.validated_data.get('text').lower())
                    if answer:
                        answer.user_list.add(request.user)
                        if answer.subsequent_question.final and CustomUser.objects.filter(
                                promocode__isnull=False).count() < 100:
                            generate_code(request.user)
                            return Response('You passed the game', status=status.HTTP_200_OK)
                        return Response({'subsequent_question': answer.subsequent_question}, status=status.HTTP_200_OK)
                    return Response('Your answer is wrong', status=status.HTTP_400_BAD_REQUEST)
                return Response(validator.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response('You have run out of attempts ', status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)


class GetQuestionView(generics.RetrieveAPIView):
    serializer_class = QuestionSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, slug=None):
        question = get_object_or_404(Question, slug=slug)
        if is_question_enable(question, request.user):
            serializer = QuestionSerializer(question)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class ListUserView(generics.ListAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = (IsAdminUser,)
    queryset = CustomUser.objects.filter(is_staff=False, is_active=True)


class RestoreAttemptsView(generics.GenericAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = (IsAdminUser,)

    def put(self, request, pk=None):
        user = get_object_or_404(CustomUser, pk=pk)
        validator = CustomUserSerializer(user, data=request.data)
        if validator.is_valid():
            instance = validator.save()
            serializer = CustomUserSerializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(validator.errors, status=status.HTTP_400_BAD_REQUEST)


class RestoreAttemptsForAllView(generics.GenericAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = (IsAdminUser,)

    def put(self, request):
        validator = CustomUserSerializer(data=request.data)
        if validator.is_valid():
            CustomUser.objects.filter(is_staff=False, is_active=True).update(
                attempts=validator.validated_data.get('attempts'))
            return Response('Attempts updated', status=status.HTTP_200_OK)
        return Response(validator.errors, status=status.HTTP_400_BAD_REQUEST)


class PromptCreateView(generics.GenericAPIView):
    serializer_class = PromptSerializer
    permission_classes = (IsAdminUser,)

    def post(self, request, slug=None):
        request.data_mutable = True
        data = request.data.copy()
        data['question'] = get_object_or_404(Question, slug=slug).pk
        validator = PromptSerializer(data=data)
        if validator.is_valid():
            instance = validator.save()
            serializer = PromptSerializer(instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(validator.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, slug=None):
        question = get_object_or_404(Question, slug=slug)
        data = request.data.copy()
        data['question'] = question.pk
        validator = PromptSerializer(question.prompt, data=data, partial=True)
        if validator.is_valid():
            instance = validator.save()
            serializer = PromptSerializer(instance)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(validator.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        question = get_object_or_404(Question, slug=slug)
        question.prompt.delete()
        return Response(status=status.HTTP_202_ACCEPTED)


class MakePromptVisibleView(generics.GenericAPIView):
    permission_classes = (IsAdminUser,)

    def post(self, request, slug):
        question = get_object_or_404(Question, slug=slug)
        question.prompt.make_visibility()
        return Response(status=status.HTTP_202_ACCEPTED)


class ListPromptsView(generics.ListAPIView):
    serializer_class = PromptSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Prompt.objects.filter(visible=True)


class ListAllPromptsView(generics.ListAPIView):
    serializer_class = PromptSerializer
    permission_classes = (IsAdminUser,)
    queryset = Prompt.objects.all()


class ListAllQuestionView(generics.ListAPIView):
    serializer_class = QuestionAdminSerializer
    permission_classes = (IsAdminUser,)
    queryset = Question.objects.all()


class CreateQuestionView(generics.CreateAPIView):
    serializer_class = QuestionSerializer
    permission_classes = (IsAdminUser,)


class AddAnswerView(generics.GenericAPIView):
    serializer_class = AnswerAdminSerializer
    permission_classes = (IsAdminUser,)

    def post(self, request, slug):
        question = get_object_or_404(Question, slug=slug)
        data = request.data.copy()
        data['question'] = question.pk
        print(data)
        validator = AnswerAdminSerializer(data=data)
        if validator.is_valid():
            instance = validator.save()
            serializer = AnswerAdminSerializer(instance)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(validator.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteAnswerView(generics.DestroyAPIView):
    serializer_class = AnswerAdminSerializer
    permission_classes = (IsAdminUser,)
    queryset = Answer.objects.all()

    def delete(self, request, slug=None, pk=None):
        question = get_object_or_404(Question, slug=slug)
        answer = question.answers.filter(pk=pk)
        if answer:
            answer.delete()
            return Response('Deleted', status=status.HTTP_200_OK)
        return Response('Wrong id', status=status.HTTP_404_NOT_FOUND)


class GetPromocodeView(generics.RetrieveAPIView):
    serializer_class = UserCodeSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = UserCodeSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
