from django.db import models
from django.conf import settings
from datetime import date


# Create your models here.
class alzhimarTest(models.Model):
    id = models.AutoField(unique=True, primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gender = models.IntegerField()
    Age = models.FloatField()
    EDUC = models.FloatField()
    SES = models.FloatField()
    MMSE = models.FloatField()
    eTIV = models.FloatField()
    nWBV = models.FloatField()
    ASF = models.FloatField()
    date = models.DateField(default=date.today, null=False)
    result = models.CharField(max_length=20, null=True)

    def __str__(self):
        return str(self.date)
