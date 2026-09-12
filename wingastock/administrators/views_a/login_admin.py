from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def admin_login(request):

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=email,   # assuming username is the email
            password=password
        )

        if user is not None and user.is_staff:
            login(request, user)
            return redirect("admin_home")

        return render(request, "login_a.html", {
            "error": "Invalid email or password."
        })

    return render(request, "login_a.html")



@login_required(login_url="login_admin")
def admin_logout(request):

    # Only staff/admin users can access this page
    if not request.user.is_staff:
        return redirect("login_admin")
    
    logout(request)
    return redirect("login_admin")