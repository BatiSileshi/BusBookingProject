from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from Bus_admin.models import Route, Single_Bus, SubRoute
from System_admin.models import Bus, UserType
from django.contrib.auth.decorators import login_required
from .decorators import admin_only
from Customer.decorators import allowed_users
from .forms import RouteForm, SubRouteForm
# Create your views here.

@login_required(login_url='login')
@admin_only
def startHome(request):
    context={}
    return render(request, 'Bus_admin/start_home.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['busadmin'])
def home(request, pk):
    user=get_object_or_404(User, id=pk)
    buses=user.bus_set.all()
    sub_routes=SubRoute.objects.all()
    routes=user.route_set.all()
    context={'buses':buses, 'routes':routes, 'sub_routes':sub_routes}
    if request.user.user_type.type != 'busadmin':
        return HttpResponse("Not your page!")
    return render(request, 'Bus_admin/home.html', context)

"""Managing single bus"""
@login_required(login_url='login')
@allowed_users(allowed_roles=['busadmin'])
def manageSingleBus(request, pk):
    bus=get_object_or_404(Bus, id=pk)
    single_buses=bus.single_bus_set.all()
    context={'bus':bus, 'single_buses':single_buses}
    if request.user != bus.bus_admin:
        return HttpResponse("You are not allowed here!")
    return render(request, 'Bus_admin/manage_single_bus.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['busadmin'])
def addSingleBus(request, pk):
    bus=get_object_or_404(Bus, id=pk)
    if request.method == 'POST':
       singlebus=Single_Bus.objects.create(
          bus=bus,
          plate_number=request.POST['plate_number'], 
          bus_number=request.POST['bus_number'], 
          bus_type=request.POST['bus_type'], 
          bus_detail=request.POST['bus_detail'], 
          number_of_seats=request.POST['number_of_seats'], 
       )
       return redirect('Bus_admin:manage-single-bus', pk=bus.id)
    context={'bus':bus}
    if request.user != bus.bus_admin:
        return HttpResponse("You are not allowed here!")
    return render(request, 'Bus_admin/add_single_bus.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['busadmin'])
def updateSingleBus(request, pk):
    single_bus=get_object_or_404(Single_Bus, id=pk)
    if request.method == 'POST':
       singlebus=Single_Bus.objects.filter(id=pk).update(
          bus=single_bus.bus,
          plate_number=request.POST['plate_number'], 
          bus_number=request.POST['bus_number'], 
          bus_type=request.POST['bus_type'], 
          bus_detail=request.POST['bus_detail'], 
          number_of_seats=request.POST['number_of_seats'], 
       )
       return redirect('Bus_admin:manage-single-bus', pk=single_bus.bus.id)
    context={'single_bus':single_bus}
    if request.user != single_bus.bus.bus_admin:
        return HttpResponse("You are not allowed here!")
    return render(request, 'Bus_admin/update_single_bus.html', context)
 
@login_required(login_url='login')
@allowed_users(allowed_roles=['busadmin'])   
def deleteSingleBus(request, pk):
    single_bus=get_object_or_404(Single_Bus, id=pk)
    if request.method=='POST':
       single_bus.delete()
       return redirect('Bus_admin:manage-single-bus', pk=single_bus.bus.id)
    if request.user != single_bus.bus.bus_admin: 
           return HttpResponse("You are not allowed here!")
    return render(request, 'Bus_admin/delete.html', {'obj':single_bus})
"""End of single bus management"""

"""Managing Route  and SubRoute"""
@login_required(login_url='login')
@allowed_users(allowed_roles=['busadmin'])
def addRoute(request):
    form=RouteForm()
    
    if request.method == 'POST':
        form =RouteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Bus_admin:bus_admin-home')
        
    context={'form':form}
    return render(request, 'Bus_admin/route_form.html', context)\
        
@login_required(login_url='login')
@allowed_users(allowed_roles=['busadmin'])
def updateRoute(request, pk):
    subroute =get_object_or_404(SubRoute, id=pk)
    form =RouteForm(instance=subroute.main_route)
    
    if request.method=='POST':
        form=RouteForm(request.POST, instance=subroute.main_route)
        if form.is_valid():
            form.save()
            return redirect('Bus_admin:bus_admin-home')
        
    context={'form':form}
    if request.user != subroute.bus.bus.bus_admin:
        return HttpResponse("You are not allowed here!")
    return render(request, 'Bus_admin/route_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['busadmin'])
def addSubRoute(request):
    form=SubRouteForm()
    
    if request.method == 'POST':
        form =SubRouteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Bus_admin:bus_admin-home')
        
    context={'form':form}
    return render(request, 'Bus_admin/add_sub_route_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['busadmin'])
def updateSubRoute(request, pk):
    subroute=get_object_or_404(SubRoute, id=pk)
    form =SubRouteForm(instance=subroute)
    
    if request.method=='POST':
        form=SubRouteForm(request.POST, instance=subroute)
        if form.is_valid():
            form.save()
            return redirect('Bus_admin:bus_admin-home')
        
    context={'form':form}
    if request.user != subroute.bus.bus.bus_admin:
        return HttpResponse("You are not allowed here!")
    return render(request, 'Bus_admin/update_sub_route_form.html', context)

# def deleteRoute(request, pk):
#     subroute=get_object_or_404(SubRoute, id=pk)
#     if request.method=='POST':
#         subroute.main_route.delete()
#         return redirect('Bus_admin:home', pk=request.user.id)
#     if request.user != subroute.bus.bus.bus_admin:
#         return HttpResponse("You are not allowed here!")
#     return render(request, 'Booker/delete.html', {'obj':subroute.main_route})

@login_required(login_url='login')
@allowed_users(allowed_roles=['busadmin'])
def deleteSubRoute(request, pk):
    subroute=get_object_or_404(SubRoute, id=pk)
    if request.method=='POST':
        subroute.delete()
        return redirect('Bus_admin:home', pk=request.user.id)
    if request.user != subroute.bus.bus.bus_admin:
        return HttpResponse("You are not allowed here!")
    return render(request, 'Bus_admin/delete.html', {'obj':subroute})