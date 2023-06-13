from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins, viewsets
from rest_framework import status, filters
from .models import Labs, Tests, Lab_Tests, Lab_appointment
from .serializers import LabsSerializer, TestsSerializer, Lab_TestsSerializer, lab_appointmentSerializer


# Create your views here.

class LabsViewSet(viewsets.ModelViewSet):
    queryset = Labs.objects.all()
    serializer_class = LabsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'address', 'phone', 'email', 'work_time_from', 'work_time_to']
    ordering_fields = ['name', 'address', 'phone', 'email', 'work_time_from', 'work_time_to']

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class TestsViewSet(viewsets.ModelViewSet):
    queryset = Tests.objects.all()
    serializer_class = TestsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class Lab_TestsViewSet(viewsets.ModelViewSet):
    queryset = Lab_Tests.objects.all()
    serializer_class = Lab_TestsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['lab__name', 'test__name', 'price']
    ordering_fields = ['lab__name', 'test__name', 'price']

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class lab_appointmentViewSet(viewsets.ModelViewSet):
    queryset = Lab_appointment.objects.all()
    serializer_class = lab_appointmentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['lab__name', 'patient__username', 'date', 'time']
    ordering_fields = ['lab__name', 'patient__username', 'date', 'time']

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)
