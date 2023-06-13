from .views import *
from django.urls import path
from rest_framework import routers

router = routers.DefaultRouter()
router.register('bloodTest', bloodTest_ViewSet, basename='bloodTest')

urlpatterns = [
]

urlpatterns += router.urls
