from django.contrib import admin
from django.urls import path,include
from users import views
from .views import testinfo, testdetails
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("userside/", views.userside,name='userside'),
    path("userside/view/", views.testdetails,name='viewtestdetails'),
    path("userside/view/test-info/<int:test_id>", views.testinfo),
    path("userside/appointments/", views.appointments, name='appointments'),
    path("userside/appointments/apt-success",views.aptsuccess, name='aptsuccess'),
    path("userlogin/",views.userlogin, name='userlogin'),
    path("userregister/",views.userregister, name='userregister'),
    path("userlogout/",views.userlogout, name='userlogout'),
    path("userside/appointment-history/", views.appointmenthistory, name='apt-history'),
    path("userside/appointment-history/<int:aptid>", views.viewappointment, name='view-apt'),
    path("newappointments/", views.newappointments, name='newappointments'),
    path("appointmentdetails/<int:apt_id>",views.appointmentdetail,name='appointmentdetails'),
    path("rejected-apts/", views.rejectedappointments, name='rejectedapts'),
    path("approved-apts/", views.approvedappointments, name='approvedapts'),
    path("approved-apts/viewapproved/<int:aptid>/", views.viewapproved, name='viewapproved'),
    path("usercanceled-apts/", views.canceledappointments, name='usercanceled'),
    path("userside/appointment-history/", include('payment.urls')),
    path("userside/appointment-history/<int:aptid>/", include('ordertracking.urls')),
    path("approved-apts/viewapproved/<int:aptid>/", include('ordertracking.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)