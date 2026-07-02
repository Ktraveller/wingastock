from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.models import Product
from django.db.models import Count


@login_required(login_url="login_admin")
def admin_home(request):
    product_t = Product.objects.aggregate(
        total=Count('id'),
    )

    seller =  Product.objects.aggregate(
        total=Count('phone', distinct=True),
    )
    
    print(seller)
    
    return render(request, 'privilege/index.html', {
        'total_products': product_t,
        'total_seller': seller
    })