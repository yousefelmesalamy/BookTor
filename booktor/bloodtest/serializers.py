from rest_framework import serializers
from .models import bloodTest
from django.conf import settings
import joblib


class bloodTestSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        default=serializers.CurrentUserDefault(),
        queryset=settings.AUTH_USER_MODEL.objects.all(), )
    patient_name = serializers.SerializerMethodField()
    class Meta :
        model = bloodTest
        fields = '__all__'
    def get_patient_name(self,instance):
        return f"{instance.user.first_name} {instance.user.last_name}"

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
