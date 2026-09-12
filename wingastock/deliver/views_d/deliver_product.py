from decimal import Decimal, InvalidOperation
from urllib.parse import quote

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from deliver.models import DeliveryRequest
from mails.models import Mails


@login_required(login_url="home")
def deliver_product(request):

    if request.method == "POST":

        image = request.FILES.get("image")
        title = request.POST.get("title", "").strip()
        category = request.POST.get("category", "").strip()
        price_value = request.POST.get("price", "").strip()
        customer_note = request.POST.get("description", "").strip()

        # -----------------------------------
        # VALIDATION
        # -----------------------------------

        if not image:
            messages.error(
                request,
                "Please upload a product image."
            )
            return redirect("deliver_product")

        if not title:
            messages.error(
                request,
                "Please enter the product name."
            )
            return redirect("deliver_product")

        # -----------------------------------
        # PRICE
        # -----------------------------------

        price = None

        if price_value:

            try:
                price = Decimal(price_value)

                if price < 0:
                    messages.error(
                        request,
                        "Price cannot be less than zero."
                    )
                    return redirect("deliver_product")

            except InvalidOperation:
                messages.error(
                    request,
                    "The price you entered is not valid."
                )
                return redirect("deliver_product")

        # -----------------------------------
        # CREATE DELIVERY REQUEST
        # -----------------------------------

        delivery_request = DeliveryRequest.objects.create(
            customer=request.user,
            image=image,
            title=title,
            category=category,
            price=price,
            customer_note=customer_note
        )

        # -----------------------------------
        # GET ADMIN / STAFF USERS ONLY
        # -----------------------------------

        User = get_user_model()

        admin_users = User.objects.filter(
            is_staff=True,
            is_active=True
        ).exclude(
            email=""
        )

        admin_emails = list(
            admin_users.values_list(
                "email",
                flat=True
            )
        )

        # -----------------------------------
        # FALLBACK ADMIN EMAIL
        # -----------------------------------

        if not admin_emails:

            fallback_email = getattr(
                settings,
                "DELIVERY_ADMIN_EMAIL",
                None
            )

            if fallback_email:
                admin_emails = [fallback_email]

        # -----------------------------------
        # IMAGE URL
        # -----------------------------------

        try:
            image_url = delivery_request.image.url
        except Exception:
            image_url = "Image uploaded successfully"

        # -----------------------------------
        # ADMIN MESSAGE
        # -----------------------------------

        admin_message = (
            f"New WingaStock Delivery Request\n\n"

            f"Request ID: #{delivery_request.id}\n"
            f"Customer: {request.user.email}\n"
            f"Product: {title}\n"
            f"Category: {category or 'Not provided'}\n"
            f"Estimated Price: "
            f"{price if price is not None else 'Not provided'}\n"
            f"Customer Note: "
            f"{customer_note or 'No note provided'}\n"
            f"Status: "
            f"{delivery_request.get_status_display()}\n\n"

            f"Product Image:\n"
            f"{image_url}\n"
        )

        # -----------------------------------
        # INTERNAL MAIL
        # ADMIN / STAFF ONLY
        # -----------------------------------

        for admin in admin_users:

            if admin.email:

                Mails.objects.create(
                    mail_id=request.user.email,
                    sender_id=request.user.email,
                    receiver_id=admin.email,
                    message=admin_message,
                    status="unread",
                    owner=request.user,
                )

        # -----------------------------------
        # EMAIL
        # ADMIN / STAFF ONLY
        # -----------------------------------

        if admin_emails:

            send_mail(
                subject=f"New delivery request: {title}",
                message=admin_message,
                from_email=getattr(
                    settings,
                    "DEFAULT_FROM_EMAIL",
                    None
                ),
                recipient_list=admin_emails,
                fail_silently=True,
            )

        # -----------------------------------
        # WHATSAPP MESSAGE
        # ADMIN NUMBER
        # 0622652290
        # -----------------------------------

        whatsapp_message = (
            f"Hello WingaStock Admin,\n\n"

            f"A new delivery request has been submitted.\n\n"

            f"Request ID: #{delivery_request.id}\n"
            f"Customer: {request.user.email}\n"
            f"Product: {title}\n"
            f"Category: {category or 'Not provided'}\n"
            f"Estimated Price: "
            f"{price if price is not None else 'Not provided'}\n"
            f"Customer Note: "
            f"{customer_note or 'No note provided'}\n"
            f"Status: "
            f"{delivery_request.get_status_display()}\n\n"

            f"Please review this delivery request."
        )

        # Convert:
        # 0622652290
        # to:
        # 255622652290

        whatsapp_number = "255622652290"

        whatsapp_url = (
            f"https://wa.me/{whatsapp_number}"
            f"?text={quote(whatsapp_message)}"
        )

        # -----------------------------------
        # SUCCESS
        # -----------------------------------

        messages.success(
            request,
            "Your delivery request has been submitted successfully."
        )

        # Store WhatsApp URL temporarily
        request.session[
            "delivery_whatsapp_url"
        ] = whatsapp_url

        return redirect("delivery_home")

    return render(
        request,
        "deliver_product.html"
    )

