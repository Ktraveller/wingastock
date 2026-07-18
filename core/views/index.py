from django.http import HttpResponse
from django.shortcuts import render
from core.models import Product


def home(request):
    scroll1_products = Product.objects.order_by('?')[:15]
    scroll2_products = Product.objects.order_by('?')[:15]
    scroll3_products = Product.objects.order_by('?')[:15]
    left1_products = Product.objects.order_by('?')[:25]
    left2_products = Product.objects.order_by('?')[:25]
    left3_products = Product.objects.order_by('?')[:25]
    right_products = Product.objects.order_by('?')[:25]

    search_result = Product.objects.order_by('?')[:10]

    # group 
    product_l = Product.objects.order_by('?')[:10]


    return render(request, 'index.html', {
        'scroll1_products': scroll1_products,
        'scroll2_products': scroll2_products,
        'scroll3_products': scroll3_products,
        'left1_products': left1_products,
        'left2_products': left2_products,
        'left3_products': left3_products,
        'right_products': right_products,

        'product_l': product_l,
        'search_result': search_result
    })


# about use page
def about(request):
    return render(request, 'about.html', {})


# web check that print "OK"
def health_check(request):
    return HttpResponse("OK", content_type="text/plain")
