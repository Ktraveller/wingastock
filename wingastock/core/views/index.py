from django.http import HttpResponse
from django.shortcuts import render
from sellers.models import Product
from mails.models import Mails
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import render


def home(request):
    products = Product.objects.filter(status='visible').order_by('?')

    if request.user.is_authenticated:
        mails = Mails.objects.filter(
            receiver_id=request.user.email,
            status='unread'
        ).order_by('-id')


        return render(request, 'index.html', {
        'products': products,
        'mails': mails
    })

    return render(request, 'index.html', {
        'products': products,
    })









# Favorite
def favorities(request):
    favorite_products = (
        Product.objects
        .filter(status="visible")
        .select_related("owner", "owner__seller")
        .order_by("-product_information__views")
    )

    return render(request, "favorities.html", {
        "favorite_products": favorite_products,
    })






# search
def search(request):

    query = request.GET.get("search", "").strip()

    # =========================================================
    # AJAX / LIVE SEARCH
    # =========================================================

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":

        if not query:
            return JsonResponse({
                "results": []
            })

        products = Product.objects.filter(
            status="visible"
        ).filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query) |
            Q(owner__seller__seller_name__icontains=query)
        ).select_related(
            "owner"
        )[:10]

        results = []

        for product in products:

            image_url = ""

            if product.image:
                image_url = product.image.url

            results.append({
                "id": product.id,
                "title": product.title,
                "description": product.description[:100],
                "price": str(product.price),
                "category": product.get_category_display(),
                "image": image_url,
                "seller": (
                    product.owner.seller.seller_name
                    if hasattr(product.owner, "seller")
                    else ""
                ),
                "url": product.get_absolute_url(),
            })

        return JsonResponse({
            "results": results
        })


    # =========================================================
    # NORMAL SEARCH PAGE
    # =========================================================

    search_result = Product.objects.filter(
        status="visible"
    ).order_by("?")

    if query:

        search_result = Product.objects.filter(
            status="visible"
        ).filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query) |
            Q(owner__seller__seller_name__icontains=query)
        ).order_by("-created_at")


    return render(
        request,
        "search.html",
        {
            "search_result": search_result,
        }
    )





# Category
def categories(request):

    return render(request, 'categories.html', {
    })






# about use page
def about(request):
    return render(request, 'about.html', {})






# Term and rules
def terms_policy(request):
    return render(request, 'terms.html')






# Communication
def communication(request):
    return render(request, 'communication.html')




# web check that print "OK"
def health_check(request):
    return HttpResponse("OK", content_type="text/plain")
