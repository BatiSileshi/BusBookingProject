from django.http import HttpResponse
from django.shortcuts import redirect 


def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group=None 
        if request.user.groups.exists():
            group=request.user.groups.all()[0].name
            
        if group=='customer':
            return redirect('home')            
        if group=='admin':
            return redirect('admin:index')
        if group=='booker':
            return redirect('Booker:booker-home')
        if group == 'busadmin':
            return view_func(request, *args, **kwargs)
    return wrapper_function
                