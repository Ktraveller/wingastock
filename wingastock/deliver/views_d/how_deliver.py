from django.shortcuts import render

def how_deliver(request):
    return render(request, 'how-to-deliver.html')