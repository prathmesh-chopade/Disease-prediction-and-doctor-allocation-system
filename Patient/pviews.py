from django.conf import settings
from django.shortcuts import render,redirect
from .models import PatientRegistration,PatientLogin,PatientAppointment
from django.core.mail import send_mail
import pandas as pd
from Doctor.models import DoctorRegistration
import datetime
from django.http import HttpResponse
import json

# Create your views here.


def Register(request):
    if request.method=='POST':
        if  request.POST['password1']==request.POST['password2'] :
            try:
                pass1=request.POST.get('password1')
                PatientRegistration.objects.get(patientid=request.POST['userid'])
                return render(request,'PatientRegistration.html',{'error':'Userid already exists please choose another Userid '})
            except PatientRegistration.DoesNotExist:
                try:
                    PatientRegistration.objects.get(email=request.POST['email'])
                    return render(request,'PatientRegistration.html',{'error1':'Email already exists please choose another Email '})
                except PatientRegistration.DoesNotExist:
                        insert1=PatientRegistration()
                        insert1.patientid=request.POST.get('userid')
                        insert1.patientname=request.POST.get('name')
                        insert1.password=pass1
                        insert1.email=request.POST.get('email')
                        insert1.mobile=request.POST.get('mobile')
                        insert1.extranumber=request.POST.get('altmobile')
                        insert1.city=request.POST.get('city')
                        insert2=PatientLogin()
                        insert2.patientid=request.POST.get('userid')
                        insert2.email=request.POST.get('email')
                        insert2.password=pass1
                        insert2.status="active"
                        insert2.secquestion=request.POST.get('question')
                        insert2.secanswer=request.POST.get('answer')
                        insert1.save()
                        insert2.save()
                        return render(request,'PatientLogin.html',{'error1':'Your Registration is successful.......'})
        else:
            return render(request,'PatientRegistration.html',{'error':'Your passwords does not match Please enter correct Password'})


def Login(request):
    if request.method=='POST':
        try:
            obj=PatientLogin.objects.get(email=request.POST['email'])
            if obj.password==request.POST['password1'] and obj.status=="active":
                id=obj.patientid
                request.session['pid']=id
                obj=PatientRegistration.objects.get(patientid=id)
                name=obj.patientname
                list=name.split(" ")
                request.session['pnm']=list[0]
                return redirect('patienthome')
            else:
                return render(request, 'PatientLogin.html', {'error':'Authentication failed...'})
        except PatientLogin.DoesNotExist:
            return render(request, 'PatientLogin.html', {'error':'Authentication failed...'})

    
def PChangePass(request):
    userid=request.session['pid']
    pass1=request.POST.get('pass1')
    pass2=request.POST.get('pass2')
    if(pass2==request.POST.get('pass3')):
        obj=PatientLogin.objects.get(patientid=userid)
        if obj.password==pass1:
            obj.password=pass2
            obj.save()
            obj=PatientRegistration.objects.get(patientid=userid)
            obj.password=pass2
            obj.save()
            return render(request, 'PatientChangePassword.html',{'error':'Password Changed Successfully..'})
        else:
            return render(request, 'PatientChangePassword.html',{'error1':'current password is incorrect'})
    return render(request, 'PatientChangePassword.html',{'error1':'Password are not same'})


def PatientHome(request):
    object1=pd.read_csv("Files/Disease_and_their_Symptoms.csv")
    list1=list(set(object1['Symptoms']))
    list1.sort()
    list1.insert(0,"Select Symptoms")
    sys=""
    for i in list1:
        sys=sys+"&"+i
    data=""
    num=0
    return render(request,'PatientHome.html',{'symptoms':list1,'error':'enable','no':num,'error1':'hidden','initilize':data,'init':sys,'mes':'hidden','mess':'enable'})

def PatientHome2(request):
    list1=request.session['remain_symptoms']
    notice='System found more than 1 disease for your symptoms for more accuracy....'
    return render(request, 'PatientHome.html',{'symptoms':list1,'error':'hidden','error1':'enable','notice':notice})

