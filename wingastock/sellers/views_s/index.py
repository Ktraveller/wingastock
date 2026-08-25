from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from sellers.models import Product
from django.db.models import Count


@login_required(login_url="login_seller")
def seller_home(request):
    product_t = Product.objects.filter(owner=request.user).aggregate(total=Count('id'))
        
    return render(request, 'index_s.html', {
        'total_products': product_t,
    })