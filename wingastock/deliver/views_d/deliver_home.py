from django.shortcuts import render


def deliver_home(request):
    return render(request, 'deliver_home.html')