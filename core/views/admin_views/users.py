from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url="login_admin")
def users(request):
    return render(request, 'privilege/users.html', {
        'products': "I phone 15"
    })