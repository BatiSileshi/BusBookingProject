from multiprocessing import context
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import get_user_model
User = get_user_model()
# from Account.models import User
from Bus_admin.models import Route, SubRouteAdmin, SubRoute, SubRouteBusAdmin
from Customer.models import Booking
from System_admin.models import BusAdmin
from .models import FinishPayment, FinishPaymentStatus, PaymentInformantion, PaymentMethod
from .forms import PaymentMethodForm, PaymentInformationForm
from django.contrib.auth.decorators import login_required, permission_required
from .decorators import for_routeadmins
# Create your views here.

@login_required(login_url='login')
@for_routeadmins

def startHome(request):
    context={}
    return render(request, 'Booker/start_home.html', context)

@login_required(login_url='login')
@for_routeadmins
def home(request, pk):
    user=User.objects.get(id=pk)
    subroute_bus_admins=user.subroutebusadmin_set.filter()
    # subroute_bus=user.subroutebusadmin.subroute_bus.all()
    subroute_admins=user.subrouteadmin_set.filter()
    context={'user':user,  'subroute_admins':subroute_admins, 'subroute_bus_admins':subroute_bus_admins}
    
    if request.user != user:
           return HttpResponse("You are not allowed here!")
    return render(request, 'Booker/home.html', context)


@login_required(login_url='login')
def bookingRequest(request, pk):
    sub_route=SubRoute.objects.get(id=pk)
    bookings=sub_route.booking_set.filter().order_by('-created') 
    finish_payment=FinishPayment.objects.filter()

    context={'sub_route':sub_route, 'bookings':bookings, 'finish_payment':finish_payment}

    return render(request, 'Booker/booking_request.html', context)

@login_required(login_url='login')
def finishPaymentStatus(request, pk):
    finishpayment=FinishPayment.objects.get(booking_id=pk)
    bookings=Booking.objects.filter()

    if request.method == 'POST':
        status=FinishPaymentStatus.objects.create(
        fnishpayment=finishpayment,
        status=request.POST['status'],
       
        )
        return redirect ('home', pk=request.user.id)
   
    context={'bookings':bookings, 'finishpayment':finishpayment}
    # if request.user != finishpayment.booking.hotel.admin: 
    #        return HttpResponse("You are not allowed here!")
    return render(request, 'Booker/paid_unpaid.html', context)



    """MANAGE PAYMENT INFORMATIONS"""
@login_required(login_url='login')
def managePaymentInformation(request, pk):
    route=Route.objects.get(id=pk)
    payment_infos=route.paymentinformation_set.all()
    
    context={'route':route, 'payment_infos':payment_infos}    
    return render(request, 'Booker/manage_payment_info.html', context)


@login_required(login_url='login')
def addPaymentMethod(request):
    form=PaymentMethodForm()
    
    if request.method=='POST':
        form=PaymentMethodForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context={'form':form}
    return render(request, 'Booker/payment_method_form.html', context)
    
@login_required(login_url='login')
def updatePaymentMethod(request, pk):
    payment_method =PaymentMethod.objects.get(id=pk)
    form =PaymentMethodForm(instance=payment_method)
    
    if request.method=='POST':
        form=PaymentMethodForm(request.POST, instance=payment_method)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context={'form':form}
    return render(request, 'Booker/payment_method_form.html', context)