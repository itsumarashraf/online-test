from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from .models import paymentdetail
from users.models import *
from django.http import Http404

from users.views import *
import razorpay
from django.views.decorators.csrf import csrf_exempt

def checkout(request,aptid):
    new=appointment.objects.get(appointmentno=aptid)
    amt=orderamount.objects.get(appointment__appointmentno=aptid)
    s=paymentdetail.objects.filter(appointment__appointmentno=aptid).first()
    if s:
        if s.paymentid:
            raise Http404("Page does not exist")

        else:
            if request.method == 'POST':
                result=request.POST.get('pay')
                if result == 'cod':
                    ramount= amt.amount
                    pay=paymentdetail.objects.filter(appointment__appointmentno=aptid).update(appointment=new,amount=0,amountdue=ramount,orderid='NA',paymentid='NA',codstatus=True)
                    return render(request,'payments/codsuccess.html',{'aptid':aptid, 'new':new,'amt':amt})
            else:

                # update already existing order with new payment id
                ramount= amt.amount * 100
                client= razorpay.Client(auth =("rzp_test_FO6OeouYXvVlwh", "DG2Es6WXrUr6DUfX76sioXXE"))
                payment = client.order.create({'amount':ramount, 'currency':'INR', 'payment_capture':'1'})
                amount=payment['amount'] /100
                pay =paymentdetail.objects.filter(appointment__appointmentno=aptid).update(appointment=new,amount=amount,orderid=payment['id'])
                
                # print('updated'+ aptid, payment)
                return render(request,'payments/checkout.html',{'aptid':aptid, 'new':new,'amt':amt,'payment':payment})
    else:
        # check payment mode
        # if payment mode is cod
        # update payment method as cod and return
        if request.method == 'POST':
            result=request.POST.get('pay')
            aptid=request.POST.get('id')
            if result == 'cod':
                # print('method is cod')
                ramount= amt.amount
                pay=paymentdetail(appointment=new,amountdue=ramount,orderid='NA',paymentid='NA',codstatus=True)
                pay.save()

                # Sending email after successfull payment
                u=enduser.objects.get(appointment__appointmentno=aptid)    
                sub='Your order was Successfull placed as COD '
                msg= render_to_string('email/emailcodsuccess.html',{'user':u,'aptid':aptid})
                sendemail(u,sub,msg)
                #---------------------------------------------------------------------------#

                return render(request,'payments/codsuccess.html',{'aptid':aptid, 'new':new,'amt':amt})

            elif result == 'online':
                # print('method is online')
                # payment method is online
                # create new instance of online payment id and return    

                ramount= amt.amount * 100
                client= razorpay.Client(auth =("rzp_test_FO6OeouYXvVlwh", "DG2Es6WXrUr6DUfX76sioXXE"))
                payment = client.order.create({'amount':ramount, 'currency':'INR', 'payment_capture':'1'})
                amount=payment['amount'] /100
                pay =paymentdetail(appointment=new,amount=amount,orderid=payment['id'])
                pay.save()
                return render(request,'payments/checkout.html',{'aptid':aptid, 'new':new,'amt':amt,'payment':payment})

    return render(request,'payments/checkout.html',{'aptid':aptid, 'new':new,'amt':amt})


@csrf_exempt
def success(request):
    if request.method == "POST":
        razorpay= request.POST
        apt=request.POST.get('getid')
        postpaymentid=razorpay['razorpay_payment_id']
        # print(postpaymentid)
        if postpaymentid:
            postorderid= razorpay['razorpay_order_id']
            # print(postorderid)
            user=paymentdetail.objects.get(orderid=postorderid)
            user.paymentstatus=True
            user.paymentid=postpaymentid 
            user.save()

            # Sending email after successfull payment
            u=enduser.objects.get(appointment__appointmentno=apt)    
            sub='Your Payment was Successfull'
            msg= render_to_string('email/emailpaymentsuccess.html',{'user':u,'aptid':apt})
            sendemail(u,sub,msg)
            #---------------------------------------------------------------------------#
            sendsms(msg,u)
            return render(request,'payments/success.html',{'apt':apt})
        else:
            return HttpResponse("Payment Failed")    
    return render(request,'payments/success.html',{'apt':apt})

