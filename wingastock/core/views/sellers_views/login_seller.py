from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


# Login sellers
def seller_login(request):
    if request.user.is_authenticated:
        return redirect("seller_home")  # Redirect to the seller home page if already logged in

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check if the email is a valid email or whatsapp number
        if "@" in email:
            # Authenticate using email
            try:
                user = User.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)
            except User.DoesNotExist:
                user = None
        else:
            # Authenticate using whatsapp number (username)
            user = authenticate(request, username=email, password=password)

            # redirect to seller home if user is authenticated
        if user is not None:
            login(request, user)
            return redirect("seller_home")  # Redirect to the seller home page after successful login
        else:
            return render(request, "sellers/login.html", {
                "error": "Invalid email/whatsapp number or password."
            })

    return render(request, "sellers/login.html")


# Signup sellers
def seller_signup(request):
    if request.user.is_authenticated:
        return redirect("seller_home")  # Redirect to the seller home page if already logged in

    if request.method == "POST":
        email = request.POST.get("email")
        whatsapp_number = request.POST.get("whatsapp_number")
        password = request.POST.get("password")

        # Check if the email is already registered
        if User.objects.filter(email=email).exists():
            return render(request, "sellers/signup.html", {
                "error": "Email is already registered."
            })

        # Whatsapp number
        if User.objects.filter(username=whatsapp_number).exists():
            return render(request, "sellers/signup.html", {
                "error": "Whatsapp number is already registered."
            })

        # validate whatsapp number format (basic validation) force start with 255
        if not whatsapp_number.startswith("255") or len(whatsapp_number) != 12:
            return render(request, "sellers/signup.html", {
                "error": "Invalid Whatsapp number format. It should start with '255' and be 12 digits long."
            })

        # Create a new user
        user = User.objects.create_user(username=whatsapp_number, email=email, password=password)
        user.save()

        login(request, user)  # Log in the newly created seller
        return redirect("seller_home")  # Redirect to the seller home page after signup

    return render(request, "sellers/signup.html")





@login_required(login_url="login_seller")
def seller_logout(request):
    logout(request)
    return redirect("login_seller")  # Redirect to the seller login page after logout