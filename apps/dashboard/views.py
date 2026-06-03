from django import forms
from django.shortcuts import render, redirect, get_object_or_404

from apps.bookings.models import Booking
from apps.products.models import Product
from apps.services.models import Service


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product

        fields = [
            'category',
            'name',
            'brand',
            'description',
            'price',
            'image',
            'stock',
            'is_featured'
        ]

        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service

        fields = [
            'name',
            'description',
            'price',
            'image'
        ]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

def dashboard_home(request):
    pending_bookings = Booking.objects.filter(status='pending').count()
    confirmed_bookings = Booking.objects.filter(status='confirmed').count()
    total_products = Product.objects.count()
    total_services = Service.objects.count()

    recent_bookings = Booking.objects.order_by('-created_at')[:5]

    context = {
        'pending_bookings': pending_bookings,
        'confirmed_bookings': confirmed_bookings,
        'total_products': total_products,
        'total_services': total_services,
        'recent_bookings': recent_bookings,
    }

    return render(request, 'dashboard/home.html', context)


def dashboard_bookings(request):
    bookings = Booking.objects.order_by('-created_at')

    return render(request, 'dashboard/bookings.html', {
        'bookings': bookings
    })


def confirm_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = 'confirmed'
    booking.save()

    return redirect('dashboard:bookings')


def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = 'cancelled'
    booking.save()

    return redirect('dashboard:bookings')


def dashboard_products(request):
    products = Product.objects.order_by('-created_at')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('dashboard:products')
        else:
            print(form.errors)

    else:
        form = ProductForm()

    return render(request, 'dashboard/products.html', {
        'products': products,
        'form': form
    })


def dashboard_services(request):
    services = Service.objects.all()

    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)

        if form.is_valid():
            service = form.save(commit=False)
            service.duration_minutes = 60
            service.is_active = True
            service.is_featured = False
            service.save()

            return redirect('dashboard:services')
        else:
            print(form.errors)

    else:
        form = ServiceForm()

    return render(request, 'dashboard/services.html', {
        'services': services,
        'form': form
    })