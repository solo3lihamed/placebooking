from django.contrib import admin
from .models import Booking, BookingService, BookingMeal

class BookingServiceInline(admin.TabularInline):
    model = BookingService
    extra = 0

class BookingMealInline(admin.TabularInline):
    model = BookingMeal
    extra = 0

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'venue', 'customer', 'start_time', 'end_time', 'status', 'total_price')
    list_filter = ('status', 'start_time')
    search_fields = ('venue__name', 'customer__username')
    inlines = [BookingServiceInline, BookingMealInline]
