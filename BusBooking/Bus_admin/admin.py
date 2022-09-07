from django.contrib import admin
from .models import *
# Register your models here.




class ChoiceInline(admin.TabularInline):
    model = SubRoute
    extra = 1



class Single_BusAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['bus','bus_number','bus_type', 'bus_detail', 'number_of_seats']}),
       
    ]
    inlines = [ChoiceInline]

admin.site.register(Single_Bus, Single_BusAdmin)




class ChoiceInlineee(admin.StackedInline):
    model = SubRoute
    extra = 1


class RouteAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['route_admin', 'name', 'start', 'destination', 'via_cities', 'travel_date', 'travel_begin_time', 'travel_distance', 'travel_aproximate_time', 'single_seat_price', 'travel_facilities' ]}),
        
    ]
    inlines = [ChoiceInlineee]

admin.site.register(Route, RouteAdmin)

admin.site.register(SubRoute)
admin.site.register(Seat)

