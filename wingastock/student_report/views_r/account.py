from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Dashboard
@login_required(login_url="home")
def account_report(request):
    return render(request, 'account_re.html')