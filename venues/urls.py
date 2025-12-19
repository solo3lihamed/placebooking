from django.urls import path, include
from . import views

urlpatterns = [
    path('dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('create/', views.create_venue, name='create_venue'),
    path('update/<int:pk>/', views.update_venue, name='update_venue'),
    path('delete/<int:pk>/', views.delete_venue, name='delete_venue'),
    path('<int:pk>/', views.venue_detail, name='venue_detail'),
    path('<int:pk>/bookings/', views.venue_bookings, name='venue_bookings'),
    path('bookings/<int:booking_id>/status/<str:status>/', views.update_booking_status, name='update_booking_status'),
    path('bookings/<int:booking_id>/', views.venue_booking_detail, name='venue_booking_detail'),
    path('<int:venue_id>/calendar/', views.venue_calendar, name='venue_calendar'),
    path('<int:venue_id>/book/<int:step>/', include('bookings.urls')),
]
