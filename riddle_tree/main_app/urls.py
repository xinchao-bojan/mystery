from django.urls import path, include
from .routers import router
from .views import GetQuestionView, ListQuestionView, AnswerView, ListUserView, RestoreAttemptsView, \
    RestoreAttemptsForAllView, PromptCreateView, MakePromptVisibleView, ListPromptsView, ListAllPromptsView, \
    AddAnswerView, GetPromocodeView, GetPromptsView, GetStatusesView, UpdateAnswerView, UserView

urlpatterns = [
    path('question/<str:slug>/', GetQuestionView.as_view()),
    path('question/<str:slug>/answer/', AnswerView.as_view()),
    path('question/', ListQuestionView.as_view()),
    path('prompt/', ListPromptsView.as_view()),
    path('prompt/<str:slug>/', GetPromptsView.as_view()),
    path('me/', GetPromocodeView.as_view()),

    path('admin/', include(router.urls)),
    path('admin/users/', ListUserView.as_view()),
    path('admin/users/<int:pk>/', UserView.as_view()),
    path('admin/prompts/', ListAllPromptsView.as_view()),
    path('admin/users/restore/<int:pk>/', RestoreAttemptsView.as_view()),
    path('admin/users/restore/', RestoreAttemptsForAllView.as_view()),
    path('admin/question/statuses/all/', GetStatusesView.as_view()),
    path('admin/question/<str:slug>/answer/', AddAnswerView.as_view()),
    path('admin/question/<str:slug>/answer/<int:pk>/', UpdateAnswerView.as_view()),
    path('admin/question/<str:slug>/prompt/', PromptCreateView.as_view()),
    path('admin/question/<str:slug>/prompt/visible/', MakePromptVisibleView.as_view()),

]
