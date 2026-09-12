from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from sellers.models import (
    Product,
    Seller,
    SellerPaymentRequest,
)
from mails.models import Mails
from deliver.models import DeliveryRequest


@login_required(login_url="login_admin")
def admin_home(request):

    # Only staff/admin users can access this page
    if not request.user.is_staff:
        return redirect("login_admin")

    # Total products
    product_t = Product.objects.aggregate(
        total=Count("id")
    )

    # Total sellers
    seller_t = Seller.objects.aggregate(
        total=Count("id")
    )

    # Total payment requests
    payment_t = SellerPaymentRequest.objects.aggregate(
        total=Count("id")
    )

    # Total delivery requests
    delivery_t = DeliveryRequest.objects.aggregate(
        total=Count("id")
    )

    # Total mails
    mail_t = Mails.objects.aggregate(
        total=Count("id")
    )

    return render(request, "index_a.html", {
        "total_products": product_t["total"],
        "total_seller": seller_t["total"],
        "total_payment": payment_t["total"],
        "total_delivery": delivery_t["total"],
        "total_mails": mail_t["total"],
    })