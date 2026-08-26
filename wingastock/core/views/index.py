from django.http import HttpResponse
from django.shortcuts import render
from sellers.models import Product
from mails.models import Mails
from django.shortcuts import get_object_or_404


def home(request):
    products = Product.objects.filter(status='visible').order_by('?')

    if request.user.is_authenticated:
        mails = Mails.objects.filter(
            receiver_id=request.user.email,
            status='unread'
        ).order_by('-id')


        return render(request, 'index.html', {
        'products': products,
        'mails': mails
    })

    return render(request, 'index.html', {
        'products': products,
    })



# Favorite
def favorities(request):
    favorite_products = Product.objects.filter(status='visible').order_by('?')

    if request.user.is_authenticated:
        mails = Mails.objects.filter(
            receiver_id=request.user.email,
            status='unread'
        ).order_by('-id')


        return render(request, 'favorities.html', {
        'favorite_products': favorite_products,
        'mails': mails
    })

    return render(request, 'favorities.html', {
        'favorite_products': favorite_products,
    })


# search
def search(request):
    search_result = Product.objects.filter(status='visible').order_by('?')

    if request.user.is_authenticated:
        mails = Mails.objects.filter(
            receiver_id=request.user.email,
            status='unread'
        ).order_by('-id')


        return render(request, 'search.html', {
        'search_result': search_result,
        'mails': mails
    })

    return render(request, 'search.html', {
        'search_result': search_result,
    })


# Category
def categories(request):

    if request.user.is_authenticated:
        mails = Mails.objects.filter(
            receiver_id=request.user.email,
            status='unread'
        ).order_by('-id')


        return render(request, 'categories.html', {
        'mails': mails
    })

    return render(request, 'categories.html', {
    })


# about use page
def about(request):
    if request.user.is_authenticated:
        mails = Mails.objects.filter(
            receiver_id=request.user.email,
            status='unread'
        ).order_by('-id')


        return render(request, 'about.html', {
        'mails': mails
    })

    return render(request, 'about.html', {})

# Term and rules
def terms_policy(request):
        
    if request.user.is_authenticated:
        mails = Mails.objects.filter(
            receiver_id=request.user.email,
            status='unread'
        ).order_by('-id')


        return render(request, 'terms.html', {
        'mails': mails
    })

    return render(request, 'terms.html')

# Communication
def communication(request):

    if request.user.is_authenticated:
        mails = Mails.objects.filter(
            receiver_id=request.user.email,
            status='unread'
        ).order_by('-id')


        return render(request, 'communication.html', {
        'mails': mails
    })
    return render(request, 'communication.html')

# web check that print "OK"
def health_check(request):
    return HttpResponse("OK", content_type="text/plain")
