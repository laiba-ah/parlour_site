from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking

        fields = [
            'customer_name',
            'phone',
            'email',
            'event_type',
            'date',
            'time_slot',
            'notes'
        ]

        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your name'
            }),

            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '03XXXXXXXXX'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Optional email'
            }),

            'event_type': forms.Select(attrs={
                'class': 'form-select'
            }),

            'date': forms.HiddenInput(),

            'time_slot': forms.HiddenInput(),

            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write event details, address or special request'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()

        date = cleaned_data.get('date')
        time_slot = cleaned_data.get('time_slot')

        if date and time_slot:
            conflict = Booking.objects.filter(
                date=date,
                time_slot=time_slot,
                status__in=['pending', 'confirmed']
            ).exists()

            if conflict:
                raise forms.ValidationError(
                    "This slot was just booked. Please choose another slot."
                )

        return cleaned_data