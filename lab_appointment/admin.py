from django.contrib import admin
from .models import Labs, Tests, Lab_Tests, Lab_appointment
# Register your models here.
admin.site.register(Labs)
admin.site.register(Tests)
admin.site.register(Lab_Tests)
admin.site.register(Lab_appointment)