from django.urls import path
from . import views

app_name='Booker'
urlpatterns= [
    path('home/', views.startHome, name="booker-home"),
    path('home/<str:pk>/', views.home, name="home"),
    path('booking-request/<str:pk>/', views.bookingRequest, name="booking-request"),
    path('paid-unpaid/<str:pk>/', views.finishPaymentStatus, name="paid-unpaid"),
    path('assign-seat/<str:pk>/', views.assignSeat, name="assign-seat"), 
    path('edit-assigned-seat/<str:pk>/', views.editAssignedSeat, name="edit-assigned-seat"),
    path('manage-payment_info/<str:pk>/', views.managePaymentInformation, name="manage-payment_info"),
    path('add-payment_info/<str:pk>/', views.addPaymentInfo, name="add-payment_info"),
    path('update-payment_info/<str:pk>/', views.updatePaymentInfo, name="update-payment_info"),
    path('delete-payment_info/<str:pk>/', views.deletePaymentInfo, name="delete-payment_info"),
    
]