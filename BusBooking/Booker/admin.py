from django.contrib import admin
from .models import PaymentInformation, FinishPayment, FinishPaymentStatus, AssignSeat
from System_admin.models import PaymentMethod
# Register your models here.


# class ChoiceInline(admin.TabularInline):
#     model = PaymentInformantion
#     extra = 3


# class PaymentMethodAdmin(admin.ModelAdmin):
#     fieldsets = [
#         (None,               {'fields': ['account_holder', 'account_number', 'phone_number']}),

#     ]
#     inlines = [ChoiceInline]

# admin.site.register(PaymentMethod, PaymentMethodAdmin)
admin.site.register(PaymentInformation)
admin.site.register(FinishPayment)
admin.site.register(FinishPaymentStatus)
admin.site.register(AssignSeat)