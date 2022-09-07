from django.urls import path
from . import views

app_name='Bus_admin'
urlpatterns= [
    path('home/', views.startHome, name="bus_admin-home"),
    path('home/<str:pk>/', views.home, name="home"),
    path('manage-single-bus/<str:pk>/', views.manageSingleBus, name="manage-single-bus"),
    path('add-single-bus/<str:pk>/', views.addSingleBus, name="add-single-bus"),
    path('update-single-bus/<str:pk>/', views.updateSingleBus, name="update-single-bus"),
    path('delete-single-bus/<str:pk>/', views.deleteSingleBus, name="delete-single-bus"),

    ##Managing Route urls

    path('add-route/', views.addRoute, name="add-route"),
    path('update-route/<str:pk>/', views.updateRoute, name="update-route"),
    path('add-sub-route/', views.addSubRoute, name="add-sub-route"),
    path('update-sub-route/<str:pk>/', views.updateSubRoute, name="update-sub-route"),
    # path('delete-route/<str:pk>/', views.deleteRoute, name="delete-route"),
    path('delete-sub-route/<str:pk>/', views.deleteSubRoute, name="delete-sub-route"),
]