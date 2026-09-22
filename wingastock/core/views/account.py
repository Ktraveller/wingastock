from django.shortcuts import render

from mails.models import Mails


# User account
def user_account(request):
    return render(request, 'account.html', {
    })


# User profile
def user_profile(request):
    return render(request, 'profile.html', {
    })



# Search history
def user_history(request):
    return render(request, 'search-history.html', {
    })


# Notification
def user_notification(request):

    if request.user.is_authenticated:
        mails = Mails.objects.filter(
            receiver_id=request.user.email,
            status='unread'
        ).order_by('-id')


        return render(request, 'notifications.html', {
        'mails': mails
    })

    return render(request, 'notifications.html', {
    })



# Support
def user_support(request):
    return render(request, 'support.html', {
    })


# About us
def about_us(request):
    return render(request, 'about-us.html', {
    })