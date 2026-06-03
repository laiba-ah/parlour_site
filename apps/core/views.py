from django.shortcuts import render

from apps.services.models import Service
from apps.products.models import Product


def home(request):

    featured_services = Service.objects.filter(
        is_featured=True,
        is_active=True
    )[:6]

    featured_products = Product.objects.filter(
        is_featured=True
    )[:8]

    context = {
        'featured_services': featured_services,
        'featured_products': featured_products,
    }

    return render(
        request,
        'core/home.html',
        context
    )