from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from deliver.models import DeliveryRequest


@login_required(login_url="login_admin")
def delivery_requests(request):

    # Only staff/admin users can access this page
    if not request.user.is_staff:
        return redirect("login_admin")
    
    return render(request, "delivery_requests_a.html", {
        "delivery_requests": DeliveryRequest.objects.select_related("customer").all(),
    })


@login_required(login_url="login_admin")
def review_delivery_request(request, id):

    # Only staff/admin users can access this page
    if not request.user.is_staff:
        return redirect("login_admin")
    
    delivery_request = get_object_or_404(DeliveryRequest, id=id)
    if request.method == "POST":
        status = request.POST.get("status")
        if status not in dict(DeliveryRequest.STATUS_CHOICES):
            messages.error(request, "Invalid request status.")
        else:
            delivery_request.status = status
            delivery_request.save(update_fields=["status", "updated_at"])
            messages.success(request, "Delivery request updated.")
    return redirect("admin_delivery_requests")