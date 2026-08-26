from django.contrib import messages
import re
import uuid

from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import default_storage
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from sellers.models import Seller
import random
import string


# Login sellers
def seller_login(request):

    if request.user.is_authenticated:
        return redirect("seller_home")

    if request.method == "POST":

        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")

        # -------------------------
        # CHECK EMAIL DOMAIN
        # -------------------------

        if not email.endswith("@winga.com"):
            return render(request, "login_s.html", {
                "error": "Seller login requires a @winga.com email address."
            })

        # -------------------------
        # FIND USER
        # -------------------------

        try:
            user = User.objects.get(email__iexact=email)

        except User.DoesNotExist:
            return render(request, "login_s.html", {
                "error": "Invalid seller email or password."
            })

        # -------------------------
        # CHECK SELLER PROFILE
        # -------------------------

        try:
            seller = user.seller

        except Seller.DoesNotExist:
            return render(request, "login_s.html", {
                "error": "This account is not registered as a seller."
            })

        # -------------------------
        # CHECK PASSWORD
        # -------------------------

        user = authenticate(
            request,
            username=user.username,
            password=password
        )

        if user is not None:

            login(request, user)

            messages.success(
                request,
                "Login successfully."
            )

            return redirect("seller_home")

        # -------------------------
        # INVALID PASSWORD
        # -------------------------

        return render(request, "login_s.html", {
            "error": "Invalid seller email or password."
        })

    return render(request, "login_s.html")


# Signup sellers
def seller_signup(request):
    if request.user.is_authenticated:
        return redirect("seller_home")  # Redirect to the seller home page if already logged in

    if request.method == 'POST':

        seller_name = request.POST.get(
            'seller_name', ''
        ).strip()

        seller_phone = request.POST.get(
            'seller_phone', ''
        ).strip()

        seller_address = request.POST.get(
            'seller_address', ''
        ).strip()

        seller_description = request.POST.get(
            'seller_description', ''
        ).strip()


        errors = []

        # ==================================
        # SELLER NAME
        # ==================================

        if not seller_name:
            errors.append(
                'Seller name is required.'
            )

        elif len(seller_name) < 2:
            errors.append(
                'Seller name must contain at least 2 characters.'
            )

        elif not re.match(
            r'^[A-Za-zÀ-ÿ\s]+$',
            seller_name
        ):
            errors.append(
                'Seller name can only contain letters and spaces.'
            )


        # ==================================
        # PHONE
        # ==================================

        if not seller_phone:
            errors.append(
                'Phone number is required.'
            )

        else:

            seller_phone = re.sub(
                r'[\s\-+]',
                '',
                seller_phone
            )

            if not re.match(
                r'^255\d{9}$',
                seller_phone
            ):
                errors.append(
                    'Enter a valid Tanzanian phone number, '
                    'e.g. 255622000000.'
                )


        # ==================================
        # ADDRESS
        # ==================================

        if not seller_address:
            errors.append(
                'Address is required.'
            )

        elif len(seller_address) < 3:
            errors.append(
                'Address must contain at least 3 characters.'
            )


        # ==================================
        # DESCRIPTION
        # ==================================

        if not seller_description:
            errors.append(
                'Seller description is required.'
            )

        elif len(seller_description) < 10:
            errors.append(
                'Description must contain at least 10 characters.'
            )


        # ==================================
        # IF VALID
        # ==================================

        if not errors:

            # Check duplicate phone
            if Seller.objects.filter(
                seller_phone=seller_phone
            ).exists():

                messages.error(
                    request,
                    'A seller with this phone number already exists.'
                )

                return redirect('signup_seller')

            # ==================================
            # SAVE EVERYTHING IN SESSION
            # ==================================
            # Generate Winga email
            seller_email = generate_winga_email(
                seller_name
            )

            request.session['seller_data'] = {
                'seller_name': seller_name,
                'seller_phone': seller_phone,
                'seller_address': seller_address,
                'seller_description': seller_description,

                # Generated email
                'seller_email': seller_email,
            }

            # Make sure session is saved
            request.session.modified = True

            # Go to confirmation page
            return redirect('seller_declaration')


        # ==================================
        # VALIDATION ERRORS
        # ==================================

        for error in errors:
            messages.error(request, error)

        return render(
            request,
            'signup_s.html',
            {
                'seller_name': seller_name,
                'seller_phone': seller_phone,
                'seller_address': seller_address,
                'seller_description': seller_description,
                'open_seller_modal': True,
            }
        )


    return render(request, "signup_s.html")


# Create an email
def generate_winga_email(username):

    # Clean username
    username = username.strip().lower()

    # Remove spaces and characters that shouldn't be in an email
    username = ''.join(
        char for char in username
        if char.isalnum() or char in '._-'
    )

    # Base email
    email = f'{username}@winga.com'

    # If email doesn't exist, use it
    if not User.objects.filter(email__iexact=email).exists():
        return email

    # Email exists, generate random suffix
    while True:

        random_number = ''.join(
            random.choices(
                string.digits,
                k=4
            )
        )

        email = (
            f'{username}{random_number}'
            f'@winga.com'
        )

        # Check again
        if not User.objects.filter(
            email__iexact=email
        ).exists():

            return email



