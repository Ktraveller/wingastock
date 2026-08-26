from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from mails.models import Mails
from sellers.models import Product, Product_informations
from django.db.models import Count, Sum


@login_required(login_url="login_seller")
def seller_home(request):

    products = Product.objects.filter(
        owner=request.user
    ).select_related('product_information')

    total_products = products.count()

    total_views = Product_informations.objects.filter(
        product__owner=request.user
    ).aggregate(
        total=Sum('views')
    )['total'] or 0


    # Mails
    mails = Mails.objects.filter(
            receiver_id=request.user.email,
            status='unread'
        ).order_by('-id')

    total_mails = mails.aggregate(total=Count('id'))

    return render(request, 'index_s.html', {
        'products': products,
        'total_products': total_products,
        'total_views': total_views,
        'mails': mails,
        'total_mails': total_mails,
    })