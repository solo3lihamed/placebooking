from django.db.models import Q
from .models import Booking
from venues.models import Venue

def check_availability(venue, start_time, end_time):
    """
    Check if a venue is available for a given time range.
    Returns True if available, False otherwise.
    """
    # Simple overlap check:
    # (StartA <= EndB) and (EndA >= StartB)
    overlapping_bookings = Booking.objects.filter(
        venue=venue,
        status__in=[Booking.Status.CONFIRMED, Booking.Status.APPROVED, Booking.Status.PENDING],
        start_time__lt=end_time,
        end_time__gt=start_time
    )
    
    return not overlapping_bookings.exists()

def calculate_price(venue, start_time, end_time, services=None, meals=None):
    """
    Calculate the total price based on venue pricing method and add-ons.
    """
    price = 0
    duration_hours = (end_time - start_time).total_seconds() / 3600
    
    if venue.pricing_method == Venue.PricingMethod.PER_HOUR:
        price = float(venue.base_price) * duration_hours
    elif venue.pricing_method == Venue.PricingMethod.PER_DAY:
        # Simplified: round up to days
        days = max(1, duration_hours / 24)
        price = float(venue.base_price) * days
    elif venue.pricing_method == Venue.PricingMethod.PER_PERIOD:
         price = float(venue.base_price)
    
    # Add services
    if services:
        for service in services:
             price += float(service.price)
             
    # Add meals (Assuming meals is a list of (meal_obj, quantity) tuples)
    if meals:
        for meal, qty in meals:
            price += float(meal.price) * qty
            
    return price
