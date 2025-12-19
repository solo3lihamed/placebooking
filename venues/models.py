from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Venue(models.Model):
    class VenueType(models.TextChoices):
        HALL = "HALL", _("Hall")
        CAFE = "CAFE", _("Cafe")
        RESTAURANT = "RESTAURANT", _("Restaurant")
        GARDEN = "GARDEN", _("Garden")
        ROOFTOP = "ROOFTOP", _("Rooftop")
        VILLA = "VILLA", _("Villa")
        OTHER = "OTHER", _("Other")

    class PricingMethod(models.TextChoices):
        PER_HOUR = "PER_HOUR", _("Per Hour")
        PER_DAY = "PER_DAY", _("Per Day")
        PER_PERIOD = "PER_PERIOD", _("Per Period")
        PER_TABLE = "PER_TABLE", _("Per Table")

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", _("Active")
        INACTIVE = "INACTIVE", _("Inactive")
        MAINTENANCE = "MAINTENANCE", _("Maintenance")

    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="managed_venues")
    name = models.CharField(max_length=255)
    venue_type = models.CharField(max_length=50, choices=VenueType.choices)
    description = models.TextField()
    address = models.CharField(max_length=255)
    map_link = models.URLField(blank=True, null=True)
    capacity = models.PositiveIntegerField()
    
    pricing_method = models.CharField(max_length=50, choices=PricingMethod.choices)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.ACTIVE)
    
    # Policies
    cancellation_policy = models.TextField(blank=True, help_text="Details about cancellation")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_venue_type_display()})"

class VenueImage(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="venues/images/")
    caption = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']

class Service(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name="services")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_optional = models.BooleanField(default=True)
    image = models.ImageField(upload_to="services/images/", blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.venue.name}"

class Meal(models.Model):
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, related_name="meals")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    min_quantity = models.PositiveIntegerField(default=1)
    image = models.ImageField(upload_to="meals/images/", blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.venue.name}"
