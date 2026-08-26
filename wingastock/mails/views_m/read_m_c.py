from django.shortcuts import render
from django.db.models import Q
from mails.models import Mails
from django.contrib.auth.models import User
from django.db.models import OuterRef, Subquery
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required


# Message reading
@login_required(login_url="customer_login")
def mail_read_c(request, m_receiver):
    if m_receiver == 'null':
        get_senders = (
            Mails.objects
            .filter(receiver_id=request.user.email, status='unread')
            .values('sender_id')
            .distinct()
        )
        return render(request, 'c/read_message.html', { 'senders': get_senders })
    else:

        get_senders = (
            Mails.objects
            .filter(receiver_id=request.user.email, status='unread')
            .values('sender_id')
            .distinct()
        )
        messages = Mails.objects.filter(
            Q(sender_id=request.user.email, receiver_id=m_receiver) | 
            Q(sender_id=m_receiver, receiver_id=request.user.email)
            ).order_by('sent_at')
        
        # Change mail status
        messages.update(status='read')

        if request.method == 'POST':
                sender = request.user.email
                message_b = request.POST.get('message')
        
                mail = Mails.objects.create(
                    mail_id = sender,
                    sender_id = sender,
                    receiver_id = m_receiver,
                    message = message_b,
                    status = 'unread',
                    owner_id = request.user.id
                )
                mail.save()
        return render(request, 'c/read_message.html', 
                {
                    'senders': get_senders,
                    'm_receiver': m_receiver, 
                     'messages': messages,
                }
        )


# Unreaded messages
@login_required(login_url="customer_login")
def unreaded_c(request):
    get_senders = (
                Mails.objects
                .filter(receiver_id=request.user.email, status='unread')
                .values('sender_id')
                .distinct()
            )

    latest_message = Mails.objects.filter(
        receiver_id=request.user.email,
        sender_id=OuterRef('sender_id')
    ).order_by('-id')

    messages = (
        Mails.objects
        .filter(
            receiver_id=request.user.email,
            status='unread',
            id=Subquery(latest_message.values('id')[:1])
        ).order_by('-sent_at')
    )

    search_content =  (
            Mails.objects
            .filter(receiver_id=request.user.email)
            .values('sender_id')
            .distinct()
        )

    return render(request, 'c/unreaded.html', 
                  {
                       'senders': get_senders, 
                       'messages': messages, 
                       'search_result': search_content
                }
        )


# readed messages
@login_required(login_url="customer_login")
def readed_c(request):
    get_senders = (
                Mails.objects
                .filter(receiver_id=request.user.email, status='unread')
                .values('sender_id')
                .distinct()
            )

    latest_message = Mails.objects.filter(
        receiver_id=request.user.email,
        sender_id=OuterRef('sender_id')
    ).order_by('-id')

    messages = (
        Mails.objects
        .filter(
            receiver_id=request.user.email,
            status='read',
            id=Subquery(latest_message.values('id')[:1])
        ).order_by('-sent_at')
    )

    search_content =  (
            Mails.objects
            .filter(receiver_id=request.user.email)
            .values('sender_id')
            .distinct()
        )

    return render(request, 'c/readed.html', 
                  {
                       'senders': get_senders, 
                       'messages': messages, 
                       'search_result': search_content
                }
        )


# Sents mails
@login_required(login_url="customer_login")
def sent_mails_c(request):
    get_senders = (
                Mails.objects
                .filter(receiver_id=request.user.email, status='unread')
                .values('sender_id')
                .distinct()
            )

    messages = (
        Mails.objects
        .filter(
            sender_id=request.user.email)
            .values('receiver_id')
            .distinct()
        )

    search_content =  (
            Mails.objects
            .filter(receiver_id=request.user.email)
            .values('sender_id')
            .distinct()
        )

    return render(request, 'c/sent_mails.html', 
                  {
                       'senders': get_senders, 
                       'messages': messages, 
                       'search_result': search_content
                }
        )



# Compose message
@login_required(login_url="customer_login")
def compose_m_c(request, m_receiver):
    if m_receiver == 'null':
        get_receivers = User.objects.all().order_by('username')
        get_senders = (
                Mails.objects
                .filter(receiver_id=request.user.email, status='unread')
                .values('sender_id')
                .distinct()
            )
        return render(request, 'c/compose_m.html', { 'receiver': get_receivers, 'senders': get_senders })
    
    else:
        get_receivers = User.objects.all().order_by('username')
        get_senders = (
                Mails.objects
                .filter(receiver_id=request.user.email, status='unread')
                .values('sender_id')
                .distinct()
            )
        messages = Mails.objects.filter(
            Q(sender_id=request.user.email, receiver_id=m_receiver) | 
            Q(sender_id=m_receiver, receiver_id=request.user.email)
            ).order_by('sent_at')
        
        if request.method == 'POST':
                sender = request.user.email
                message_b = request.POST.get('message')
        
                mail = Mails.objects.create(
                    mail_id = sender,
                    sender_id = sender,
                    receiver_id = m_receiver,
                    message = message_b,
                    status = 'unread',
                    owner_id = request.user.id
                )
                mail.save()
        return render(request, 'c/compose_m.html', 
                    {
                    'receiver': get_receivers,
                    'm_receiver': m_receiver, 
                     'messages': messages,
                     'senders': get_senders
                    }
            )



# Delete messages
@login_required(login_url="customer_login")
def delete_mail_c(request, id):
    select_mail = get_object_or_404(Mails, id=id)

    current_user = request.user.email

    # Get the other person in the conversation
    if select_mail.sender_id == current_user:
        m_receiver = select_mail.receiver_id
    else:
        m_receiver = select_mail.sender_id

    # Delete the selected message
    select_mail.delete()

    # Redirect back to the conversation
    return redirect('mail_read_c', m_receiver=m_receiver)


# Delete all mails
@login_required(login_url="customer_login")
def clear_mails_c(request, m_receiver):
     messages = Mails.objects.filter(
                 Q(sender_id=request.user.email, receiver_id=m_receiver) | 
                 Q(sender_id=m_receiver, receiver_id=request.user.email)
                 )
     messages.delete()
     return redirect('mail_home_c')