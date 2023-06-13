from rest_framework import serializers
from .models import *


class Doctor_CategorySerializer(serializers.ModelSerializer):
    doctor_name = serializers.SerializerMethodField()

    class Meta:
        model = Doctor_Category
        fields = ['doctor', 'doctor_name', 'category']

    def get_doctor_name(self, obj):
        return obj.doctor.username

    def create(self, validated_data):
        doctor_category = Doctor_Category.objects.create(**validated_data)
        doctor_category.save()
        return doctor_category

    # def validate_doctor(self, value):
    #     #how to check if user is doctor from user model
    #     if value.is_doctor == False:
    #         raise serializers.ValidationError("User must be a doctor.")
    #     return value

    def validate_category(self, value):
        if value not in dict(Category_CHOICES):
            raise serializers.ValidationError("Invalid category.")
        return value

    def doctor_have_one_category(self, value):
        if Doctor_Category.objects.filter(doctor=value).exists():
            raise serializers.ValidationError("Doctor already have a category.")
        return value


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

    def create(self, validated_data):
        appointment = Appointment.objects.create(**validated_data)
        appointment.save()
        return appointment

    def validate_date(self, value):
        if value < datetime.date.today():
            raise serializers.ValidationError("Date must be after today.")
        return value

    def validate_doctors_only(self, value):
        if value.user_goal != 'DOC':
            raise serializers.ValidationError("User must be a doctor.")
        return value

    def validate_patients_only(self, value):
        if value.user_goal != 'PAT':
            raise serializers.ValidationError("User must be a patient.")
        return value


class DatesSerializer(serializers.ModelSerializer):
    doctor_name = serializers.SerializerMethodField()

    class Meta:
        model = Dates
        fields = ['id', 'doctor', 'doctor_name', 'date', 'time_from', 'time_to', 'created_at', 'availability']

    def create(self, validated_data):
        dates = Dates.objects.create(**validated_data)
        dates.save()
        return dates

    def get_doctor_name(self, obj):
        return obj.doctor.username + ' ' + obj.doctor.last_name
    def validate_date(self, value):
        if value < datetime.date.today():
            raise serializers.ValidationError("Date must be after today.")
        return value

    def validate_time_from(self, value):
        if value < datetime.datetime.now().time():
            raise serializers.ValidationError("Time must be after now.")
        return value

    def validate_time_to(self, value):
        if value < datetime.datetime.now().time():
            raise serializers.ValidationError("Time must be after now.")
        return value

    def validate_time_to_after_time_from(self, value):
        if value < self.validate_time_from:
            raise serializers.ValidationError("Time to must be after time from.")
        return value

    def validate_time_from_after_time_to(self, value):
        if value > self.validate_time_to:
            raise serializers.ValidationError("Time from must be before time to.")
        return value
