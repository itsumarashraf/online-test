from django.db import models
import random
from django.utils import timezone
from datetime import date


# Create your models here.




class enduser(models.Model):
    firstname = models.CharField(max_length=40)
    lastname = models.CharField(max_length=20)
    username = models.CharField(max_length=30, unique=True)
    email=models.CharField(max_length=50, unique=True)
    phone = models.IntegerField(unique=True)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.firstname


class appointment(models.Model):
    user_id = models.ForeignKey(enduser,on_delete=models.CASCADE)
    appointmentno = models.CharField(max_length=100)
    patientname =models.CharField(max_length=30)
    gender = models.CharField(max_length=10)
    address= models.CharField(max_length=200, default='NA')
    dateofbirth = models.DateField()
    mobile = models.IntegerField(unique=True)
    email= models.CharField(max_length=100)
    appointmentdate = models.DateField(default=date.today)
    appointmenttime = models.DateTimeField(default=timezone.now)
    prescription= models.FileField(blank=True, null=True)
    

    def __str__(self):
        return self.patientname

class appointmentstatus(models.Model):
    appointment = models.ForeignKey(appointment, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default='NEW')
    comment = models.CharField(max_length=100, default='Yet to Review')

    def __str__(self):
        return self.status


class testchoice(models.Model):
    appointment=models.ForeignKey(appointment, on_delete=models.CASCADE)
    tname=models.CharField(max_length=50)
    price=models.IntegerField(default=0)

    def __str__(self):
        return self.tname


# class apt(models.Model):
#     pname=models.CharField(max_length=40)
#     tests =models.ManyToManyField(test1)

#     def __str__(self):
#         return self.pname
