from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def admin_login(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

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

        return render(request, "privilege/login.html", {
            "error": "Invalid email or password."
        })

    return render(request, "privilege/login.html")



@login_required(login_url="login_admin")
def admin_logout(request):
    logout(request)
    return redirect("login_admin")