# Terms and conditions
def seller_terms(request):
    return render(request, 'terms_s.html')


# Declarations

# ==========================================
# DECLARATION
# ==========================================

def seller_declaration(request):

    # Get seller information from session
    seller_data = request.session.get('seller_data')

    # If session doesn't contain seller data
    if not seller_data:

        messages.error(
            request,
            'Seller information was not found. Please start again.'
        )

        return redirect('signup_seller')


    if request.method == 'POST':

        password = request.POST.get(
            'password',
            ''
        )

        confirm_password = request.POST.get(
            'confirm_password',
            ''
        )

        errors = []


        # ==========================================
        # PASSWORD VALIDATION
        # ==========================================

        if not password:

            errors.append(
                'Password is required.'
            )

        elif len(password) < 8:

            errors.append(
                'Password must contain at least 8 characters.'
            )


        # ==========================================
        # CONFIRM PASSWORD
        # ==========================================

        if not confirm_password:

            errors.append(
                'Please confirm your password.'
            )

        elif password != confirm_password:

            errors.append(
                'Passwords do not match.'
            )


        # ==========================================
        # GET SESSION DATA
        # ==========================================

        seller_name = seller_data.get(
            'seller_name',
            ''
        ).strip()

        seller_phone = seller_data.get(
            'seller_phone',
            ''
        ).strip()

        seller_address = seller_data.get(
            'seller_address',
            ''
        ).strip()

        seller_description = seller_data.get(
            'seller_description',
            ''
        ).strip()

        seller_email = seller_data.get(
            'seller_email',
            ''
        ).strip().lower()


        # ==========================================
        # VALIDATE SESSION DATA AGAIN
        # ==========================================

        # Seller name
        if not seller_name:

            errors.append(
                'Seller name is missing.'
            )

        elif len(seller_name) < 2:

            errors.append(
                'Seller name is invalid.'
            )


        # Phone
        if not seller_phone:

            errors.append(
                'Seller phone number is missing.'
            )

        elif not re.match(
            r'^255\d{9}$',
            seller_phone
        ):

            errors.append(
                'Seller phone number is invalid.'
            )


        # Address
        if not seller_address:

            errors.append(
                'Seller address is missing.'
            )

        elif len(seller_address) < 3:

            errors.append(
                'Seller address is invalid.'
            )


        # Description
        if not seller_description:

            errors.append(
                'Seller description is missing.'
            )

        elif len(seller_description) < 10:

            errors.append(
                'Seller description is invalid.'
            )


        # Email
        if not seller_email:

            errors.append(
                'Seller email is missing.'
            )

        elif not seller_email.endswith(
            '@winga.com'
        ):

            errors.append(
                'Seller email is invalid.'
            )


        # ==========================================
        # CHECK USER AGAIN
        # ==========================================

        if seller_email:

            if User.objects.filter(
                email__iexact=seller_email
            ).exists():

                errors.append(
                    'The generated seller email is already in use. '
                    'Please start again.'
                )


        # ==========================================
        # CHECK PHONE AGAIN
        # ==========================================

        if seller_phone:

            if Seller.objects.filter(
                seller_phone=seller_phone
            ).exists():

                errors.append(
                    'A seller with this phone number already exists.'
                )


        # ==========================================
        # IF VALIDATION FAILS
        # ==========================================

        if errors:

            for error in errors:

                messages.error(
                    request,
                    error
                )

            # Keep password values out of session.
            # Return them only to the template if needed.
            return render(
                request,
                'declaration_s.html',
                {
                    'seller': seller_data,
                }
            )


        # ==========================================
        # SAVE USER + SELLER
        # ==========================================

        try:

            with transaction.atomic():

                # ----------------------------------
                # CREATE USER
                # ----------------------------------

                user = User.objects.create(
                    username=seller_email,
                    email=seller_email,
                    password=make_password(password),
                )


                # ----------------------------------
                # CREATE SELLER
                # ----------------------------------

                seller = Seller.objects.create(
                    user=user,
                    seller_name=seller_name,
                    seller_phone=seller_phone,
                    seller_address=seller_address,
                    seller_description=seller_description,
                )


                # ----------------------------------
                # CLEAR SESSION
                # ----------------------------------

                del request.session['seller_data']

                request.session.modified = True

                # ======================================
                # LOGIN USER DIRECTLY
                # ======================================

                login(request, user)


            # ======================================
            # SUCCESS
            # ======================================

            messages.success(
                request,
                f'Congratulation "{seller_name}", Your registration to wingastock successfully.'
            )

            return redirect(
                'seller_home'
            )


        except Exception as e:

            messages.error(
                request,
                'Something went wrong while creating '
                'the seller account. Please try again.'
            )

            return render(
                request,
                'declaration_s.html',
                {
                    'seller': seller_data,
                }
            )


    # ==========================================
    # GET REQUEST
    # ==========================================

    return render(
        request,
        'declaration_s.html',
        {
            'seller': seller_data,
        }
    )


@login_required(login_url="login_seller")
def seller_logout(request):
    logout(request)
    return redirect("login_seller")  # Redirect to the seller login page after logout