from django.shortcuts import render, HttpResponse
from datetime import datetime
from main.models import Messages
from django.contrib import messages
# Create your views here.

def index(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email =request.POST.get('email')
        message =request.POST.get('message')

        contact = Messages(name=name, email=email, message=message, date=datetime.today())
        contact.save()
        messages.success(request,'Your Message has been sent!')
    return render(request,'index.html')