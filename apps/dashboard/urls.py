from django.urls import path

from . import views


app_name = 'dashboard'


urlpatterns = [

    path('', views.dashboard_home, name='home'),

    path('bookings/', views.dashboard_bookings, name='bookings'),

    path(
        'bookings/<int:booking_id>/confirm/',
        views.confirm_booking,
        name='confirm_booking'
    ),

    path(
        'bookings/<int:booking_id>/cancel/',
        views.cancel_booking,
        name='cancel_booking'
    ),

    path(
        'products/',
        views.dashboard_products,
        name='products'
    ),

    path(
        'services/',
        views.dashboard_services,
        name='services'
    ),

]