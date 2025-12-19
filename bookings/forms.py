from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import Booking

class BookingDateForm(forms.Form):
    start_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        label="وقت البداية"
    )
    end_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        label="وقت النهاية"
    )

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_time')
        end = cleaned_data.get('end_time')

        if start and end:
            if start < timezone.now():
                 raise ValidationError("لا يمكن الحجز في الماضي")
            if end <= start:
                raise ValidationError("وقت النهاية يجب أن يكون بعد وقت البداية")
        return cleaned_data

class BookingDetailsForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['event_type', 'attendees_count', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'event_type': 'نوع المناسبة',
            'attendees_count': 'عدد الحضور',
            'notes': 'ملاحظات إضافية'
        }
