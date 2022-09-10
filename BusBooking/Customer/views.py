from multiprocessing import context
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Booking
from django.contrib.auth.models import User, Group
from Bus_admin.models import Route,  Single_Bus, Seat, SubRoute
from Booker.models import FinishPayment
from System_admin.models import Bus
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
### please do not import all classes from .models because there may be error while login

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from .decorators import unauthenticated_user, allowed_users, admin_only


# Create your views here.


def home(request):
    q=request.GET.get('q') if request.GET.get('q') != None else ''
    routes=Route.objects.filter(
    
        Q(name__icontains=q) |
        Q(start__icontains=q) |
        Q(destination__icontains=q)|
        Q(travel_date__icontains=q)
        )
   
    context={'routes':routes}
    return render(request, 'Customer/home.html', context)


def route(request, pk):

    route = get_object_or_404(Route, id=pk)
    subroutes=route.subroute_set.all()
   
    context={'route':route, 'subroutes':subroutes}
    return render(request, 'Customer/route.html', context)

@login_required(login_url='login')
def booking(request, pk):
    subroute = get_object_or_404(SubRoute, id=pk)
    seats=Seat.objects.all()
    if request.method=='POST':
    
        book=Booking.objects.create(
        user=request.user,
        route=subroute.main_route,
        sub_route=subroute,
        bus=subroute.bus,
        start=subroute.main_route.start,
        destination=subroute.main_route.destination,
        travel_date=subroute.main_route.travel_date,
        travel_begin_time=subroute.main_route.travel_begin_time,
        travaler_name=request.POST['travaler_name'],
        traveler_contact=request.POST['traveler_contact'],
        seat_quantity=request.POST.get('seat_quantity'),
        
        )
        return redirect ('my-booking', pk=request.user.id)
    
    context={'seats':seats}
    return render(request, 'Customer/booking.html', context)
    
@login_required(login_url='login') 
def myBooking(request, pk):
    user = get_object_or_404(User, id=pk)
    bookings=user.booking_set.filter().order_by('-created')
    
    context={'bookings':bookings}
    if request.user != user: 
        return HttpResponse("You are not allowed here!")
    return render(request, 'Customer/my_booking.html', context)

@login_required(login_url='login')
def pay(request, pk):
    booking = get_object_or_404(Booking, id=pk)
    payment_infos=booking.route.paymentinformation_set.all()
    
    if request.method == 'POST':
        finishpymnt=FinishPayment.objects.create(
        booking=booking,
        payment_method_id=request.POST['payment_method'],
        paid_by=request.POST['paid_by'],
        transaction_id=request.POST['transaction_id'],
        screenshot=request.FILES.get('screenshot'),
        )
        return redirect ('my-booking', pk=request.user.id)
    
    context={'booking':booking, 'payment_infos':payment_infos}

    return render(request, 'Customer/pay.html', context)

@unauthenticated_user
def loginPage(request):
    page='login'
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        try:
             user=User.objects.get(username=username)
 
        except:
            messages.error(request, 'Sorry! User does not exist.')
        user=authenticate(request, username=username, password=password)
        
        if user is not None:
           
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))

            else: 
                return redirect('Booker:booker-home')
        else :
          messages.error(request, 'Sorry! username or password does not exist.')  
    context={'page':page}
    return render(request, 'Customer/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')

@unauthenticated_user
def registerPage(request):
    page='register'
    form=UserCreationForm()
    
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save()
            
            group=Group.objects.get(name='customer')
            user.groups.add(group)
   
            user.save()
            return redirect('login')
        else:
            messages.error(request, "An error occured during registration")
    context={'page':page, 'form':form}
    return render(request, 'Customer/login_register.html', context)
