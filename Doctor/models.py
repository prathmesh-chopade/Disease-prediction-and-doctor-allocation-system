from django.db import models

# Create your models here.
class DoctorRegistration(models.Model):
    doctorid=models.CharField(max_length=100,primary_key=True)
    doctorname=models.CharField(max_length=100)
    mobile=models.CharField(max_length=10,unique=True)
    email=models.EmailField(unique=True)
    address=models.CharField(max_length=1000)
    education=models.CharField(max_length=100)
    experience=models.CharField(max_length=100)
    specility=models.CharField(max_length=100)
    rating=models.FloatField()
    image=models.FileField()
    city=models.CharField(max_length=50)

    def __str__(self):
        return self.doctorid
    
class DoctorLogin(models.Model):
    doctorid=models.CharField(max_length=100,primary_key=True)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=100)
    status=models.CharField(max_length=100)
    secquestion=models.CharField(max_length=200)
    secanswer=models.CharField(max_length=100)

    def __str__(self):
        return self.doctorid

class DoctorActivity(models.Model):
    date=models.DateField()
    patientname=models.CharField(max_length=100)
    disease=models.CharField(max_length=100)

    def __str__(self):
        return self.patientname

    