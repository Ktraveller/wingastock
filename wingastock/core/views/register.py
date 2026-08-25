from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


# Customer login
def customer_register(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not email or not password:
            return render(request, "register.html", {
                "error": "Email and password are required."
            })

        if User.objects.filter(email=email).exists():
            return render(request, "register.html", {
                "error": "An account with this email already exists."
            })

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )

        # Automatically log the user in
        login(request, user)

        return redirect("home")

    return render(request, "register.html")




# Customer login
def customer_login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if not email or not password:
            return render(request, "login.html", {
                "error": "Email and password are required."
            })

        # Since we use email as username during registration
        user = authenticate(
            request,
            username=email,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("home")

        return render(request, "login.html", {
            "error": "Invalid email or password."
        })  

    return render(request, "login.html")



# Logout
def customer_logout(request):
    logout(request)
    return redirect("customer_login")