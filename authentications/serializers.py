from rest_framework import serializers
from .models import *
from django.conf import settings
from reservation.serializers import Doctor_CategorySerializer, DatesSerializer
from reservation.models import Doctor_Category, Dates

from bloodtest.serializers import bloodTestSerializer
from heartTest.serializers import heartTestSerializer
from alzhimarTest.serializers import alzhimarTestSerializer



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


class MlModelsResultsSerializer(serializers.Serializer):
    def to_representation(self, instance):
        print(instance)
        data = super().to_representation(instance)

        if instance.bloodTest() is not None:
            data['bloodTest'] = bloodTestSerializer(instance.bloodTest()).data

        else:
            data['bloodTest'] = None

        if instance.heartTest() is not None:
            data['heartTest'] = heartTestSerializer(instance.heartTest()).data

        else:
            data['heartTest'] = None

        if instance.alzhimarTest() is not None:
            data['alzhimarTest'] = alzhimarTestSerializer(instance.alzhimarTest()).data

        else:
            data['alzhimarTest'] = None

        return data

