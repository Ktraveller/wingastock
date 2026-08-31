from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from sellers.models import Product, Seller
from django.db.models import Count


@login_required(login_url="login_admin")
def admin_home(request):
    product_t = Product.objects.aggregate(
        total=Count('id'),
    )

    seller =  Seller.objects.aggregate(
        total=Count('id', distinct=True),
    )
        
    return render(request, 'index_a.html', {
        'total_products': product_t,
        'total_seller': seller
    })