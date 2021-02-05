from django.shortcuts import render,HttpResponse,redirect
from users import views
from users.models import appointment
from .models import trackorder
from django.http import Http404

# Create your views here.

def tracking(document):
    track=trackorder(appointment=document)
    track.save()

def track(request,aptid):
    if request.session.has_key('userid'):
        item=trackorder.objects.filter(appointment=aptid)
        details=appointment.objects.get(appointmentno=aptid)
        return render(request,'ordertracking/track.html',{'item':item,'details':details})
    raise Http404('Page Does not Exist')

def updatetrack(request,aptid):
    if request.user.id:
        if request.method == 'POST':
            print('hello this is update track function',aptid)
            status=request.POST.get('comment')
            details=appointment.objects.get(appointmentno=aptid)
            item=trackorder(appointment=details,orderstatus=status)
            item.save()
        return redirect('viewapproved',aptid)
    raise Http404('Page not found')