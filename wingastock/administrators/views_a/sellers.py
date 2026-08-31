from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from sellers.models import Seller
from django.contrib.auth.models import User



@login_required(login_url="login_admin")
def sellers(request):

    sellers_list = Seller.objects.all().order_by('id').distinct()

    return render(request, 'sellers_a.html', {
        'sellers_list': sellers_list
    })



@login_required(login_url="login_admin")
def delete_seller(request, id):

    seller = get_object_or_404(Seller, id=id)

    user = get_object_or_404(User, id=seller.user.id)
    user.delete()

    return redirect('admin_sellers')