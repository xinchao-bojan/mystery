from django.urls import path, include
from .views import GetQuestionApiVIew

urlpatterns = [
    path('get/<str:slug>/', GetQuestionApiVIew.as_view()),

]
