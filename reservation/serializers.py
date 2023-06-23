from rest_framework import serializers
from .models import *
from authentications.serializers import *


class Doctor_CategorySerializer(serializers.ModelSerializer):
    # doctor_username = serializers.SerializerMethodField()
    class Meta:
        model = Doctor_Category
        # fields = ['doctor', 'category']
        fields = '__all__'
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['doctor'] = instance.doctor.username
        return data

    def validate(self, attrs):
        doctor = attrs['doctor']
        if Doctor_Category.objects.filter(doctor=doctor).exists():
            raise serializers.ValidationError({"Error_Message": "Doctor already have a category."})
        if attrs['category'] not in dict(Category_CHOICES):
            raise serializers.ValidationError({"Error_Message": "Invalid category."})
        if not doctor.is_doctor:
            raise serializers.ValidationError({"Error_Message": "User must be a doctor."})
        return attrs

    def create(self, validated_data):
        doctor_category = Doctor_Category.objects.create(**validated_data)
        # doctor_category.save()
        return doctor_category




class AppointmentSerializer(serializers.ModelSerializer):
    patient_data = serializers.SerializerMethodField()
    class Meta:
        model = Appointment
        fields = '__all__'

    def get_patient_data(self, obj):
        data = UserSerializer(obj).data
        return data

    def validate(self, attrs):
        doctor = attrs['doctor']
        patient = attrs['patient']
        if doctor == patient:
            raise serializers.ValidationError({"Error_Message": "Doctor and patient must be different."})
        if Appointment.objects.filter(doctor=doctor, patient=patient).exists():
            raise serializers.ValidationError({"Error_Message": "Appointment already exists."})
        if not doctor.is_doctor:
            raise serializers.ValidationError({"Error_Message": "User must be a doctor."})
        if not patient.is_patient:
            raise serializers.ValidationError({"Error_Message": "User must be a patient."})

        if attrs['date'] < datetime.date.today():
            raise serializers.ValidationError({"Error_Message": "Date must be after today."})

        return attrs

    def create(self, validated_data):
        appointment = Appointment.objects.create(**validated_data)
        # appointment.save()
        return appointment

class DatesSerializer(serializers.ModelSerializer):
    doctor_username = serializers.SerializerMethodField()

    class Meta:
        model = Dates
        fields = ['id', 'doctor', 'doctor_username', 'date', 'time_from', 'time_to', 'created_at', 'availability']

    def get_doctor_username(self, obj):
        return obj.doctor.username + ' ' + obj.doctor.last_name

    def validate(self, attrs):
        doctor = attrs['doctor']
        if not doctor.is_doctor:
            raise serializers.ValidationError({"Error_Message": "User must be a doctor."})

        if attrs['date'] < datetime.date.today():
            raise serializers.ValidationError({"Error_Message": "Date must be after today."})

        if attrs['time_from'] < datetime.datetime.now().time():
            raise serializers.ValidationError({"Error_Message": "Time must be after now."})

        if attrs['time_to'] < datetime.datetime.now().time():
            raise serializers.ValidationError({"Error_Message": "Time must be after now."})

        if attrs['time_from'] > attrs['time_to']:
            raise serializers.ValidationError({"Error_Message": "Time from must be before time to."})

        if Dates.objects.filter(doctor=doctor, date=attrs['date'], time_from=attrs['time_from'], time_to=attrs['time_to']).exists():
            raise serializers.ValidationError({"Error_Message": "Date already exists."})

        return attrs

    def create(self, validated_data):
        dates = Dates.objects.create(**validated_data)
        # dates.save()
        return dates
