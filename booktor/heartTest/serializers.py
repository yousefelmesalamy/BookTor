from rest_framework import serializers
from .models import heartTest
from django.conf import settings
import joblib


class heartTestSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        default=serializers.CurrentUserDefault(),
        queryset=settings.AUTH_USER_MODEL.objects.all(), )
    patient_name = serializers.SerializerMethodField()

    class Meta:
        model = heartTest
        fields = '__all__'

    def get_patient_name(self, instance):
        return f"{instance.user.first_name} {instance.user.last_name}"

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
