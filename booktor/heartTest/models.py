from django.db import models
from django.conf import settings
from datetime import date


# Create your models here.
class heartTest(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Age = models.FloatField()
    Sex = models.IntegerField()
    ChestPainType = models.FloatField()
    Cholesterol = models.FloatField()
    FastingBS = models.FloatField()
    MaxHR = models.FloatField()
    ExerciseAngina = models.FloatField()
    Oldpeak = models.FloatField()
    ST_Slope = models.FloatField()
    date = models.DateField(default=date.today, null=False)
    result = models.CharField(max_length=20, null=True)

    def __str__(self):
        return str(self.date)
