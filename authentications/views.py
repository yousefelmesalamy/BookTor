from .serializers import UserSerializer, DoctorProfile, MlModelsResultsSerializer
from .models import USER
from .permissons import UserPermission

from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import User

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.decorators import action




# Create your views here.


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)

            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email,
            })
        else:
            return Response({"Response": "username or password was incorrect"}, status=status.HTTP_401_UNAUTHORIZED)


class UserViewSet(viewsets.ModelViewSet):
    queryset = USER.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserPermission]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # pagination_class = StandardResultsSetPagination
    filterset_fields = ['id', 'username', 'email', 'is_active', 'is_doctor', ]

    search_fields = ['username', 'email', 'is_active', 'is_doctor', ]

    lockup_field = 'id'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        token = Token.objects.get(user=serializer.instance).key
        return Response({"Response": serializer.data, "token": token}, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=['get'], permission_classes=[AllowAny])
    def doctorProfile(self, request, pk=None):
        user = self.get_object()
        if user.is_doctor:
            serializer = DoctorProfile(user)
            return Response(serializer.data)
        else:
            return Response({"detail": "user is not doctor"}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def MlModelsResults(self, request, pk=None):
        user = self.get_object()
        serializer = MlModelsResultsSerializer(user)
        return Response(serializer.data)







