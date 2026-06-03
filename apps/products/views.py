from django.shortcuts import render

from .models import ProductCategory, Product


def products_list(request):
    selected_category = request.GET.get('category')

    categories = ProductCategory.objects.all()

    products = Product.objects.select_related('category').all()

    if selected_category:
        products = products.filter(category__slug=selected_category)

    context = {
        'categories': categories,
        'products': products,
        'selected_category': selected_category,
    }

    return render(request, 'products/products_list.html', context)