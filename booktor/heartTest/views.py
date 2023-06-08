from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import heartTest
from .serializers import heartTestSerializer


# Create your views here.
class heartTest_ViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = heartTest.objects.all()
    serializer_class = heartTestSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user__id', 'user__username', 'id', 'date', "result"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            result = serializer.predict()
            serializer.save(result=result)
            return Response({"response": result}, status=status.HTTP_201_CREATED)
        else:
            return Response({"response": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)
