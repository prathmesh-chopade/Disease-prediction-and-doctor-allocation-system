
from django.contrib import admin
from django.urls import path,include
from . import first
from Patient import pviews
from Doctor import dviews
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', first.HomePage, name='home'),
    path('doctorhome/patienttreated/',dviews.TreatedPatient,name="patienttreated"),
    path('doctorhome/patientdelete/',dviews.PatientDelete,name="patientdelete"),
    path('plogin/', first.PatientLoginPage, name='patientlogin'),
    path('dlogin/', first.DoctorLoginPage, name='doctorlogin'),
    path('patientregistration/', first.PatientRegistrationPage, name='patientreg'),
    path('doctorregistration/', first.DoctorRegistrationPage, name='doctorreg'),
    path('doctorreg/', dviews.Register, name='dreg'),
    path('doctorreg2/', dviews.Register2, name='exdreg'),
    path('patientreg/', pviews.Register, name='preg'),
    path('doctorHome/', dviews.Login, name='dprof'),
    path('patientHome/', pviews.Login, name='pprof'),
    path('patientforgotpassword/',first.PForgot, name='patientforgot'),
    path('doctorforgotpassword/',first.DForgot, name='doctorforgot'),
    # path('patientmail/',pviews.Mail,name='patientmail'),
    # path('doctormail/',dviews.Mail,name='doctormail'),
    path('doctorchangepassword/',first.DoctorChangePassword, name='doctorchangepassword'),
    path('patientchangepassword/',first.PatientChangePassword, name='patientchangepassword'),
    path('doctoractivity/',dviews.DoctorActivity, name='doctoractivity'),
    path('patientactivity/',pviews.PatientActivity, name='patientactivity'),
    path('doctorprofile/', dviews.DoctorProfile,name='doctorprofile'),
    path('patientprofile/', first.PatientProfile,name='patientprofile'),
    path('doctorhome/',dviews.DoctorHome,name='doctorhome'),
    path('doctorhome2/',dviews.DoctorHome2,name='doctorhome2'),
    path('patienthome/',pviews.PatientHome,name='patienthome'),
    path('patienthome2/',pviews.PatientHome2,name='patienthome2'),
    path('dchangepass/', dviews.DChangePass, name='dchangepass'),
    path('pchangepass/', pviews.PChangePass, name='pchangepass'),
    # path('doctorimage/',dviews.DImage,name='dimage'),
    path('predictdisease/',pviews.DiseasePrediction, name='predictdisease'),
    path('showdiseasedetail/',pviews.DiseaseDetail),
    path('patientforgotpassword1/',pviews.ForgotPassword,name='patientforgotpassword'),
    path('doctorforgotpassword2/',dviews.ForgotPassword,name='doctorforgotpassword'),
    path('doctoradddisease/',first.AddDisease,name='doctoradddisease'),
    path('adddisease/',dviews.AddDisease,name='adddisease'),
    path('takeappointment/',pviews.TakeAppointment,name='takeappointment'),
    path('patientappointment/',pviews.PatientAppointments,name='patientappointment'),
    path('Dropdownlist/',pviews.SelectDropdownElement),
    
 ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)