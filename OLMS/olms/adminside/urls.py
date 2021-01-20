from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("adminside/", views.adminside, name='adminside'),
    path("adminside/add/", views.addtest, name='add'),
    path("adminside/manage/", views.manage, name='manage'),
    path("adminside/manage/edit-test/<int:test_id>", views.edittest), 
    path("adminlogin/", views.adminlogin, name='adminlogin'),
    path("adminregister/", views.adminregister, name='adminregister'),
    path("adminlogout/",views.adminlogout, name='adminlogout'),

]