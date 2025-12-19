from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from venues.models import Venue, Service, Meal
from .models import Booking, BookingService, BookingMeal
from .forms import BookingDateForm, BookingDetailsForm
from .utils import check_availability, calculate_price
import datetime

@login_required
def booking_wizard(request, venue_id, step=1):
    venue = get_object_or_404(Venue, pk=venue_id)
    
    # Session management for wizard data
    session_key = f'booking_venue_{venue_id}'
    booking_data = request.session.get(session_key, {})

    if step == 1: # Date Selection
        if request.method == 'POST':
            form = BookingDateForm(request.POST)
            if form.is_valid():
                start = form.cleaned_data['start_time']
                end = form.cleaned_data['end_time']
                
                if check_availability(venue, start, end):
                    booking_data['start_time'] = start.isoformat()
                    booking_data['end_time'] = end.isoformat()
                    request.session[session_key] = booking_data
                    return redirect('booking_wizard_step', venue_id=venue.id, step=2)
                else:
                    messages.error(request, 'المكان غير متاح في هذا التوقيت. يرجى اختيار موعد آخر.')
        else:
            initial = {}
            if 'start_time' in booking_data:
                initial['start_time'] = datetime.datetime.fromisoformat(booking_data['start_time'])
            if 'end_time' in booking_data:
                initial['end_time'] = datetime.datetime.fromisoformat(booking_data['end_time'])
            form = BookingDateForm(initial=initial)
        
        return render(request, 'bookings/wizard_step1.html', {'venue': venue, 'form': form})

    elif step == 2: # Details
        if request.method == 'POST':
            form = BookingDetailsForm(request.POST)
            if form.is_valid():
                 booking_data.update(form.cleaned_data)
                 request.session[session_key] = booking_data
                 return redirect('booking_wizard_step', venue_id=venue.id, step=3)
        else:
            form = BookingDetailsForm(initial=booking_data)
            
        return render(request, 'bookings/wizard_step2.html', {'venue': venue, 'form': form})

    elif step == 3: # Services & Meals
        if request.method == 'POST':
            # Manual handling of services/meals checkboxes/inputs
            selected_services = request.POST.getlist('services')
            meals_data = {}
            for key, value in request.POST.items():
                if key.startswith('meal_qty_') and int(value) > 0:
                    meal_id = key.split('_')[2]
                    meals_data[meal_id] = int(value)
            
            booking_data['services'] = selected_services
            booking_data['meals'] = meals_data
            request.session[session_key] = booking_data
            return redirect('booking_wizard_step', venue_id=venue.id, step=4)
            
        return render(request, 'bookings/wizard_step3.html', {'venue': venue})

    elif step == 4: # Review & Submit
        # Calculate totals for display
        start = datetime.datetime.fromisoformat(booking_data['start_time'])
        end = datetime.datetime.fromisoformat(booking_data['end_time'])
        
        services_objs = Service.objects.filter(id__in=booking_data.get('services', []))
        
        meals_list = []
        meals_dict = booking_data.get('meals', {})
        for m_id, qty in meals_dict.items():
            m_obj = Meal.objects.get(id=m_id)
            meals_list.append((m_obj, qty))
            
        total_price = calculate_price(venue, start, end, services_objs, meals_list)
        
        if request.method == 'POST':
            # Create Booking
            booking = Booking.objects.create(
                customer=request.user,
                venue=venue,
                start_time=start,
                end_time=end,
                event_type=booking_data['event_type'],
                attendees_count=booking_data['attendees_count'],
                notes=booking_data.get('notes', ''),
                status=Booking.Status.PENDING,
                total_price=total_price
            )
            
            # Create Relations
            for serv in services_objs:
                BookingService.objects.create(booking=booking, service=serv, price_at_booking=serv.price)
                
            for meal_obj, qty in meals_list:
                BookingMeal.objects.create(booking=booking, meal=meal_obj, price_at_booking=meal_obj.price, quantity=qty)
                
            # Clear session
            del request.session[session_key]
            
            messages.success(request, 'تم إرسال طلب الحجز بنجاح! سيتم مراجعته من قبل الإدارة.')
            return redirect('customer_dashboard') # To be implemented
            
        context = {
            'venue': venue,
            'booking_data': booking_data,
            'start': start,
            'end': end,
            'services': services_objs,
            'meals': meals_list,
            'total_price': total_price
        }
        return render(request, 'bookings/wizard_step4.html', context)
        
    return redirect('home')
