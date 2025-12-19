from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from bookings.models import Booking
from .models import Venue
from .forms import VenueForm
import datetime
import calendar

def is_manager(user):
    return user.is_authenticated and (user.is_manager() or user.is_staff)

@login_required
@user_passes_test(is_manager)
def manager_dashboard(request):
    venues = Venue.objects.filter(manager=request.user)
    return render(request, 'venues/dashboard.html', {'venues': venues})

@login_required
@user_passes_test(is_manager)
def create_venue(request):
    if request.method == 'POST':
        form = VenueForm(request.POST, request.FILES)
        if form.is_valid():
            venue = form.save(commit=False)
            venue.manager = request.user
            venue.save()
            messages.success(request, 'Venue created successfully.')
            return redirect('manager_dashboard')
    else:
        form = VenueForm()
    return render(request, 'venues/venue_form.html', {'form': form, 'title': 'Create Venue'})

@login_required
@user_passes_test(is_manager)
def update_venue(request, pk):
    venue = get_object_or_404(Venue, pk=pk, manager=request.user)
    if request.method == 'POST':
        form = VenueForm(request.POST, request.FILES, instance=venue)
        if form.is_valid():
            form.save()
            messages.success(request, 'Venue updated successfully.')
            return redirect('manager_dashboard')
    else:
        form = VenueForm(instance=venue)
    return render(request, 'venues/venue_form.html', {'form': form, 'title': 'Update Venue', 'venue': venue})

@login_required
@user_passes_test(is_manager)
def delete_venue(request, pk):
    venue = get_object_or_404(Venue, pk=pk, manager=request.user)
    if request.method == 'POST':
        venue.delete()
        messages.success(request, 'Venue deleted successfully.')
        return redirect('manager_dashboard')
    return render(request, 'venues/venue_confirm_delete.html', {'venue': venue})

def venue_detail(request, pk):
    venue = get_object_or_404(Venue, pk=pk)
    return render(request, 'venues/venue_detail.html', {'venue': venue})

@login_required
@user_passes_test(is_manager)
def venue_bookings(request, pk):
    venue = get_object_or_404(Venue, pk=pk, manager=request.user)
    bookings = venue.bookings.all().order_by('-created_at')
    return render(request, 'venues/venue_bookings.html', {'venue': venue, 'bookings': bookings})

@login_required
def venue_booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    # Ensure user manages this venue
    if booking.venue.manager != request.user:
        messages.error(request, "ليس لديك صلاحية لعرض هذا الحجز")
        return redirect('manager_dashboard')
        
    return render(request, 'venues/venue_booking_detail.html', {'booking': booking})

@login_required
def venue_calendar(request, venue_id):
    venue = get_object_or_404(Venue, pk=venue_id)
    if venue.manager != request.user:
        return redirect('manager_dashboard')

    # Handle Block Date
    if request.method == 'POST':
        date_str = request.POST.get('block_date')
        try:
            block_date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            # Create a maintenance booking
            Booking.objects.create(
                customer=request.user, # Manager as blocking user
                venue=venue,
                start_time=datetime.datetime.combine(block_date, datetime.time.min),
                end_time=datetime.datetime.combine(block_date, datetime.time.max),
                event_type="Maintenance",
                status=Booking.Status.MAINTENANCE,
                total_price=0
            )
            messages.success(request, f"تم إغلاق اليوم {date_str} للصيانة.")
        except ValueError:
            messages.error(request, "تاريخ غير صحيح.")
        return redirect('venue_calendar', venue_id=venue.id)

    # Prepare Calendar Data using Python's HTMLCalendar? Or manual grid.
    # Let's do a simple manual grid for the current month.
    today = timezone.now().date()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))
    
    cal = calendar.monthcalendar(year, month)
    
    # Get bookings for this month
    bookings = Booking.objects.filter(
        venue=venue,
        start_time__year=year,
        start_time__month=month
    ).exclude(status__in=[Booking.Status.CANCELLED, Booking.Status.REJECTED])

    # Map bookings to days
    events_by_day = {}
    for b in bookings:
        day = b.start_time.day
        if day not in events_by_day:
            events_by_day[day] = []
        events_by_day[day].append(b)

    context = {
        'venue': venue,
        'calendar': cal,
        'year': year,
        'month': month,
        'today': today,
        'month_name': calendar.month_name[month],
        'events_by_day': events_by_day
    }
    return render(request, 'venues/venue_calendar.html', context)

@login_required
@user_passes_test(is_manager)
def update_booking_status(request, booking_id, status):
    booking = get_object_or_404(Booking, id=booking_id, venue__manager=request.user)
    if status in ['CONFIRMED', 'REJECTED', 'COMPLETED']:
        booking.status = getattr(Booking.Status, status) if status != 'REJECTED' else Booking.Status.CANCELLED 
        # Note: mapping REJECTED to CANCELLED or a new status if we added one. 
        # Let's map REJECTED to CANCELLED for now or we should have added REJECTED to choices.
        # Earlier I defined Status: Draft, PENDING, APPROVED, CONFIRMED, IN_PROGRESS, COMPLETED, CANCELLED
        if status == 'REJECTED':
            booking.status = Booking.Status.CANCELLED
        booking.save()
        messages.success(request, f'تم تحديث حالة الحجز إلى {booking.get_status_display()}')
    
    return redirect('venue_bookings', pk=booking.venue.id)
