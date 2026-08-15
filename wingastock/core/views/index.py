from django.http import HttpResponse
from django.shortcuts import render
from core.models import Product


def home(request):
    products = Product.objects.order_by('?')[:50]
    products_o = Product.objects.order_by('?')
    return render(request, 'index.html', {
        'products': products,
        'products_o': products_o,
    })



# Favorite
def favorities(request):
    favorite_products = Product.objects.order_by('?')[:20]
    products = Product.objects.order_by('?')
    return render(request, 'favorities.html', {
        'favorite_products': favorite_products,
        'products': products
    })


# search
def search(request):
    search_result = Product.objects.order_by('?')
    products = Product.objects.order_by('?')[:50]
    return render(request, 'search.html', {
        'search_result': search_result,
        'products': products
    })


# Category
def categories(request):
    products = Product.objects.order_by('?')[:50]
    return render(request, 'categories.html', {
        'products': products
    })


# about use page
def about(request):
    return render(request, 'about.html', {})

# Term and rules
def terms_policy(request):
    return render(request, 'terms.html')

# Communication
def communication(request):
    return render(request, 'communication.html')

# web check that print "OK"
def health_check(request):
    return HttpResponse("OK", content_type="text/plain")
