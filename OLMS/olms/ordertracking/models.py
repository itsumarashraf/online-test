from django.db import models
from users.models import appointment
from django.utils import timezone
# Create your models here.

class trackorder(models.Model):
    appointment= models.ForeignKey(appointment, to_field='appointmentno', on_delete=models.CASCADE)
    orderstatus=models.CharField(max_length=500,default="Order Placed")
    ordertimestamp=models.DateField(auto_now_add=True)
    updatetimestamp=models.TimeField(default=timezone.now)
    

    def __str__(self): 
         return self.appointment.patientname