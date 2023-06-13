from .views import LabsViewSet, TestsViewSet, Lab_TestsViewSet, lab_appointmentViewSet
from django.urls import path
from rest_framework import routers

router = routers.DefaultRouter()
router.register('Labs', LabsViewSet, basename="LabsViewSet")
router.register('Tests', TestsViewSet, basename="TestsViewSet")
router.register('Lab_Tests', Lab_TestsViewSet, basename="Lab_TestsViewSet")
router.register('lab_appointment', lab_appointmentViewSet, basename="lab_appointmentViewSet")


urlpatterns = [
    ]

urlpatterns += router.urls