from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Mail system settings
@login_required(login_url="login_seller")
def mail_settings(request):

    # User must have a Seller profile
    if not hasattr(request.user, "seller"):
        return redirect("login_seller") 
    
    return render(request, 'settings_m.html')


# For customer
@login_required(login_url="customer_login")
def mail_settings_c(request):
    return render(request, 'c/settings_m.html')



# For Admin
@login_required(login_url="login_admin")
def mail_settings_a(request):

    # Only staff/admin users can access this page
    if not request.user.is_staff:
        return redirect("login_admin")
    
    return render(request, 'a/settings_m.html')