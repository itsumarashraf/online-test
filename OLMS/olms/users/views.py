from django.shortcuts import render, HttpResponse,redirect
from adminside.models import test
from users.models import appointment,enduser, appointmentstatus,testchoice,orderamount
from payment.models import paymentdetail
from django.contrib.auth.decorators import login_required
import random
from django.contrib.sessions.models import Session
from users.authmiddleware import userlogin_auth 
from django.utils.decorators import method_decorator
from ordertracking.views import tracking,track
from django.http import Http404
from ordertracking.models import trackorder
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


# Create your views here.
def checkauth(request):
    if request.session.has_key('userid'):
        return True
    else:
        return False


@userlogin_auth
def userside(request):
    if request.session.has_key('userlogged'):
        if request.method=="GET":
            sea=request.GET.get('search')
            if sea:
                # print(sea)
                a=appointment.objects.filter(user_id=request.session['userid']).filter(appointmentno__iexact=sea).first()          
                if not a:
                    msg='No Records Found'
                    return render(request,'userside.html',{'msg':msg})
                else:
                    r=a              
                # print(r.email)
                return render(request,'userside.html',{'r':r})

        return render(request,'userside.html')
    else:
        return redirect('userlogin')
     


@userlogin_auth
def testdetails(request):
    test_details = test.objects.all()
    return render(request,'view-test-details.html',{'testitems':test_details})

def testinfo(request, test_id):
    if checkauth(request) == True:
        test_info = test.objects.get(id=test_id)
        return render(request, 'test-info.html',{'info':test_info})
    return redirect('userlogin')

@userlogin_auth
def appointments(request):
    testitem = test.objects.all()
    return render(request, 'appointments.html',{'testitems':testitem})


# function to generate random appointment id's
def random_aptno():
    return str(random.randint(10000, 99999))



def aptsuccess(request):
    if request.method=="POST":
        userid=request.POST.get('loggeduserid')
        who=enduser.objects.get(id=userid)
        user= who
        aptid = random_aptno()
        name=request.POST.get('patientname')
        address=request.POST.get('address')
        gender=request.POST.get('gender')
        dob=request.POST.get('dob')
        cell=request.POST.get('phone')
        mail=request.POST.get('email')
        ticket=request.FILES.get("file")
        
        document = appointment(user_id=user,appointmentno=aptid,patientname=name,address=address,gender=gender,dateofbirth=dob,mobile=cell,email=mail,prescription=ticket)
        document.save()
        apt= appointmentstatus(appointment=document)
        apt.save()

        # gets a list of test name and price from the checkboxes and saves them in testchoice model 
        choice=request.POST.getlist('choice[]')
        price=request.POST.getlist('price[]')

        

        if choice:
            for val,val2 in zip(choice,price):
                h=testchoice(appointment=document,tname=val,price=val2)
                h.save() 
        # -----------------------------------------------------------------------------------------
        
        # calulate the total amount and save in orderamount model #
        total = calculateamount(price)
        
        amt=orderamount(appointment=document,amount=total)
        amt.save()
        # -----------------------------------------------------------------------
        
        tracking(document)  #updates tracking details with refrence to current appointment
        sub= 'You Order was Placed.'
        msg= render_to_string('email/emailtemplate.html',{'user':user,'aptid':aptid})
        sendemail(who,sub,msg)
    return render(request,'appointment-success.html',{'who':who,'name':name,'aptid':aptid})




def calculateamount(price):
    s=0
    for val in price:
        s=s+int(val)
    return s


def sendemail(who,sub,msg):
    send_mail(sub,msg,settings.EMAIL_HOST_USER,[who.email],fail_silently=False,)




def appointmenthistory(request):
    if checkauth(request)==True:
        userid=request.session['userid']
        history=appointment.objects.filter(user_id=userid)
        status=appointmentstatus.objects.filter(appointment__user_id=userid)
        mylist = zip(history,status)

        return render(request,'appointment-history.html',{'context':mylist})
    return redirect('userlogin')


def viewappointment(request,aptid):
    if checkauth(request)==True:
        val=appointmentstatus.objects.get(appointment__appointmentno=aptid)
        if val.status !='NEW':
            enable='disabled'
        else:
            enable=""

            if request.method == 'POST':
                appointmentstatus.objects.filter(appointment__appointmentno=aptid).update(status='Cancel', comment='You have Canceled This Order')

        aptdetail=appointment.objects.get(appointmentno=aptid)
        if aptdetail:
            status=appointmentstatus.objects.get(appointment__appointmentno=aptid)
            new=testchoice.objects.filter(appointment__appointmentno=aptid)
            amt=orderamount.objects.get(appointment=aptid)
            # print(aptid)
            s=paymentdetail.objects.filter(appointment__appointmentno=aptid).first()
            
            if aptdetail.prescription:
                if aptdetail.report:
                    url=aptdetail.prescription.url
                    text="Download Prescription"
                    urll=aptdetail.report.url
                    textt="Download Report"
                else:
                    url=aptdetail.prescription.url
                    text="Download Prescription"
                    urll=aptdetail.report
                    textt=""               
            elif aptdetail.report:
                    url=aptdetail.prescription
                    text=""
                    urll=aptdetail.report.url
                    textt="Download Report" 
            else:
                    url=aptdetail.prescription
                    text=""
                    urll=aptdetail.report
                    textt=""

            if s:
                if s.paymentid or s.codstatus==True:
                    payenable='disabled'
                else:
                    payenable=''
                return render(request,'view-appointment.html',{'detail':aptdetail, 'status':status,'amt':amt, 'new':new, 'enable':enable,'s':s,'payenable':payenable,'url':url,'urll':urll,'text':text,'textt':textt})
            return render(request,'view-appointment.html',{'detail':aptdetail, 'status':status,'amt':amt, 'new':new, 'enable':enable,'s':s,'url':url,'urll':urll,'text':text,'textt':textt})
        raise Http404('Page does not exist')
    return redirect('userlogin')


