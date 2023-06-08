from rest_framework.routers import DefaultRouter
from .views import alzhimarTest_ViewSet

router = DefaultRouter()
router.register('alzhimarTest', alzhimarTest_ViewSet, basename='alzhimarTest')

urlpatterns = []
urlpatterns += router.urls
