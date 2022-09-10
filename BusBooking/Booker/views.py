from multiprocessing import context
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from Bus_admin.models import Route, SubRoute, Seat
from Customer.models import Booking
from System_admin.models import  PaymentMethod
from .models import FinishPayment, FinishPaymentStatus, PaymentInformation, AssignSeat
from .forms import  PaymentInformationForm
from django.contrib.auth.decorators import login_required, permission_required
from Customer.decorators import allowed_users
from .decorators import admin_only
# Create your views here.

@login_required(login_url='login')
@admin_only
def startHome(request):
    context={}
    return render(request, 'Booker/start_home.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['booker'])
def home(request, pk):
    user = get_object_or_404(User, id=pk)
    # subroute_bus_admins=user.subroutebusadmin_set.filter()
    # subroute_bus=user.subroutebusadmin.subroute_bus.all()
    # subroute_admins=user.subrouteadmin_set.filter()
    
    subroutes=user.subroute_set.filter()
    context={'user':user, 'subroutes':subroutes}
    
    if request.user != user:
           return HttpResponse("You are not allowed here!")
    return render(request, 'Booker/home.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['booker'])
def bookingRequest(request, pk):
    sub_route=get_object_or_404(SubRoute, id=pk)
    bookings=sub_route.booking_set.filter().order_by('-created') 
    finish_payment=FinishPayment.objects.filter()

    context={'sub_route':sub_route, 'bookings':bookings, 'finish_payment':finish_payment}
    if request.user != sub_route.sub_route_admin: 
           return HttpResponse("You are not allowed here!")
    return render(request, 'Booker/booking_request.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['booker'])
def finishPaymentStatus(request, pk):
    finishpayment=get_object_or_404(FinishPayment, booking_id=pk)
    bookings=Booking.objects.filter()

    if request.method == 'POST':
        status=FinishPaymentStatus.objects.create(
        fnishpayment=finishpayment,
        status=request.POST['status'],

        )
        return redirect ('Booker:booker-home')
   
    context={'bookings':bookings, 'finishpayment':finishpayment}
    # if request.user != finishpayment.booking.hotel.admin: 
    #        return HttpResponse("You are not allowed here!")
    return render(request, 'Booker/paid_unpaid.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['booker'])
def assignSeat(request, pk):
    booking=get_object_or_404(Booking, id=pk)
    seats=Seat.objects.all()
    if request.method == 'POST':
        asign=AssignSeat.objects.create(
        booking=booking,
        seat_number=request.POST.get('seat_number'),
       
        )
        return redirect ('Booker:booker-home')
   
    context={'booking':booking, 'seats':seats}
    if request.user != booking.route.route_admin: 
          return HttpResponse("You are not allowed here!")

    return render(request, 'Booker/assign_seat.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['booker'])
def editAssignedSeat(request, pk):
    asigned=get_object_or_404(AssignSeat, booking_id=pk)
    seats=Seat.objects.all()
    if request.method == 'POST':
        asign=AssignSeat.objects.filter(booking_id=pk).update(
        booking=asigned.booking,
        seat_number=request.POST.get('seat_number'),
       
        )
        return redirect ('Booker:booker-home')   
   
    context={'asigned':asigned, 'seats':seats}
    if request.user != asigned.booking.route.route_admin: 
          return HttpResponse("You are not allowed here!")

    return render(request, 'Booker/edit_assign_seat.html', context)


    """MANAGE PAYMENT INFORMATIONS"""
@login_required(login_url='login')
@allowed_users(allowed_roles=['booker'])
def managePaymentInformation(request, pk):
    route=get_object_or_404(Route, id=pk)
    payment_infos=route.paymentinformation_set.all()
    
    context={'route':route, 'payment_infos':payment_infos} 
    if request.user != route.route_admin: 
        return HttpResponse("You are not allowed here!")
    return render(request, 'Booker/manage_payment_info.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['booker'])
def addPaymentInfo(request, pk):
    route=get_object_or_404(Route, id=pk)
    pymnt_methods=PaymentMethod.objects.all()
    if request.method=='POST':
        payment_inf=PaymentInformation.objects.create(
            route=route, 
            payment_method_id=request.POST['payment_method'], 
            account_holder=request.POST['account_holder'], 
            account_number=request.POST['account_number'], 
            phone_number=request.POST['phone_number'], 
            
        )
        return redirect('Booker:booker-home')
        
    context={ 'route':route, 'pymnt_methods':pymnt_methods}
    if request.user != route.route_admin: 
        return HttpResponse("You are not allowed here!")
    return render(request, 'Booker/add_payment_info_form.html', context)
    
@login_required(login_url='login')
@allowed_users(allowed_roles=['booker'])
def updatePaymentInfo(request, pk):
    payment_info=get_object_or_404(PaymentInformation, id=pk)
    pymnt_methods=PaymentMethod.objects.all()
    if request.method=='POST':
        payment_inf=PaymentInformation.objects.filter(id=pk).update(
            route=payment_info.route, 
            payment_method_id=request.POST['payment_method'], 
            account_holder=request.POST['account_holder'], 
            account_number=request.POST['account_number'], 
            phone_number=request.POST['phone_number'], 
            
        )
        return redirect('Booker:booker-home')
        
    context={'payment_info':payment_info, 'pymnt_methods':pymnt_methods}
    if request.user != payment_info.route.route_admin: 
        return HttpResponse("You are not allowed here!")
    return render(request, 'Booker/update_payment_info_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['booker'])
def deletePaymentInfo(request, pk):
    payment_info=get_object_or_404(PaymentInformation, id=pk)
    if request.method=='POST':
        payment_info.delete()
        return redirect('Booker:booker-home')
    
    if request.user != payment_info.route.route_admin: 
        return HttpResponse("You are not allowed here!")
    return render(request, 'Booker/delete.html', {'obj':payment_info})