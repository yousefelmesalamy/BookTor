from rest_framework import serializers
from .models import *
from django.conf import settings
from reservation.serializers import *
from reservation.models import *


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


class DoctorProfile(serializers.Serializer):
    doctor = serializers.SerializerMethodField()
    speciality = serializers.SerializerMethodField()
    dates = serializers.SerializerMethodField()

    def get_doctor(self, obj):
        try:
            user = UserSerializer(obj).data
            if user.get("is_doctor"):
                data = user
            else:
                # data = {"detail": "User is not a doctor"}
                raise Exception("User is not a doctor")
        except Exception as e:
            print(e)
            data = {"detail": "Doctor not found"}
        return data

    def get_speciality(self, obj):
        doctorCategory = Doctor_Category.objects.filter(doctor=obj)
        data = Doctor_CategorySerializer(doctorCategory, many=True).data
        return data

    def get_dates(self, obj):
        doc = Dates.objects.filter(doctor=obj)
        data = DatesSerializer(doc, many=True).data
        return data
