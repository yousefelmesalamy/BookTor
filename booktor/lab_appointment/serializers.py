from rest_framework import serializers
from .models import Labs, Tests, Lab_Tests, Lab_appointment
import datetime


class LabsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Labs
        fields = '__all__'

    def create(self, validated_data):
        labs = Labs.objects.create(**validated_data)
        labs.save()
        return labs

    def validate_country(self, value):
        if value not in dict(self.EGYPT_CITIES_CHOICES):
            raise serializers.ValidationError("Invalid category.")
        return value
    def validate_name(self, value):
        if value == "":
            raise serializers.ValidationError("Name must not be empty.")
        return value

    def validate_address(self, value):
        if value == "":
            raise serializers.ValidationError("Address must not be empty.")
        return value

    def validate_phone(self, value):
        if value == "":
            raise serializers.ValidationError("Phone must not be empty.")
        return value

    def validate_email(self, value):
        if value == "":
            raise serializers.ValidationError("Email must not be empty.")
        return value

    def validate_Time_from_to(self, time):
        if self.work_time_from > self.work_time_to:
            raise serializers.ValidationError("Time from must be before time to.")


class TestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tests
        fields = '__all__'

    def create(self, validated_data):
        tests = Tests.objects.create(**validated_data)
        tests.save()
        return tests

    def validate_name(self, value):
        if value == "":
            raise serializers.ValidationError("Name must not be empty.")
        return value


class Lab_TestsSerializer(serializers.ModelSerializer):
    lab_name = serializers.SerializerMethodField()
    test_name = serializers.SerializerMethodField()
    class Meta:
        model = Lab_Tests
        fields = '__all__'

    def create(self, validated_data):
        lab_tests = Lab_Tests.objects.create(**validated_data)
        lab_tests.save()
        return lab_tests

    def get_lab_name(self, obj):
        return obj.lab_id.lab_name

    def get_test_name(self, obj):
        return obj.Test_id.test_name

    def validate_price(self, value):
        if value == "":
            raise serializers.ValidationError("Price must not be empty.")
        return value


class lab_appointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lab_appointment
        fields = '__all__'

    def create(self, validated_data):
        lab_appointment = Lab_appointment.objects.create(**validated_data)
        lab_appointment.save()
        return lab_appointment

    def validate_date(self, value):
        if value < datetime.date.today():
            raise serializers.ValidationError("Date must be after today.")
        return value

    def validate_time(self, value):
        if value < datetime.datetime.now().time():
            raise serializers.ValidationError("Time must be after now.")
        return value
