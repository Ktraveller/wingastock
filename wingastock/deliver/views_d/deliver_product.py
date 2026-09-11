from django.shortcuts import render

def deliver_product(request):
    return render(request, 'deliver_product.html')