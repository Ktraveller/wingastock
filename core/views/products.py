from django.shortcuts import get_object_or_404, render
from core.models import Product

def products(request):
    products = Product.objects.prefetch_related('images').order_by('?')[:50]
    return render(request, 'products.html', {
        'products': products,
    })



def preview_products(request, id):
    product = get_object_or_404(Product, id=id)
    products = Product.objects.prefetch_related('images').order_by('?')[:50]
    return render(request, 'product_details.html', {
        'product': product,
        'products': products
    })


def filter_products(request, category):
    products = Product.objects.prefetch_related('images').order_by('?').filter(category=category)[:50]
    products_related = Product.objects.prefetch_related('images').order_by('?')[:50]
    return render(request, 'products.html', {
        'products': products,
        'category': category,
        'product_related': products_related
    })