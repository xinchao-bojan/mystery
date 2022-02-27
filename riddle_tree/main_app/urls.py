from django.urls import path, include
from .views import GetQuestionView, ListQuestionView, AnswerView, ListUserView, RestoreAttemptsView, \
    RestoreAttemptsForAllView, PromptCreateView, MakePromptVisibleView, ListPromptsView, ListAllPromptsView, \
    CreateQuestionView, ListAllQuestionView, AddAnswerView, DeleteAnswerView

urlpatterns = [
    path('question/<str:slug>/', GetQuestionView.as_view()),
    path('question/<str:slug>/answer/', AnswerView.as_view()),
    path('question/', ListQuestionView.as_view()),
    path('prompt/', ListPromptsView.as_view()),

    path('admin/users/', ListUserView.as_view()),
    path('admin/prompts/', ListAllPromptsView.as_view()),
    path('admin/users/restore/<int:pk>/', RestoreAttemptsView.as_view()),
    path('admin/users/restore/', RestoreAttemptsForAllView.as_view()),
    path('admin/question/', CreateQuestionView.as_view()),
    path('admin/question/all/', ListAllQuestionView.as_view()),
    path('admin/question/<str:slug>/answer/', AddAnswerView.as_view()),
    path('admin/question/<str:slug>/answer/<int:pk>/', DeleteAnswerView.as_view()),
    path('admin/question/<str:slug>/prompt/', PromptCreateView.as_view()),
    path('admin/question/<str:slug>/prompt/visible/', MakePromptVisibleView.as_view()),

]
