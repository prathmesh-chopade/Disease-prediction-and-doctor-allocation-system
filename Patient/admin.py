from django.contrib import admin
from .models import PatientLogin,PatientRegistration,Review,PatientAppointment

admin.site.register(PatientLogin)
admin.site.register(PatientRegistration)
admin.site.register(Review)
admin.site.register(PatientAppointment)