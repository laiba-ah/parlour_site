# apps/bookings/views.py


from datetime import date as date_type

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_GET

from .forms import BookingForm
from .models import TimeSlot, Booking, DayOff


def booking_page(request):

    if request.method == 'POST':
        form = BookingForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('bookings:success')

    else:
        form = BookingForm()

    return render(
        request,
        'bookings/booking_page.html',
        {
            'form': form
        }
    )


def booking_success(request):

    return render(
        request,
        'bookings/success.html'
    )


@require_GET
def get_available_slots(request):

    date_str = request.GET.get('date')

    # Validate date exists
    if not date_str:
        return JsonResponse(
            {'error': 'Date is required'},
            status=400
        )

    # Validate date format
    try:
        selected_date = date_type.fromisoformat(date_str)

    except ValueError:
        return JsonResponse(
            {'error': 'Invalid date format'},
            status=400
        )

    # Prevent past booking
    if selected_date < timezone.localdate():
        return JsonResponse(
            {'error': 'Past dates not allowed'},
            status=400
        )

    # Parlour closed check
    if DayOff.objects.filter(date=selected_date).exists():
        return JsonResponse({
            'closed': True,
            'slots': []
        })

    # Active slots
    all_slots = TimeSlot.objects.filter(
        is_active=True
    )

    # Already booked slots
    booked_slot_ids = set(
        Booking.objects.filter(
            date=selected_date,
            status__in=['pending', 'confirmed']
        ).values_list(
            'time_slot_id',
            flat=True
        )
    )

    slots = []

    for slot in all_slots:

        slots.append({
            'id': slot.id,
            'label': slot.label,
            'available': slot.id not in booked_slot_ids
        })

    return JsonResponse({
        'closed': False,
        'slots': slots
    })