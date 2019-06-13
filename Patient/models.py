from django.db import models

# Create your models here.
class PatientLogin(models.Model):
    patientid=models.CharField(max_length=100,primary_key=True)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=100)
    status=models.CharField(max_length=100)
    secquestion=models.CharField(max_length=200)
    secanswer=models.CharField(max_length=100)

    def __str__(self):
        return self.patientid

class PatientRegistration(models.Model):
    patientid=models.CharField(max_length=100,primary_key=True)
    patientname=models.CharField(max_length=100)
    mobile=models.CharField(max_length=10)
    email=models.EmailField(unique=True)
    extranumber=models.CharField(max_length=10)
    city=models.CharField(max_length=50)

    def __str__(self):
        return self.patientid


class Review(models.Model):
    patientid=models.CharField(max_length=100)
    doctorid=models.CharField(max_length=100)
    star=models.FloatField()

    def __str__(self):
        return self.patientid


class PatientAppointment(models.Model):
    patientid=models.CharField(max_length=100)
    patientname=models.CharField(max_length=100)
    pre_disease=models.CharField(max_length=100)
    doctorid=models.CharField(max_length=100)
    symptoms=models.CharField(max_length=1000)
    pre_doctor=models.CharField(max_length=100)
    date=models.DateField(blank=True, null=True)
    appointdate=models.DateField(blank=True, null=True)
    appointmentstatus=models.CharField(max_length=100)


    def __str__(self):
        return self.patientid
