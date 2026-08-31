from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from sellers.models import Product, Seller
from mails.models import Mails


def shop_lists(request):
    shops = Seller.objects.order_by('?')

    if request.user.is_authenticated:
        mails = Mails.objects.filter(
            receiver_id=request.user.email,
            status='unread'
        ).order_by('-id')


        return render(request, 'shop_lists.html', {
        'shops': shops,
        'mails': mails
    })

    return render(request, 'shop_lists.html', {
        'shops': shops,
    })



def shop_preview(request, id):
    shop = get_object_or_404(Seller, id=id)

    products = Product.objects.filter(owner = shop.user)


    if request.user.is_authenticated:
        mails = Mails.objects.filter(
            receiver_id=request.user.email,
            status='unread'
        ).order_by('-id')

        return render(request, 'shop_details.html', {
            'shop': shop,
            'products': products,
            'mails': mails
        })

    return render(request, 'shop_details.html', {
        'shop': shop,
        'products': products,
    })

