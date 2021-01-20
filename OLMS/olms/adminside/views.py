from django.shortcuts import render,HttpResponse,redirect
from adminside.models import test
from django.contrib.auth.forms import UserCreationForm
from .forms import createuserform

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from users.models import appointmentstatus
# Create your views here.

@login_required(login_url='adminlogin')
def adminside(request):
    n=appointmentstatus.objects.filter(status='NEW')
    r=appointmentstatus.objects.filter(status='Reject')
    a=appointmentstatus.objects.filter(status='Approve')
    c=appointmentstatus.objects.filter(status='Cancel')
    
    return render(request,'adminside.html',{'n':len(n),'r':len(r),'a':len(a),'c':len(c)})

@login_required(login_url='adminlogin')
def addtest(request):
    if request.method == "POST":
        testname = request.POST.get('testname')
        testdetail = request.POST.get('testdetail')
        testinterp = request.POST.get('testinterp')
        price = request.POST.get('price')
        
        testdetails = test(test_title=testname, test_desc=testdetail, test_interp=testinterp, price=price)
        testdetails.save()
    return render(request,'addtest.html')

@login_required(login_url='adminlogin')
def manage(request):
    all_tests = test.objects.all()
    return render(request,'manage.html',{'testitems': all_tests})

@login_required(login_url='adminlogin')
def edittest(request, test_id):
    test_data=test.objects.get(id=test_id)
    if request.method == 'POST':
        testname = request.POST.get('testname')
        testdetail = request.POST.get('testdetail')
        testinterp = request.POST.get('testinterp')
        price = request.POST.get('price')

        test.objects.filter(id=test_id).update(test_title=testname, test_desc=testdetail, test_interp=testinterp, price=price)
    return render(request, 'edit-test.html', {'t':test_data})

def adminregister(request):
    form = createuserform()

    if request.method == 'POST':
        form = createuserform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('adminlogin')

    context = {'form':form}
    return render(request, 'registration/adminregister.html', context)
    
def adminlogin(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('adminside')

    return render(request, 'registration/adminlogin.html')

def adminlogout(request):
    logout(request)
    return redirect('adminlogin')


########### Calculate Total Tests ################################
