from django.db import models
from users.models import appointment
# Create your models here.
 
class paymentdetail(models.Model):
    appointment=models.ForeignKey(appointment,on_delete=models.CASCADE)
    amount=models.IntegerField(default=0)
    amountdue=models.IntegerField(default=0)
    orderid=models.CharField(max_length=100)
    paymentid=models.CharField(max_length=100)
    paymentstatus=models.BooleanField(default=False)
    codstatus=models.BooleanField(default=False)
    
    


