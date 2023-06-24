from django.db import models
from django.conf import settings
import datetime

# Create your models here.

Category_CHOICES = (
    ('Dentist', 'Dentist'),
    ('Cardiologist', 'Cardiologist'),
    ('Neurologist', 'Neurologist'),
    ('Gynecologist', 'Gynecologist'),
    ('Pediatrician', 'Pediatrician'),
    ('Psychiatrist', 'Psychiatrist'),
    ('Dermatologist', 'Dermatologist'),
    ('Ophthalmologist', 'Ophthalmologist'),
    ('Otolaryngologist', 'Otolaryngologist'),
    ('Urologist', 'Urologist'),
    ('Orthopedist', 'Orthopedist'),
    ('Radiologist', 'Radiologist'),
    ('Anesthesiologist', 'Anesthesiologist'),
    ('Oncologist', 'Oncologist'),
    ('Gastroenterologist', 'Gastroenterologist'),
    ('Rheumatologist', 'Rheumatologist'),
    ('Allergist', 'Allergist'),
)


class Doctor_Category(models.Model):
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=Category_CHOICES, null=False, blank=False)

    # def __str__(self):
    #     return f"{self.doctor} - {self.category}"

    class Meta:
        verbose_name = 'Doctor Category'
        verbose_name_plural = 'Doctor Categories'


class Appointment(models.Model):
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doctor_appointments')
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patient_appointments')
    date = models.DateField()
    time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.doctor} - {self.patient}"

    class Meta:
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'
        ordering = ['-created_at']


class Dates(models.Model):
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doctor_date')
    date = models.DateField()
    time_from = models.TimeField()
    time_to = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.doctor} - {self.date}"

    def change_availability(self):
        self.availability = False
