from rest_framework import serializers
from .models import *
from django.conf import settings
# from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER
        fields = ('id', 'username', 'email', 'password', 'profile_pic', 'is_doctor')
        read_only_fields = ('id', 'date_joined',)
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'username': {'required': True}
        }

    def create(self, validated_data):
        user = USER.objects.create_user(**validated_data)
        return user
