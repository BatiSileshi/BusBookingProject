from django.db import models
from django.conf import settings
User = settings.AUTH_USER_MODEL

# Create your models here.

class Bus(models.Model):
    name=models.CharField(max_length=255, null=True)
    bus_admin=models.ForeignKey(User, on_delete=models.CASCADE , null=True)
    number_of_buses=models.IntegerField(null=True)
    about=models.CharField(max_length=255, null=True)
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class BusAdmin(models.Model):
    user=models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    bus=models.ForeignKey(Bus, null=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.bus.name