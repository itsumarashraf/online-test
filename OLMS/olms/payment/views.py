from django.shortcuts import render,HttpResponse
from .models import paymentdetail
from users.models import *
from users.views import *
import razorpay
from django.views.decorators.csrf import csrf_exempt

def checkout(request,aptid):
    new=appointment.objects.get(appointmentno=aptid)
    amt=orderamount.objects.get(appointment__appointmentno=aptid)

    if request.method == 'POST':
        ramount= amt.amount * 100
        client= razorpay.Client(auth =("rzp_test_FO6OeouYXvVlwh", "DG2Es6WXrUr6DUfX76sioXXE"))
        payment = client.order.create({'amount':ramount, 'currency':'INR', 'payment_capture':'1'})
        amount=payment['amount'] /100
        pay =paymentdetail(appointment=new,amount=amount,orderid=payment['id'])
        pay.save()
        print(payment)
        return render(request,'payments/checkout.html',{'aptid':aptid, 'new':new,'amt':amt,'payment':payment})

    
    
    return render(request,'payments/checkout.html',{'aptid':aptid, 'new':new,'amt':amt})


@csrf_exempt
def success(request):
    if request.method == "POST":
        razorpay= request.POST
        postpaymentid=razorpay['razorpay_payment_id']
        print(postpaymentid)
        if postpaymentid:
            postorderid= razorpay['razorpay_order_id']
            print(postorderid)
            user=paymentdetail.objects.get(orderid=postorderid)
            user.paymentstatus=True
            user.paymentid=postpaymentid 
            user.save()
    
    return render(request,'payments/success.html')