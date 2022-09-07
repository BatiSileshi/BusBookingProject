from django.contrib import admin
from .models import Bus, PaymentMethod, UserType



admin.site.register(Bus)

admin.site.register(PaymentMethod)
admin.site.register(UserType)