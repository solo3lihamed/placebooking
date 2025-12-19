from django import forms
from .models import Venue

class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ['name', 'venue_type', 'description', 'address', 'map_link', 'capacity', 'pricing_method', 'base_price', 'status', 'cancellation_policy']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'cancellation_policy': forms.Textarea(attrs={'rows': 3}),
        }
