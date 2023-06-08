from .views import *
from django.urls import path
from rest_framework import routers

router = routers.DefaultRouter()
router.register('heart_test', heartTest_ViewSet, basename='heart_test')

urlpatterns = [
]

urlpatterns += router.urls
