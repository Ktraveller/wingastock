from django.db.models import Q
from django.shortcuts import render, redirect
from mails.models import Mails
from django.contrib.auth.decorators import login_required

# Mail Home Seller
@login_required(login_url="login_seller")
def mail_index(request):

    # User must have a Seller profile
    if not hasattr(request.user, "seller"):
        return redirect("login_seller") 
    
     # Change mail status
    messages = Mails.objects.filter(receiver_id=request.user.email, status='sent')
    messages.update(status='unread')
    
    get_senders = (
    Mails.objects
    .filter(receiver_id=request.user.email, status='unread')
    .values('sender_id')
    .distinct()
)

    search_content =  (
        Mails.objects
        .filter(receiver_id=request.user.email)
        .values('sender_id')
        .distinct()
    )

    return render(request, 'index_m.html', {
        'senders': get_senders,
        'search_result': search_content
    })


# Mail home customer
@login_required(login_url="customer_login")
def mail_index_c(request):
     # Change mail status
    messages = Mails.objects.filter(receiver_id=request.user.email, status='sent')
    messages.update(status='unread')
    
    get_senders = (
    Mails.objects
    .filter(receiver_id=request.user.email, status='unread')
    .values('sender_id')
    .distinct()
)

    search_content =  (
        Mails.objects
        .filter(receiver_id=request.user.email)
        .values('sender_id')
        .distinct()
    )

    return render(request, 'c/index_m.html', {
        'senders': get_senders,
        'search_result': search_content
    })




# Mail home admin
@login_required(login_url="login_admin")
def mail_index_a(request):

    # Only staff/admin users can access this page
    if not request.user.is_staff:
        return redirect("login_admin")
    
     # Change mail status
    messages = Mails.objects.filter(receiver_id=request.user.email, status='sent')
    messages.update(status='unread')
    
    get_senders = (
    Mails.objects
    .filter(receiver_id=request.user.email, status='unread')
    .values('sender_id')
    .distinct()
)

    search_content =  (
        Mails.objects
        .filter(receiver_id=request.user.email)
        .values('sender_id')
        .distinct()
    )

    return render(request, 'a/index_m.html', {
        'senders': get_senders,
        'search_result': search_content
    })