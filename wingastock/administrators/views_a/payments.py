from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from sellers.models import SellerPaymentRequest


@login_required(login_url="login_admin")
def payment_requests(request):

    # Only staff/admin users can access this page
    if not request.user.is_staff:
        return redirect("login_admin")
    
    requests = SellerPaymentRequest.objects.select_related("seller").all()
    return render(request, "payment_requests_a.html", {
        "payment_requests": requests,
    })


@login_required(login_url="login_admin")
def review_payment_request(request, id):

    # Only staff/admin users can access this page
    if not request.user.is_staff:
        return redirect("login_admin")
    
    payment_request = get_object_or_404(SellerPaymentRequest, id=id)

    if request.method != "POST":
        return redirect("admin_payment_requests")

    status = request.POST.get("status", "")
    if status not in {"approved", "rejected", "pending"}:
        messages.error(request, "Invalid payment review status.")
        return redirect("admin_payment_requests")

    payment_request.status = status
    payment_request.admin_note = request.POST.get("admin_note", "").strip()
    payment_request.reviewed_at = timezone.now() if status != "pending" else None
    payment_request.save(update_fields=["status", "admin_note", "reviewed_at"])

    messages.success(request, "Payment request review updated.")
    return redirect("admin_payment_requests")
