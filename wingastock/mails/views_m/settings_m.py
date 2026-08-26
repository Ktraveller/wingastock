from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Mail system settings
@login_required(login_url="login_seller")
def mail_settings(request):
    return render(request, 'settings_m.html')


# For customer
@login_required(login_url="customer_login")
def mail_settings_c(request):
    return render(request, 'c/settings_m.html')