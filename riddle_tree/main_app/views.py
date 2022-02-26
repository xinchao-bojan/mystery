from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .serializers import QuestionBasicSerializer
from .models import Question


class GetQuestionApiVIew(generics.RetrieveAPIView):
    serializer_class = QuestionBasicSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, slug):
        question = get_object_or_404(Question, slug=slug)
        try:
            if (question.id == 1) or (request.user in question.previous_answer.user_list.all()):
                serializer = QuestionBasicSerializer(question)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_404_NOT_FOUND)
