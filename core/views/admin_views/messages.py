from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url="login_admin")
def messages(request):
    return render(request, 'privilege/messages.html', {
        'products': "I phone 15"
    })