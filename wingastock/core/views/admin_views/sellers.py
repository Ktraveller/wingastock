from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.models import Product
from django.db.models import Count



@login_required(login_url="login_admin")
def sellers(request):

    sellers_list = Product.objects.all().order_by('phone').distinct()

    #seller =  Product.objects.aggregate(
     #   total=Count('phone', distinct=True),
    #)

    return render(request, 'privilege/sellers.html', {
        'sellers_list': sellers_list
    })