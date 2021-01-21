from django.contrib import admin
from users.models import enduser, appointment, appointmentstatus,testchoice,orderamount
# from adminside.models import test


# Register your models here.
# admin.site.register(test)
admin.site.register(appointment)
admin.site.register(enduser)
admin.site.register(appointmentstatus)
admin.site.register(testchoice)
admin.site.register(orderamount)
