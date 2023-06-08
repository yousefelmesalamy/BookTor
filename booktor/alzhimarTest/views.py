from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import alzhimarTest
from .serializers import alzhimarTestSerializer


# Create your views here.
class alzhimarTest_ViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = alzhimarTest.objects.all()
    serializer_class = alzhimarTestSerializer
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
