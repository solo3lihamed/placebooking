from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
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

@login_required
@user_passes_test(is_admin)
def admin_users_list(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'users/admin_users.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def admin_venues_list(request):
    venues = Venue.objects.all().order_by('-created_at')
    return render(request, 'users/admin_venues.html', {'venues': venues})

@login_required
@user_passes_test(is_admin)
def admin_bookings_list(request):
    bookings = Booking.objects.all().order_by('-created_at')
    return render(request, 'users/admin_bookings.html', {'bookings': bookings})

@login_required
@user_passes_test(is_admin)
def admin_booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'users/admin_booking_detail.html', {'booking': booking})

@login_required
@user_passes_test(is_admin)
def admin_update_booking_status(request, booking_id, status):
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Simple validation using choices
    valid_statuses = [choice[0] for choice in Booking.Status.choices]
    if status in valid_statuses:
        booking.status = status
        booking.save()
        messages.success(request, f"تم تحديث حالة الحجز #{booking.id} إلى {booking.get_status_display()}")
    else:
        messages.error(request, "حالة غير صحيحة!")
        
    return redirect('admin_booking_detail', booking_id=booking.id)
