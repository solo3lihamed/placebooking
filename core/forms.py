from django import forms
from venues.models import Venue

class SearchForm(forms.Form):
    query = forms.CharField(required=False, label='بحث', widget=forms.TextInput(attrs={
        'placeholder': 'اسم المكان...',
        'class': 'form-control'
    }))
    venue_type = forms.ChoiceField(
        choices=[('', 'الكل')] + Venue.VenueType.choices,
        required=False,
        label='نوع المكان'
    )
    price_min = forms.DecimalField(required=False, label='أقل سعر', min_value=0)
    price_max = forms.DecimalField(required=False, label='أعلى سعر', min_value=0)
    capacity = forms.IntegerField(required=False, label='السعة (شخص)', min_value=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if 'class' not in field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'
