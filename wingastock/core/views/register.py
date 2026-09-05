import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import redirect




# Customer registration
def customer_register(request):
    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "error": "Only POST requests are allowed."
        }, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({
            "success": False,
            "error": "Invalid JSON data."
        }, status=400)

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    # Validate fields
    if not email or not password:
        return JsonResponse({
            "success": False,
            "error": "Email and password are required."
        }, status=400)

    # Check existing account
    if User.objects.filter(email=email).exists():
        return JsonResponse({
            "success": False,
            "error": "An account with this email already exists."
        }, status=400)

    # Create user
    user = User.objects.create_user(
        username=email,
        email=email,
        password=password
    )

    # Automatically login
    login(request, user)

    return JsonResponse({
        "success": True,
        "message": "Account created successfully.",
        "redirect_url": reverse("home")
    })


# Customer login
def customer_login(request):
    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "error": "Only POST requests are allowed."
        }, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({
            "success": False,
            "error": "Invalid JSON data."
        }, status=400)

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    # Validate fields
    if not email or not password:
        return JsonResponse({
            "success": False,
            "error": "Email and password are required."
        }, status=400)

    # Authenticate
    user = authenticate(
        request,
        username=email,
        password=password
    )

    if user is not None:
        login(request, user)

        return JsonResponse({
            "success": True,
            "message": "Login successful.",
        })

    return JsonResponse({
        "success": False,
        "error": "Invalid email or password."
    }, status=401)




# Logout
def customer_logout(request):
    logout(request)
    return redirect("home")

