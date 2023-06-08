from django.db import models
from django.conf import settings
from datetime import date


# Create your models here.
class bloodTest(models.Model):
    id = models.AutoField(unique=True, primary_key=True, auto_created=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    age = models.IntegerField()
    bmi = models.FloatField()
    glucouse = models.FloatField()
    insuline = models.FloatField()
    homa = models.FloatField()
    leptin = models.FloatField()
    adiponcetin = models.FloatField()
    resistiin = models.FloatField()
    mcp = models.FloatField()
    date = models.DateField(default=date.today, null=False)
    result = models.CharField(max_length=20, null=True)

    def __str__(self):
        return str(self.date)
