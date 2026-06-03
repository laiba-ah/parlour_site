# apps/bookings/urls.py

from django.urls import path

from . import views


app_name = 'bookings'


urlpatterns = [

    path(
        '',
        views.booking_page,
        name='booking'
    ),

    path(
        'slots/',
        views.get_available_slots,
        name='slots'
    ),

    path(
        'success/',
        views.booking_success,
        name='success'
    ),
]

