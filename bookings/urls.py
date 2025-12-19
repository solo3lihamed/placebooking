from django.urls import path
from . import views

urlpatterns = [
    path('', views.booking_wizard, name='booking_wizard_step'),
]
