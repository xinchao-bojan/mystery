from rest_framework.routers import DefaultRouter
from .views import SaleViewSet,AdminQuestionViewSet

router = DefaultRouter()
router.register(r'sale', SaleViewSet, basename='sale')
router.register(r'question', AdminQuestionViewSet, basename='question')