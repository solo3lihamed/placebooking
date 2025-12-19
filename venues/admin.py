from django.contrib import admin
from .models import Venue, Service, Meal, VenueImage

class VenueImageInline(admin.TabularInline):
    model = VenueImage
    extra = 1

class ServiceInline(admin.TabularInline):
    model = Service
    extra = 1

class MealInline(admin.TabularInline):
    model = Meal
    extra = 1

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'venue_type', 'manager', 'pricing_method', 'base_price', 'status')
    list_filter = ('venue_type', 'status', 'pricing_method')
    search_fields = ('name', 'description')
    inlines = [VenueImageInline, ServiceInline, MealInline]

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'venue', 'price', 'is_optional')

@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('name', 'venue', 'price', 'min_quantity')
