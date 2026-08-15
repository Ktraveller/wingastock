from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.models import Product
from django.db.models import Count


@login_required(login_url="login_seller")
def seller_home(request):
    product_t = Product.objects.filter(phone=request.user.username).aggregate(total=Count('id'))
        
    return render(request, 'sellers/index.html', {
        'total_products': product_t,
    })