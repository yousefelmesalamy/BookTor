from .views import *
from django.urls import path
from rest_framework import routers

router = routers.DefaultRouter()
router.register('Doctor_Category', Doctor_CategoryViewSet)
router.register('appointments', AppointmentViewSet)
router.register('dates', DateViewSet)


urlpatterns = [
    ]

urlpatterns += router.urls