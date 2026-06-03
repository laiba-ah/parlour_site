from django.db import models
from django.core.validators import RegexValidator


PHONE_REGEX = RegexValidator(
    regex=r'^\+?03\d{9}$',
    message="Enter a valid Pakistani phone number."
)


class TimeSlot(models.Model):
    time = models.TimeField(unique=True)
    label = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['time']

    def __str__(self):
        return self.label


class DayOff(models.Model):
    date = models.DateField(unique=True)
    reason = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Closed: {self.date}"


class Booking(models.Model):
    EVENT_CHOICES = [
        ('bridal', 'Bridal Makeup'),
        ('party', 'Party Makeup'),
        ('mehndi', 'Mehndi Event'),
        ('walima', 'Walima Event'),
        ('engagement', 'Engagement Event'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]

    customer_name = models.CharField(max_length=200)
    phone = models.CharField(validators=[PHONE_REGEX], max_length=15)
    email = models.EmailField(blank=True)
    
    event_type = models.CharField(
    max_length=20,
    choices=EVENT_CHOICES,
    default='bridal'
)
    date = models.DateField()
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.PROTECT, related_name='bookings')

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['date', 'time_slot']
        ordering = ['-date', 'time_slot']

    def __str__(self):
        return f"{self.customer_name} — {self.get_event_type_display()} on {self.date} at {self.time_slot}"