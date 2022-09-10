from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserType(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,related_name="user_type")
    type=models.CharField(max_length=20,  null=True)
    
    def __str__(self):
        return str((self.user.username, self.type))


class Bus(models.Model):
    name=models.CharField(max_length=255, null=True)
    bus_admin=models.ForeignKey(User, on_delete=models.CASCADE , null=True)
    number_of_buses=models.IntegerField(null=True)
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    
class PaymentMethod(models.Model):
    name = models.CharField(max_length=55)
    type = models.CharField(max_length=55)
    logo = models.ImageField(max_length=55, null=True)
    description = models.TextField()
    code = models.IntegerField()
    contact = models.IntegerField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name