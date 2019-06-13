from django.shortcuts import render

def HomePage(request):
    return render(request, 'Home.html')

def PatientLoginPage(request):
    return render(request, 'PatientLogin.html')

def DoctorLoginPage(request):
    return render(request, 'DoctorLogin.html')

def PatientRegistrationPage(request):
    return render(request, 'PatientRegistration.html')

def DoctorRegistrationPage(request):
    return render(request, 'DoctorRegistration.html')

def DForgot(request):
    return render(request,'DoctorForgotPassword.html')

def PForgot(request):
    return render(request,'PatientForgotPassword.html')

def DoctorChangePassword(request):
    return render(request, 'DoctorChangePassword.html')

def PatientChangePassword(request):
    return render(request, 'PatientChangePassword.html')

def PatientProfile(request):
    return render(request, 'PatientProfile.html')

def Register(request):
    return render(request, 'DoctorRegistration2.html')

def AddDisease(request):
    return render(request, 'AddDiseaseandSymptom.html')

