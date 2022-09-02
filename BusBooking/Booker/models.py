from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
from System_admin.models import Bus

from Bus_admin.models import Route
from Customer.models import Booking
# Create your models here.

class PaymentMethod(models.Model):
    name = models.CharField(max_length=55)
    type = models.CharField(max_length=55)
    # logo = models.ImageField(max_length=55)
    description = models.TextField()
    code = models.IntegerField()
    contact = models.IntegerField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class PaymentInformantion(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE, blank=False, null=True)
    account_holder = models.CharField(max_length=55)
    account_number = models.IntegerField()
    phone_number = models.IntegerField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.payment_method.name)
    
class FinishPayment(models.Model):
    booking=models.OneToOneField(Booking, on_delete=models.CASCADE, primary_key=True, related_name="finishpymnt_booking")
    payment_method=models.ForeignKey(PaymentInformantion, on_delete=models.CASCADE, blank=True, null=True)
    paid_by=models.CharField(max_length=255, null=True)
    transaction_id=models.CharField(max_length=255, null=True)
    # screenshot=
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.paid_by
    
    
class FinishPaymentStatus(models.Model):
    fnishpayment=models.OneToOneField(FinishPayment, on_delete=models.CASCADE, primary_key=True, related_name="finishpayment_status")
    status=models.BooleanField(default=False, null=True)
    
    def __str__(self):
        return self.finishpayment
    
