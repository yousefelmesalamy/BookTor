from rest_framework import serializers
from .models import *
from django.conf import settings
# from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'phone',  'password', 'is_doctor')
        read_only_fields = ('id', 'date_joined',)
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
            'username': {'required': True}
        }

    user = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    def get_user(self, instance):
        return instance.user.username

    def get_user_id(self, instance):
        return instance.user.id

    def get_email(self, instance):
        return instance.user.email


    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

