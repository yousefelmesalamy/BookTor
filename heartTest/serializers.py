from rest_framework import serializers
from .models import heartTest
from django.conf import settings
from django.contrib.auth.models import User
from sklearn.ensemble import RandomForestClassifier
import joblib


class heartTestSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(source='user.username',
                                   default=serializers.CurrentUserDefault())

    class Meta:
        model = heartTest
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['patient_username'] = instance.user.username
        return response

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        heart = heartTest.objects.create(**validated_data)
        return heart

    def predict(self):
        data = self.validated_data

        Age = data.get('Age')
        print(Age)
        Sex = int(data.get('Sex'))
        ChestPainType = float(data.get('ChestPainType'))
        Cholesterol = float(data.get('Cholesterol'))
        FastingBS = float(data.get('FastingBS'))
        MaxHR = float(data.get('MaxHR'))
        ExerciseAngina = float(data.get('ExerciseAngina'))
        Oldpeak = float(data.get('Oldpeak'))
        ST_Slope = float(data.get('ST_Slope'))

        all_data = [Age, Sex, ChestPainType, Cholesterol, FastingBS, MaxHR,
                    ExerciseAngina, Oldpeak, ST_Slope]
        loaded_model = joblib.load("ml_models/HeartAttack_model.pkl")
        result = loaded_model.predict([all_data])
        if int(result[0]) == 1:
            result = 'Have a heart attack'
        elif int(result[0]) == 0:
            result = "don't have a heart attack"
        return result
