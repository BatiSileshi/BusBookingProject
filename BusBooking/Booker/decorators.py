from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse

# def for_routeadmins(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
#     '''
#     A decorator to check logged in user could be a student and redirects to the login page if the user isn't authenticated.
#     '''
#     actual_decorator = user_passes_test(
#         lambda u: u.is_active and u.is_routeadmin,
#         login_url=login_url,
#         redirect_field_name=redirect_field_name
#     )
#     if function:
#         return actual_decorator(function)
#     return actual_decorator



def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group=None 
        if request.user.groups.exists():
            group=request.user.groups.all()[0].name
        
        if group=='busadmin':
            return redirect('Bus_admin:bus_admin-home') 
        if group=='admin':
            return redirect('admin:index')
        if group=='customer':
            return redirect('home')
        if group == 'booker':
            return view_func(request, *args, **kwargs)
    return wrapper_function
                
                
      