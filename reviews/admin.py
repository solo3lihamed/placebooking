from django.contrib import admin
from .models import Review, Complaint

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('venue', 'customer', 'rating', 'created_at')
    list_filter = ('rating',)

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('subject', 'venue', 'customer', 'status', 'created_at')
    list_filter = ('status',)
