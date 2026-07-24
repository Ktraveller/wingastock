from django.shortcuts import get_object_or_404, render
from core.models import Product

def products(request):
    products = Product.objects.order_by('?')
    return render(request, 'products.html', {
        'products': products,
    })



def preview_products(request, id):
    product = get_object_or_404(Product, id=id)
    products = Product.objects.order_by('?').filter(category=product.category)

    return render(request, 'product_details.html', {
        'product': product,
        'products': products,
    })


def filter_products(request, category):
    products = Product.objects.order_by('?').filter(category=category)
    products2 = Product.objects.order_by('?').filter(category=category)

    return render(request, 'products.html', {
        'products': products,
        'products2': products2,
    })

