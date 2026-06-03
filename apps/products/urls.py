from django.urls import path

from .views import products_list


app_name = 'products'


urlpatterns = [
    path('', products_list, name='products_list'),
]