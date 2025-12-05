from django.contrib import admin
from bookings.models import Car, Booking, Service


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'year', 'price_per_day', 'user', 'status')
    search_fields = ('brand', 'model')
    list_filter = ('status', 'year')


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'car',
        'customer',
        'service',
        'start_date',
        'end_date',
        'total_cost',
        'status'
    )
    search_fields = ('customer__username', 'car__brand', 'car__model')
    list_filter = ('status', 'start_date')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration', 'price')
    search_fields = ('name',)
