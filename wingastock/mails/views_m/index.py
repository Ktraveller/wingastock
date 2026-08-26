from django.db.models import Q
from django.shortcuts import render
from mails.models import Mails
from django.contrib.auth.decorators import login_required

# Mail Home Seller
@login_required(login_url="login_seller")
def mail_index(request):
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