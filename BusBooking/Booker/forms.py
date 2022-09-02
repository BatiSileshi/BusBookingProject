from django.forms import ModelForm
from django.conf.urls.static import static 
from .models import PaymentMethod, PaymentInformantion



class PaymentMethodForm(ModelForm):
    class Meta:
        model=PaymentMethod
        fields='__all__'
     
     
class PaymentInformationForm(ModelForm):
    class Meta:
        model=PaymentInformantion
        fields='__all__'