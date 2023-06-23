from .serializers import UserSerializer, DoctorProfile
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

    # def create(self, request, *args, **kwargs):
    #     # data_1 = {key: value for key, value in request.data.items() if key in USERSSS.Meta.fields}
    #     data_1 = {
    #         'username': request.data["username"],
    #         'first_name': request.data["first_name"],
    #         'last_name': request.data["last_name"],
    #         'email': request.data["email"],
    #         'password1': request.data["password1"],
    #         'password2': request.data["password2"],
    #     }
    #     try:
    #         is_doctor = request.data["is_doctor"]
    #     except Exception as e:
    #         is_doctor = False
    #         print(e)
    #     data_2 = {
    #         'name': request.data["name"],
    #         'profile_picture': request.data["profile_picture"],
    #         'bio': request.data["bio"],
    #         'phone_number': request.data["phone_number"],
    #         'gander': request.data["gander"],
    #         'age': request.data["age"],
    #         'is_doctor': is_doctor
    #     }
    #     serializer = UserSerializer(data=data_2, context={'request': request})
    #     if User.objects.filter(username=data_1['username']).exists():
    #         return Response({"Response": "username already exist !"}, status=status.HTTP_401_UNAUTHORIZED)
    #     elif User.objects.filter(email=data_1['email']).exists():
    #         return Response({"Response": "email already exist !"}, status=status.HTTP_401_UNAUTHORIZED)
    #     elif data_1['password1'] != data_1['password2']:
    #         return Response({"Response": "Passwords not matched !"}, status=status.HTTP_401_UNAUTHORIZED)
    #     else:
    #         if serializer.is_valid():
    #             user = User.objects.create_user(username=data_1["username"],
    #                                             password=data_1["password1"], email=data_1["email"],
    #                                             first_name=data_1["first_name"],
    #                                             last_name=data_1["last_name"])
    #
    #             serializer.save(user=user)
    #             user.save()
    #             # instance = (instance_1, instance_2)
    #
    #             token = Token.objects.get(user=user).key
    #             return Response({"token": token, "user_id": user.id}, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
