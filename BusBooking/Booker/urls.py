from django.urls import path
from . import views

urlpatterns= [
    path('home/', views.startHome, name="booker-home"),
    path('home/<str:pk>/', views.home, name="home"),
    path('booking-request/<str:pk>/', views.bookingRequest, name="booking-request"),
    path('paid-unpaid/<str:pk>/', views.finishPaymentStatus, name="paid-unpaid"),
    path('manage-payment_info/<str:pk>/', views.managePaymentInformation, name="manage-payment_info"),
    path('add-payment_method/', views.addPaymentMethod, name="add-payment_method"),
    path('update-payment_method/<str:pk>/', views.updatePaymentMethod, name="update-payment_method"),
    
]