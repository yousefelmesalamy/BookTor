from rest_framework import serializers
from .models import bloodTest
from django.contrib.auth.models import User
from django.conf import settings
import joblib
from sklearn.ensemble import RandomForestClassifier

class bloodTestSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(source='user.username',
                                   default=serializers.CurrentUserDefault())

    class Meta:
        model = bloodTest
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['patient_username'] = instance.user.username
        return response

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        obj = bloodTest.objects.create(**validated_data)
        return obj


    def predict(self):
        data = self.validated_data
        age = data.get('age')
        bmi = data.get('bmi')
        glucouse = data.get('glucouse')
        insuline = data.get('insuline')
        homa = data.get('homa')
        leptin = data.get('leptin')
        adiponcetin = data.get('adiponcetin')
        resistiin = data.get('resistiin')
        mcp = data.get('mcp')
        all_data = [age, bmi, glucouse, insuline, homa, leptin, adiponcetin, resistiin, mcp]

        loaded_model = joblib.load(open("ml_models/bloodmodelRBF", 'rb'))
        clf = loaded_model.predict([all_data])
        result = None
        if clf[0] == 0:
            result = "No Cancer"
        elif clf[0] == 1:
            result = "Cancer"

        # self.instance.result = result

        return result