def SelectDropdownElement(request):
    symptom=request.POST.get('sym')
    count=int(request.POST.get('count'))
    sy=request.POST.get('sy')
    list2=[]
    value=5
    sy=sy[1:]
    list8=sy.split("&")
    symptom=symptom[1:]
    list6=symptom.split("&")
    if "Select Symptoms" in list6:
        list6.remove('Select Symptoms') 
    for i in list8:
        if i=="none":
            value=1
    if(value==5):
        list4=list(set(list6)-set(list8))
        list4.sort()
        list2=[]
        for i in list4:
            data={}
            data["Symptom"]=i
            list2.append(data)
        return HttpResponse(json.dumps(list2)) 
    else:
        return HttpResponse("Yes")


def DiseasePrediction(request):
    number=request.POST.get('number')
    niki=request.POST.get('symptom')
    symptom=niki[1:]
    list1=symptom.split("&")
    if "none" in list1:
        list1.remove('none')
    sysm=""
    for i in list1:
        sysm=sysm+"&"+i
    dir1={}
    object1=pd.read_csv("Files/Disease_and_their_Symptoms.csv")
    for sym in list1:
        list2=[]
        object2=object1['Diseases'][object1['Symptoms']==sym]
        list2=object2.tolist()
        for element in list2:
            if element not in dir1:
                dir1[element]=1
            else:
                dir1[element]+=1
    predicted_disease=max(zip(dir1.values(),dir1.keys()))
    no=predicted_disease[0]
    list4=[]
    for x,y in dir1.items():
        if y==no:
            list4.append(x)
    length=len(list4)
    list7=[]
    print(list4)
    print(dir1)
    if (length>1):
        for i in list4:
            data=object1['Symptoms'][object1['Diseases']==i]
            list2=data.tolist()
            list7=list7+list2
        list2=list(set(list7)-set(list1))
        sys=""
        for i in list2:
            sys=sys+"&"+i
        list2.insert(0,'Do you feel any of these ?')
        return render(request,'PatientHome.html',{'symptoms':list2,'error':'enable','no':number,'mess':'enable','error1':'hidden','mes':'enable','initilize':sysm,'init':sys,'message':'enable'})
    else:
        disease=list4[0]
        object1=pd.read_csv("Files/Spe_disease.csv")
        data=object1['Specialization'][object1['Disease']==list4[0]].tolist()
        if len(data)>0:
            spec=data[0]
        else:
            spec="General physician"
        try:
            doctor=DoctorRegistration.objects.filter(specility=spec)
            no=len(doctor)
            request.session['dno']=no
            doc_list=[]
            doc_name=[]
            doc_id=[]
            for i in range(0,no):
                doctors={}
                doctors['Name']=doctor[i].doctorname
                doc_name.append(doctor[i].doctorname)
                doctors['Education']=doctor[i].education
                doctors['Speciality']=doctor[i].specility
                doctors['Experience']=doctor[i].experience
                doctors['Rating']=doctor[i].rating
                doctors['Hospital Address']=doctor[i].address
                doctors['Email']=doctor[i].email
                doctors['Mobile']=doctor[i].mobile
                doc_list.append(doctors)
                patientid=request.session['pid']
                insert1=PatientAppointment()
                obj=PatientRegistration.objects.get(patientid=patientid)
                insert1.patientid=patientid
                insert1.patientname=obj.patientname
                print(disease)
                insert1.pre_disease=disease
                insert1.doctorid=doctor[i].doctorid
                insert1.symptoms=list1
                insert1.pre_doctor=doctor[i].doctorname
                date1=datetime.date.today()
                insert1.date=date1
                insert1.appointmentstatus="No"
                insert1.save()
                data=insert1.pk 
                dir9={}
                dir9[data]=doctor[i].doctorname
                doc_name.append(dir9)

            return render(request,'PatientHome.html',{'error':'hidden','disease':disease,'mess':'hidden','error1':'enable','mes':'hidden','doc_list':doc_list,'doctorappoint':doc_name})
        except DoctorRegistration.DoesNotExist:
            return render(request,'PatientHome.html',{'Disease':disease,'error':'hidden','error1':'enable','doctor1':'Doctor is not available'})


