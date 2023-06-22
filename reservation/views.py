from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics, mixins, viewsets
from rest_framework import status, filters
from .permissons import *
from .models import *
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import *


# Create your views here.

class Doctor_CategoryViewSet(viewsets.ModelViewSet):
    queryset = Doctor_Category.objects.all()
    serializer_class = Doctor_CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['doctor__username', 'category']
    ordering_fields = ['doctor__username', 'category']

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsDoctorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['doctor__username', 'patient__username', 'date', 'time']
    ordering_fields = ['doctor__username', 'patient__username', 'date', 'time']

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


class DateViewSet(viewsets.ModelViewSet):
    permission_classes = [IsDoctorOrReadOnly]
    queryset = Dates.objects.all()
    serializer_class = DatesSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['doctor__username', 'date']
    ordering_fields = ['doctor__username', 'date']

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)
