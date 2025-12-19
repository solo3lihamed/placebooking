from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        MANAGER = "MANAGER", "Venue Manager"
        CUSTOMER = "CUSTOMER", "Customer"

    role = models.CharField(max_length=50, choices=Role.choices, default=Role.CUSTOMER)
    
    # Manager specific fields (can be linked to Venue later)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def is_manager(self):
         return self.role == self.Role.MANAGER

    def is_customer(self):
        return self.role == self.Role.CUSTOMER
