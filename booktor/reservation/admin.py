from django.contrib import admin
from .models import Doctor_Category,Appointment,Dates
# Register your models here.
admin.site.register(Doctor_Category)
admin.site.register(Appointment)
admin.site.register(Dates)
