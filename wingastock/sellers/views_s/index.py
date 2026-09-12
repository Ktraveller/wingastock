from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from mails.models import Mails
from sellers.models import Product, Product_informations, SellerPaymentRequest
from django.db.models import Count, Sum


@login_required(login_url="login_seller")
def seller_home(request):

    # User must have a Seller profile
    if not hasattr(request.user, "seller"):
        return redirect("login_seller") 

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
    messages = Mails.objects.filter(receiver_id=request.user.email, status='sent')
    messages.update(status='unread')
    
    mails = Mails.objects.filter(
            receiver_id=request.user.email,
            status='unread'
        ).order_by('-id')

    total_mails = mails.aggregate(total=Count('id'))
    paid_posts = sum(
        item.requested_products
        for item in SellerPaymentRequest.objects.filter(
            seller=request.user,
            status='approved',
        )
    )
    product_limit = 5 + paid_posts
    chart_products = list(products.order_by('-product_information__views', '-created_at')[:8])

    return render(request, 'index_s.html', {
        'products': products,
        'total_products': total_products,
        'total_views': total_views,
        'mails': mails,
        'total_mails': total_mails,
        'product_limit': product_limit,
        'product_progress': min(100, round((total_products / product_limit) * 100)) if product_limit else 0,
        'chart_products': chart_products,
    })



# Seller terms and condtions
@login_required(login_url="login_seller")
def seller_terms_conditions(request):

    # User must have a Seller profile
    if not hasattr(request.user, "seller"):
        return redirect("login_seller") 
    
    return render(request, 'terms-conditions_s.html')