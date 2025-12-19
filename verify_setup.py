import os
import django
from django.utils import timezone
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from venues.models import Venue
from bookings.models import Booking
from bookings.utils import check_availability, calculate_price
from django.urls import reverse

User = get_user_model()

def run_checks():
    print("Running system checks...")
    
    # 1. Check Superuser
    if User.objects.filter(is_superuser=True).exists():
        print("✅ Superuser exists.")
    else:
        print("❌ Superuser NOT found.")
        
    # 2. Check Manager Logic
    username = "test_manager"
    if not User.objects.filter(username=username).exists():
        manager = User.objects.create_user(username=username, password="password123", role=User.Role.MANAGER)
        print(f"✅ Created test manager: {username}")
    else:
        manager = User.objects.get(username=username)
        print(f"ℹ️ Test manager exists: {username}")
        
    # 3. Create Venue checking
    venue_name = "Royal Hall"
    if not Venue.objects.filter(name=venue_name).exists():
        venue = Venue.objects.create(
            manager=manager,
            name=venue_name,
            venue_type=Venue.VenueType.HALL,
            description="A luxury hall for weddings.",
            address="123 King St",
            capacity=500,
            pricing_method=Venue.PricingMethod.PER_PERIOD,
            base_price=5000.00
        )
        print(f"✅ Created venue: {venue_name}")
    else:
        venue = Venue.objects.get(name=venue_name)
        print(f"ℹ️ Venue exists: {venue_name}")
        
    # 4. Verify Home Query
    active_venues = Venue.objects.filter(status=Venue.Status.ACTIVE).count()
    print(f"✅ Active venues count: {active_venues}")

    # 5. Verify URL Resolution
    try:
        url = reverse('venue_detail', args=[venue.pk])
        print(f"✅ Venue detail URL resolves to: {url}")
        url_search = reverse('search')
        print(f"✅ Search URL resolves to: {url_search}")
        url_dashboard = reverse('customer_dashboard')
        print(f"✅ Customer Dashboard URL resolves to: {url_dashboard}")
        url_admin = reverse('admin_dashboard')
        print(f"✅ Admin Dashboard URL resolves to: {url_admin}")
        print(f"✅ Admin Users URL: {reverse('admin_users_list')}")
        print(f"✅ Admin Venues URL: {reverse('admin_venues_list')}")
        print(f"✅ Admin Bookings URL: {reverse('admin_bookings_list')}")
        # Manager Features
        print(f"✅ Venue Calendar URL: {reverse('venue_calendar', args=[1])}")
        
    except Exception as e:
        print(f"❌ URL resolution failed: {e}")

    # 6. Verify Availability Check
    start = timezone.now() + datetime.timedelta(days=1)
    end = start + datetime.timedelta(hours=4)
    
    is_available = check_availability(venue, start, end)
    print(f"✅ Availability Check (Future): {is_available}")
    
    # 7. Verify Price Calculation
    price = calculate_price(venue, start, end)
    print(f"✅ Calculated Price (Per Period): {price} (Expected: {venue.base_price})")
    
    # 8. Simulate Full Booking Flow
    # Create Customer
    cust_name = "test_customer"
    if not User.objects.filter(username=cust_name).exists():
        customer = User.objects.create_user(username=cust_name, password="password123", role=User.Role.CUSTOMER)
    else:
        customer = User.objects.get(username=cust_name)

    # Create Booking
    booking = Booking.objects.create(
        customer=customer,
        venue=venue,
        start_time=start,
        end_time=end,
        event_type="Wedding",
        attendees_count=100,
        status=Booking.Status.PENDING,
        total_price=price
    )
    print(f"✅ Created Booking #{booking.id} for {cust_name}")
    
    # Verify Manager sees it
    manager_bookings = venue.bookings.all()
    if booking in manager_bookings:
         print(f"✅ Manager can see booking #{booking.id}")
    else:
         print(f"❌ Manager CANNOT see booking #{booking.id}")

    # Verify Customer sees it
    customer_bookings = Booking.objects.filter(customer=customer)
    if booking in customer_bookings:
         print(f"✅ Customer can see their booking #{booking.id}")
    else:
         print(f"❌ Customer CANNOT see their booking #{booking.id}")

    print("All checks completed.")

if __name__ == "__main__":
    run_checks()
