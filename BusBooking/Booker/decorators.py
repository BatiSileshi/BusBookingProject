from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model
User = get_user_model()
from django.shortcuts import render, redirect

def for_routeadmins(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    '''
    A decorator to check logged in user could be a student and redirects to the login page if the user isn't authenticated.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_routeadmin,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

# def for_teachers(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
#     '''
#     A decorator to check whether the logged-in user is a teacher and 
#     redirect to the login page if the user is not authenticated.
#     '''
#     actual_decorator = user_passes_test(
#         lambda u: u.is_active and u.is_teacher,
#         login_url=login_url,
#         redirect_field_name=redirect_field_name
#     )
#     if function:
#         return actual_decorator(function)
#     return actual_decorator


# def admin_only(view_func):
#     def wrapper_function(request, *args, **kwargs):
#         user
        
            
#         if user.is_busadmin==True:
#             return redirect('home')
#         if user.is_routeadmin == True:
#             return view_func(request, *args, **kwargs)
#     return wrapper_function
                