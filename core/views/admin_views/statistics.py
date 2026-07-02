from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url="login_admin")
def statistics(request):
    return render(request, 'privilege/statistics.html', {
        'products': "I phone 15"
    })