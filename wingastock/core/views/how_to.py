from django.shortcuts import render

# What is wingastock
def how1(request):
    return render(request, 'what_is.html')


# How to get seller phone
def how2(request):
    return render(request, 'how2.html')


# How to get register as seller
def how3(request):
    return render(request, 'how3.html')