from django.contrib import admin
from .models import DoctorLogin,DoctorRegistration

admin.site.register(DoctorLogin)
admin.site.register(DoctorRegistration)