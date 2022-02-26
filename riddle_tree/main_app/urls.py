from django.urls import path, include
from .views import GetQuestionView,ListQuestionView,AnswerView,ListUserView,RestoreAttemptsView,RestoreAttemptsForAllView

urlpatterns = [
    path('question/<str:slug>/', GetQuestionView.as_view()),
    path('question/<str:slug>/answer/', AnswerView.as_view()),
    path('question/', ListQuestionView.as_view()),
    path('users/', ListUserView.as_view()),
    path('users/restore/<int:pk>/', RestoreAttemptsView.as_view()),
    path('users/restore/<int:pk>/', RestoreAttemptsForAllView.as_view()),

]
