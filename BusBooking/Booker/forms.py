from django.forms import ModelForm
from django.conf.urls.static import static 
from .models import PaymentInformation




     
     
class PaymentInformationForm(ModelForm):
    class Meta:
        model=PaymentInformation
        fields='__all__'
      
        