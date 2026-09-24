from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from sellers.models import Product, Seller, UserLocation
from mails.models import Mails


def shop_lists(request):
    shops = Seller.objects.order_by('?')

    return render(request, 'shop_lists.html', {
        'shops': shops,
    })



def shop_preview(request, id):

    shop = get_object_or_404(
        Seller,
        id=id
    )

    # Seller products
    products = Product.objects.filter(
        owner=shop.user,
        status='visible'
    )

    # Seller location
    seller_location = None

    try:
        seller_location = shop.user.location
    except UserLocation.DoesNotExist:
        seller_location = None

    return render(
        request,
        "shop_details.html",
        {
            "shop": shop,
            "products": products,
            "seller_location": seller_location,
        }
    )
