from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/users/', views.admin_users_list, name='admin_users_list'),
    path('admin/venues/', views.admin_venues_list, name='admin_venues_list'),
    path('admin/bookings/', views.admin_bookings_list, name='admin_bookings_list'),
    path('admin/bookings/<int:booking_id>/', views.admin_booking_detail, name='admin_booking_detail'),
    path('admin/bookings/<int:booking_id>/status/<str:status>/', views.admin_update_booking_status, name='admin_update_booking_status'),
]
