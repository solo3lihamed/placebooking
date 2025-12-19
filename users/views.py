from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from bookings.models import Booking
from venues.models import Venue
from .models import User

def is_admin(user):
    return user.role == User.Role.ADMIN or user.is_superuser

@login_required
def customer_dashboard(request):
    bookings = Booking.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'users/customer_dashboard.html', {'bookings': bookings})

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    total_users = User.objects.count()
    total_venues = Venue.objects.count()
    total_bookings = Booking.objects.count()
    recent_bookings = Booking.objects.all().order_by('-created_at')[:10]
    
    context = {
        'total_users': total_users,
        'total_venues': total_venues,
        'total_bookings': total_bookings,
        'recent_bookings': recent_bookings
    }
    return render(request, 'users/admin_dashboard.html', context)