def DiseaseDetail(request):
    disease=request.GET.get('disease')
    file=open("Files/"+disease+".txt","r")
    file_content=file.read()
    file.close()
    context={'file_content':file_content,'error':'hidden'}
    return render(request,'PatientHome.html',context)



def ForgotPassword(request):
    if request.method=="POST":
        try:
            pass1=request.POST.get('password1')
            pass2=request.POST.get('password2')
            if(pass1==pass2):
                email=request.POST.get('email')
                sque=request.POST.get('squestion')
                sans=request.POST.get('sanswer')
                object1=PatientLogin.objects.get(email=email)
                if(object1.secquestion==sque and object1.secanswer==sans):
                    object1.password=pass1
                    object1.save()
                    return render(request, 'PatientForgotPassword.html',{'error':'Password changed successfully please login'})
                else:
                    return render(request, 'PatientForgotPassword.html',{'error1':'Invalid security question or answer'})
            else:
                return render(request, 'PatientForgotPassword.html',{'error1':'Password does not match'})
        except PatientLogin.DoesNotExist:
            return render(request, 'PatientForgotPassword.html',{'error1':'error'})


def TakeAppointment(request):
    if request.method=='POST':
        try:
            docname=request.POST.get('doc')
            appdate=request.POST.get('date')
            l=[]
            for i in appdate:
	            l=appdate.strip().split('/')
            d=l[2]+"-"+l[0]+"-"+l[1]
            a=datetime.datetime.strptime(d, "%Y-%m-%d").date()
            obj=PatientAppointment.objects.get(id=docname)
            obj.appointdate=a
            obj.appointmentstatus='Yes'
            obj.save()
            return HttpResponse("Your appointment is successful...!")
        except PatientAppointment.DoesNotExist:
            return render(request, 'PatientHome.html',{'message':'error...','error1':'hidden','error':'enable'})


def PatientActivity(request):
    datalist=[]
    object1=PatientAppointment.objects.filter(patientid=request.session['pid'])
    for i in object1:
        did=i.doctorid
        list1=[]
        counter=0
        string=""
        date=str(i.date)
        list1.append(date)
        list1.append(i.pre_disease)
        sym=i.symptoms
        sym=sym[1:-1]
        l3=sym.split(',')
        list1.append(i.pre_doctor)
        obj1=DoctorRegistration.objects.get(doctorid=did)
        list1.append(obj1.address)
        list1.append(obj1.email)
        list1.append(obj1.mobile)
        for j in l3:
            counter+=1
            if j==l3[0]:
                j=j[1:-1]
                string=str(counter) + " )"+j
                list1.append(string)
            else:
                j=j[2:-1]
                string=str(counter) + " ) "+j
                list1.append(string)
        datalist.append(list1)
    print(datalist)
    return render(request, 'PatientActivity.html',{'datalist':datalist})

def PatientAppointments(request):
    datalist=[]
    datalist2=[]
    listcount=[]
    obj=PatientAppointment.objects.filter(patientid=request.session['pid'])
    for i in obj:
        if str(i.appointmentstatus)=='Yes':
            list1=[]
            list5=[]
            list1.append(str(i.date))
            list1.append(i.pre_disease)
            # sym=i.symptoms
            # l=sym.replace('[','')
            # l1=l.replace(']','')
            # l2=l1.replace("'","")
            # l3=l2.strip().split(',')
            # for j in l3:
            #     list1.append(j)
            list1.append(i.pre_doctor)
            did=i.doctorid
            obj1=DoctorRegistration.objects.get(doctorid=did)
            list1.append(obj1.address)
            list1.append(obj1.email)
            list1.append(obj1.mobile)
            list1.append(i.appointmentstatus)
            datalist.append(list1)
            # datalist2.append(list5)
            # for i in range(0,len(datalist2)):
            #     listcount.append(i)
    print(datalist)
    return render(request, 'PatientAppointments.html',{'datalist':datalist})
