from django.forms import ModelForm

from .models import Route, SubRoute

    
class RouteForm(ModelForm):
    class Meta:
        model=Route
        fields='__all__'
        

class SubRouteForm(ModelForm):
    class Meta:
        model=SubRoute
        fields='__all__'     
        