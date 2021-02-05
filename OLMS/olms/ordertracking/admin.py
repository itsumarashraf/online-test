from django.contrib import admin
from .models import trackorder
# Register your models here.


class trackorderadmin(admin.ModelAdmin): 
    list_display = ('appointment', 'orderstatus')
    
    
admin.site.register(trackorder, trackorderadmin)