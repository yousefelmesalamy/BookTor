from django.db import models
from django.conf import settings

# Create your models here.
EGYPT_CITIES_CHOICES = [
    ("Cairo", "Cairo"),
    ("Alexandria", "Alexandria"),
    ("Giza", "Giza"),
    ("Shubra El-Kheima", "Shubra El-Kheima"),
    ("Port Said", "Port Said"),
    ("Suez", "Suez"),
    ("Luxor", "Luxor"),
    ("El-Mansura", "El-Mansura"),
    ("El-Mahalla El-Kubra", "El-Mahalla El-Kubra"),
    ("Tanta", "Tanta"),
    ("Asyut", "Asyut"),
    ("Ismailia", "Ismailia"),
    ("Fayyum", "Fayyum"),
    ("sharqia", "sharqia"),
    ("Aswan", "Aswan"),
    ("Damietta", "Damietta"),
    ("Damanhur", "Damanhur"),
    ("El-Minya", "El-Minya"),
    ("Beni Suef", "Beni Suef"),
    ("Qena", "Qena"),
    ("Sohag", "Sohag"),
    ("Hurghada", "Hurghada"),
    ("6th of October City", "6th of October City"),
    ("Shibin El Kom", "Shibin El Kom"),
    ("Banha", "Banha"),
    ("Kafr el-Sheikh", "Kafr el-Sheikh"),
    ("Arish", "Arish"),
    ("Mallawi", "Mallawi"),
    ("10th of Ramadan City", "10th of Ramadan City"),
    ("Bilbais", "Bilbais"),
    ("Marsa Matruh", "Marsa Matruh"),
    ("Idfu", "Idfu"),
    ("Mit Ghamr", "Mit Ghamr"),
]


class Labs(models.Model):
    lab_country = models.CharField(choices=EGYPT_CITIES_CHOICES, max_length=50, null=False, blank=False)
    lab_name = models.CharField(max_length=50, null=False, blank=False)
    lab_address = models.CharField(max_length=50, null=False, blank=False)
    work_time_from = models.TimeField()
    work_time_to = models.TimeField()
    lab_phone = models.CharField(max_length=50, null=False, blank=False)
    lab_email = models.EmailField(max_length=50, null=False, blank=False)

    def __str__(self):
        return f"{self.lab_name} - {self.lab_country}"

    class Meta:
        verbose_name = 'Lab'
        verbose_name_plural = 'Labs'


class Tests(models.Model):
    test_name = models.CharField(max_length=50, null=False, blank=False,name='test_name')


def __str__(self):
    return f"{self.test_name}"


class Lab_Tests(models.Model):
    lab_id = models.ForeignKey(Labs, on_delete=models.CASCADE)
    Test_id = models.ForeignKey(Tests, on_delete=models.CASCADE)


def __str__(self):
    return f"{self.lab_id} - {self.Test_id}"


class Lab_appointment(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patient')
    lab_test = models.ForeignKey(Lab_Tests, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.lab_test} - {self.patient}"

    class Meta:
        verbose_name = 'lab_appointment'
        verbose_name_plural = 'lab_appointments'
        ordering = ['-created_at']
