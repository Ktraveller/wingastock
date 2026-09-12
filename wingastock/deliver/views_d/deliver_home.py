from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from deliver.models import DeliveryRequest
import cloudinary.uploader
from urllib.parse import quote
from django.contrib.auth import get_user_model
from deliver.models import DeliveryRequest
from mails.models import Mails



# Deliver home
@login_required(login_url="home")
def deliver_home(request):

    delivery_requests = DeliveryRequest.objects.filter(
        customer=request.user
    ).order_by("-created_at")

    whatsapp_url = request.session.pop(
        "delivery_whatsapp_url",
        None
    )

    context = {
        "delivery_requests": delivery_requests,
        "whatsapp_url": whatsapp_url,
    }

    return render(
        request,
        "deliver_home.html",
        context
    )




# Delete request
@login_required(login_url="home")
def delete_delivery_request(request, request_id):

    delivery_request = get_object_or_404(
        DeliveryRequest,
        id=request_id,
        customer=request.user
    )

    if request.method == "POST":

        # Save information before deleting the request
        request_id_value = delivery_request.id
        title = delivery_request.title
        category = delivery_request.category
        price = delivery_request.price
        customer_note = delivery_request.customer_note

        # ---------------------------------------------------------
        # 1. Delete the admin mail related to this delivery request
        # ---------------------------------------------------------

        User = get_user_model()

        admin_users = User.objects.filter(
            is_staff=True,
            is_active=True
        ).exclude(email="")

        admin_emails = list(
            admin_users.values_list("email", flat=True)
        )

        # Delete only the mail records belonging to this request
        # and sent to admin/staff users.
        Mails.objects.filter(
            receiver_id__in=admin_emails,
            message__contains=f"Request ID: #{request_id_value}"
        ).delete()

        # ---------------------------------------------------------
        # 2. Delete image from Cloudinary
        # ---------------------------------------------------------

        if delivery_request.image:

            try:
                public_id = delivery_request.image.public_id

                if public_id:
                    cloudinary.uploader.destroy(
                        public_id,
                        resource_type="image"
                    )

            except Exception as e:

                # Do not stop database deletion if Cloudinary
                # deletion has an issue.
                print(
                    f"Cloudinary delete error: {e}"
                )

        # ---------------------------------------------------------
        # 3. Delete delivery request from database
        # ---------------------------------------------------------

        delivery_request.delete()

        # ---------------------------------------------------------
        # 4. Create WhatsApp notification for admin
        # ---------------------------------------------------------

        whatsapp_message = (
            f"Hello WingaStock Admin,\n\n"
            f"A delivery request has been deleted by the customer.\n\n"
            f"Request ID: #{request_id_value}\n"
            f"Customer: {request.user.email}\n"
            f"Product: {title}\n"
            f"Category: {category or 'Not provided'}\n"
            f"Estimated Price: "
            f"{price if price is not None else 'Not provided'}\n"
            f"Customer Note: "
            f"{customer_note or 'No note provided'}\n\n"
            f"Status: Deleted\n\n"
            f"The customer has cancelled and deleted this delivery request."
        )

        whatsapp_number = "255622652290"

        whatsapp_url = (
            f"https://wa.me/{whatsapp_number}"
            f"?text={quote(whatsapp_message)}"
        )

        # ---------------------------------------------------------
        # 5. Success message
        # ---------------------------------------------------------

        messages.success(
            request,
            f'Request "{title}" deleted successfully.'
        )

        # ---------------------------------------------------------
        # 6. Store WhatsApp URL for delivery_home
        # ---------------------------------------------------------

        request.session["delivery_whatsapp_url"] = whatsapp_url

        # ---------------------------------------------------------
        # 7. Redirect normally - NO JSON
        # ---------------------------------------------------------

        return redirect("delivery_home")

    return redirect("delivery_home")
