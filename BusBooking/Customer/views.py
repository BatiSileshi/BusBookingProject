from multiprocessing import context
from django.shortcuts import get_object_or_404, render, redirect

from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import get_user_model
User = get_user_model()
from Account.forms import UserRegisterForm

from .models import Booking
from Account.models import User
from Bus_admin.models import Route,  Single_Bus, Seat, SubRoute
from Booker.models import FinishPayment
from System_admin.models import Bus
from django.contrib.auth.forms import UserCreationForm
### please do not import all classes from .models because there may be error while login

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required


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
        seat=request.POST.get('seat'),
        
        )
        return redirect ('my-booking', pk=request.user.id)
    
    context={'seats':seats}
    return render(request, 'Customer/booking.html', context)
    
    
def myBooking(request, pk):
    user = get_object_or_404(User, id=pk)
    bookings=user.booking_set.filter().order_by('-created')
    
    context={'bookings':bookings}
    return render(request, 'Customer/my_booking.html', context)

def pay(request, pk):
    booking = get_object_or_404(Booking, id=pk)
    payment_infos=booking.route.paymentinformantion_set.all()
    
    if request.method == 'POST':
        finishpymnt=FinishPayment.objects.create(
        booking=booking,
        payment_method_id=request.POST['payment_method'],
        paid_by=request.POST['paid_by'],
        transaction_id=request.POST['transaction_id'],
        )
        return redirect ('my-booking', pk=request.user.id)
    
    context={'booking':booking, 'payment_infos':payment_infos}
    return render(request, 'Customer/pay.html', context)

def loginPage(request):
    page='login'
    if request.method=='POST':
        phone_number=request.POST.get('phone_number')
        password=request.POST.get('password')

        try:
             user=User.objects.get(phone_number=phone_number)
           
        except:
            messages.error(request, 'Sorry! User does not exist.')
        user=authenticate(request, phone_number=phone_number, password=password)
        
        if user is not None:
           
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))

            else: 
                return redirect('home')
        else :
          messages.error(request, 'Sorry! phone_number or password does not exist.')  
    context={'page':page}
    return render(request, 'Customer/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    page='register'
    form=UserRegisterForm()
    
    if request.method =='POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.is_active = True
            user.save()
            return redirect('home')
        else:
            messages.error(request, "An error occured during registration")
    context={'page':page, 'form':form}
    return render(request, 'Customer/login_register.html', context)
