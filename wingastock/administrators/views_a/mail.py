from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from mails.models import Mails


@login_required(login_url="login_admin")
def admin_mail(request):

    # Only staff/admin users can access this page
    if not request.user.is_staff:
        return redirect("login_admin")
    
    messages = Mails.objects.filter(receiver_id=request.user.email).order_by("-sent_at")
    return render(request, "mail_a.html", {"messages": messages})