def userlogin(request):
        if request.method == "POST":
            name = request.POST.get('username')
            password = request.POST.get('password')
            user = enduser.objects.filter(username=name,password=password)
            if user:
                userdetails =enduser.objects.get(username=name)
                name=userdetails.firstname +" "+userdetails.lastname
                email=userdetails.email
                id=userdetails.id
                request.session['userid']=id
                request.session['userlogged']=name
                request.session['useremail']=email
                # userdetail=enduser.objects.get(username=name)
                # user=userdetail.firstname +" "+ userdetail.lastname
                # email=userdetail.email
                # request.session['userin']=user
                # request.session['userin_email']=email
                # return render(request,'userside.html',{'name':user,'email':email})
                return redirect('userside')
            else:
                return HttpResponse('email or password wrong')

        return render(request,'userreg/userlogin.html')
                
                    
    
def userregister(request):
    if request.method == 'POST':
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        uname=request.POST.get('username')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        password=request.POST.get('password')
        userreg = enduser(firstname=fname,lastname=lname,username=uname,phone=phone,email=email,password=password)
        userreg.save()
    return render(request,'userreg/userregister.html')

def userlogout(request):
    del request.session['userlogged']
    del request.session['useremail']
    del request.session['userid']
    return redirect('userlogin')


def newappointments(request):
    # new=appointment.objects.all()
    new=appointment.objects.filter(appointmentstatus__status='NEW')
    return render(request,'new-appointments.html',{'newapt':new})

def appointmentdetail(request,apt_id):
    if request.method == 'POST':
        status=request.POST.get('mark')
        comment=request.POST.get('comment')
        appointmentstatus.objects.filter(appointment__id=apt_id).update(status=status,comment=comment)
    
    aptdetail=appointment.objects.get(id=apt_id)
    status=appointmentstatus.objects.get(appointment__id=apt_id)
    new=testchoice.objects.filter(appointment=apt_id)
    amt=orderamount.objects.get(appointment__id=apt_id)
    pay=paymentdetail.objects.filter(appointment__id=apt_id).first()
    # print(pay.paymentstatus)
    if aptdetail.prescription:
        url=aptdetail.prescription.url
        text="Download"
    else:
        url=aptdetail.prescription
        text=""
    return render(request, 'appointment-details.html',{'detail':aptdetail, 'new':new,'amt':amt, 'status':status, 'url':url, 'text':text,'pay':pay})
    
def approvedappointments(request):
    if checkauth(request)==True:
        new=appointment.objects.filter(appointmentstatus__status='Approve')
        return render(request, 'approved-apts.html',{'newapt':new})
    return redirect('userlogin')

def rejectedappointments(request):
    if checkauth(request)==True:
        new=appointment.objects.filter(appointmentstatus__status='Reject')
        return render(request, 'rejected-apts.html',{'newapt':new})
    return redirect('userlogin')

def canceledappointments(request):
    if checkauth(request)==True:
        new=appointment.objects.filter(appointmentstatus__status='Cancel')
        return render(request,'usercanceled-apts.html',{'newapt':new})
    return redirect('userlogin')

def viewapproved(request, aptid):
    if checkauth(request)==True:
        if request.method == 'POST':
            report=request.FILES.get('file')
            aptdetail=appointment.objects.get(appointmentno=aptid)
            aptdetail.report=report
            aptdetail.save()
            
            # Sending email after successfull payment
            u=enduser.objects.get(appointment__appointmentno=aptid)    
            sub='Your Report has been Generated '
            msg= render_to_string('email/emailreportgen.html',{'user':u,'aptid':aptdetail})
            sendemail(u,sub,msg)
            #---------------------------------------------------------------------------#

        aptdetail=appointment.objects.get(appointmentno=aptid)
        status=appointmentstatus.objects.get(appointment__appointmentno=aptid)
        new=testchoice.objects.filter(appointment__appointmentno=aptid)
        amt=orderamount.objects.get(appointment__appointmentno=aptid)
        pay=paymentdetail.objects.filter(appointment__appointmentno=aptid).first()
        item=trackorder.objects.filter(appointment=aptid)
        # print(pay.paymentstatus)
        if aptdetail.prescription:
            if aptdetail.report:
                url=aptdetail.prescription.url
                text="Download Prescription"
                urll=aptdetail.report.url
                textt="Download Report"
            else:
                url=aptdetail.prescription.url
                text="Download Prescription"
                urll=aptdetail.report
                textt=""               
        elif aptdetail.report:
                url=aptdetail.prescription
                text=""
                urll=aptdetail.report.url
                textt="Download Report" 
        else:
                url=aptdetail.prescription
                text=""
                urll=aptdetail.report
                textt="" 


        return render(request, 'viewapproved.html',{'detail':aptdetail, 'new':new,'amt':amt, 'status':status, 'url':url,'urll':urll,'textt':textt, 'text':text,'pay':pay,'item':item})
    return redirect('userlogin')