from django.contrib.sessions.models import Session
from django.shortcuts import render, HttpResponse,redirect

def is_userin(view_func):
    def isloggedin(request, *args, **kwargs):
        if request.session.has_key('user_in'):
            userlogged=request.session['user_in']
            return render(request,'userside.html',{'ul': userlogged})
        else:
            return redirect('userlogin')
    return isloggedin