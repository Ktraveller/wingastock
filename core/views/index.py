from django.shortcuts import render
from core.models import Product


def home(request):
    products = Product.objects.prefetch_related('images').order_by('?')[:50]
    return render(request, 'index.html', {
        'products': products,
    })