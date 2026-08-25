from django.db import models
from django.contrib.auth.models import User


# Mails model
class Mails(models.Model):
    mail_id = models.CharField(max_length=20, blank=False, null=False)
    sender_id = models.CharField(max_length=20, blank=False, null=False)
    receiver_id = models.CharField(max_length=20, blank=False, null=False)
    message = models.TextField()
    status = models.CharField(max_length=100, default='unreaded')
    sent_at = models.DateTimeField(auto_now_add=True)
    #sent_by = models.CharField(max_length=20, blank=False, null=False)

    owner = models.ForeignKey(User, on_delete=models.CASCADE)