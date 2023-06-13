from rest_framework import serializers
from .models import alzhimarTest
from django.contrib.auth.models import User
import pickle
from django.contrib.auth.models import User


class alzhimarTestSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(source='user.username',
                                   default=serializers.CurrentUserDefault())

    # patient_name = serializers.SerializerMethodField()

    class Meta:
        model = alzhimarTest
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['patient_name'] = f"{instance.user.first_name} {instance.user.last_name}"
        return response

    # def get_patient_name(self, instance):
    #     return f"{instance.user.first_name} {instance.user.last_name}"
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        obj = alzhimarTest.objects.create(**validated_data)
        return obj


    def predict(self):
        data = self.validated_data
        gender = data.get('gender')
        age = data.get('Age')
        EDUC = data.get('EDUC')
        SES = data.get('SES')
        MMSE = data.get('MMSE')
        eTIV = data.get('eTIV')
        nWBV = data.get('nWBV')
        ASF = data.get('ASF')
        all_data = [gender, age, EDUC, SES, MMSE, eTIV, nWBV, ASF]
        scaler = pickle.load(open("ml_models/alzheimer.scl", "rb"))
        loaded_model = pickle.load(open(r"ml_models/alzheimer.model", "rb"))
        scaled_feature = scaler.transform([all_data])
        prediction = loaded_model.predict(scaled_feature)
        result = None
        if (prediction == 0):
            result = "Nondemented"
        elif (prediction == 1):
            result = "Demented"
        return result
