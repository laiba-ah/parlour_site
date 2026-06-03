from django.urls import path
from .views import services_list

app_name = 'services'

urlpatterns = [
    path('', services_list, name='services_list'),
]