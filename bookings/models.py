from django.db import models
from django.conf import settings
from venues.models import Venue, Service, Meal
from django.utils.translation import gettext_lazy as _

class Booking(models.Model):
    class Status(models.TextChoices):
        Draft = "Draft", _("Draft")
        PENDING = "PENDING", _("Pending Review")
        APPROVED = "APPROVED", _("Approved by Admin")
        CONFIRMED = "CONFIRMED", _("Confirmed (Manager Assigned)")
        IN_PROGRESS = "IN_PROGRESS", _("In Progress")
        COMPLETED = "COMPLETED", _("Completed")
        CANCELLED = "CANCELLED", _("Cancelled")
        REJECTED = "REJECTED", _("Rejected")
        MAINTENANCE = "MAINTENANCE", _("Maintenance")

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name="bookings")
    
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    event_type = models.CharField(max_length=100) # Wedding, Birthday, etc.
    attendees_count = models.PositiveIntegerField()
    
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    deposit_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.Draft)
    
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking #{self.id} - {self.venue.name}"

class BookingService(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="booking_services")
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    price_at_booking = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1) # For services that might have quantity

class BookingMeal(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="booking_meals")
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    price_at_booking = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    notes = models.TextField(blank=True)
