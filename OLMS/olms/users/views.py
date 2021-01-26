from django.shortcuts import render, HttpResponse,redirect
from adminside.models import test
from users.models import appointment,enduser, appointmentstatus,testchoice,orderamount
from payment.models import paymentdetail
from django.contrib.auth.decorators import login_required
import random
from django.contrib.sessions.models import Session
from users.authmiddleware import userlogin_auth 
from django.utils.decorators import method_decorator

# Create your views here.

@userlogin_auth
def userside(request):
    if request.session.has_key('userlogged'):
        if request.method=="GET":
            sea=request.GET.get('search')
            if sea:
                print(sea)
                a=appointment.objects.filter(user_id=request.session['userid']).filter(appointmentno__iexact=sea).first()          
                if not a:
                    msg='No Records Found'
                    return render(request,'userside.html',{'msg':msg})
                else:
                    r=a              
                print(r.email)
                return render(request,'userside.html',{'r':r})

        return render(request,'userside.html')
    else:
        return redirect('userlogin')

def search(request):
        
    return HttpResponse('this is the search result')     


@userlogin_auth
def testdetails(request):
    test_details = test.objects.all()
    return render(request,'view-test-details.html',{'testitems':test_details})

def testinfo(request, test_id):
    test_info = test.objects.get(id=test_id)
    return render(request, 'test-info.html',{'info':test_info})

@userlogin_auth
def appointments(request):
    # if request.method=="POST":
    #     userid=request.POST.get('loggeduserid')
    #     who=enduser.objects.get(id=userid)
    #     userid= who
    #     name=request.POST.get('patientname')
    #     address=request.POST.get('address')
    #     gender=request.POST.get('gender')
    #     dob=request.POST.get('dob')
    #     cell=request.POST.get('phone')
    #     mail=request.POST.get('email')
    #     ticket=request.FILES.get("file")
        
    #     document = appointment(user_id=userid,patientname=name,address=address,gender=gender,dateofbirth=dob,mobile=cell,email=mail,prescription=ticket)
    #     document.save()
    #     apt= appointmentstatus(appointment=document)
    #     apt.save()

    #     # gets a list of test name and price from the checkboxes and saves them in testchoice model 
    #     choice=request.POST.getlist('choice[]')
    #     price=request.POST.getlist('price[]')
    #     if choice:
    #         for val,val2 in zip(choice,price):
    #             h=testchoice(appointment=document,tname=val,price=val2)
    #             h.save() 
    #     # -----------------------------------------------------------------------------------------

        


    testitem = test.objects.all()
    return render(request, 'appointments.html',{'testitems':testitem})


# function to generate random appointment id's
def random_aptno():
    return str(random.randint(10000, 99999))



def aptsuccess(request):
    if request.method=="POST":
        userid=request.POST.get('loggeduserid')
        who=enduser.objects.get(id=userid)
        userid= who
        aptid = random_aptno()
        name=request.POST.get('patientname')
        address=request.POST.get('address')
        gender=request.POST.get('gender')
        dob=request.POST.get('dob')
        cell=request.POST.get('phone')
        mail=request.POST.get('email')
        ticket=request.FILES.get("file")
        
        document = appointment(user_id=userid,appointmentno=aptid,patientname=name,address=address,gender=gender,dateofbirth=dob,mobile=cell,email=mail,prescription=ticket)
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

    return render(request,'appointment-success.html',{'who':who,'name':name,'aptid':aptid})


def calculateamount(price):
    s=0
    for val in price:
        s=s+int(val)
    return s




def appointmenthistory(request,userid):
    history=appointment.objects.filter(user_id=userid)
    status=appointmentstatus.objects.filter(appointment__user_id=userid)
    mylist = zip(history,status)

    return render(request,'appointment-history.html',{'context':mylist})


def viewappointment(request,userid,aptid):
    val=appointmentstatus.objects.get(appointment__appointmentno=aptid)
    if val.status !='NEW':
        enable='disabled'
    else:
        enable=""

        if request.method == 'POST':
            appointmentstatus.objects.filter(appointment__appointmentno=aptid).update(status='Cancel', comment='You have Canceled This Order')

    aptdetail=appointment.objects.get(appointmentno=aptid)
    status=appointmentstatus.objects.get(appointment__appointmentno=aptid)
    new=testchoice.objects.filter(appointment__appointmentno=aptid)
    amt=orderamount.objects.get(appointment=aptid)
    print(aptid)
    s=paymentdetail.objects.filter(appointment__appointmentno=aptid).first()
    
    if s:
        if s.paymentid or s.codstatus==True:
            payenable='none'
        else:
            payenable='initial'
        return render(request,'view-appointment.html',{'detail':aptdetail, 'status':status,'amt':amt, 'new':new, 'enable':enable,'s':s,'payenable':payenable})
    return render(request,'view-appointment.html',{'detail':aptdetail, 'status':status,'amt':amt, 'new':new, 'enable':enable,'s':s})


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
    new=appointment.objects.filter(appointmentstatus__status='Approve')
    return render(request, 'approved-apts.html',{'newapt':new})

def rejectedappointments(request):
    new=appointment.objects.filter(appointmentstatus__status='Reject')
    return render(request, 'rejected-apts.html',{'newapt':new})

def canceledappointments(request):
    new=appointment.objects.filter(appointmentstatus__status='Cancel')
    return render(request,'usercanceled-apts.html',{'newapt':new})