from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class CustomerSpin(models.Model):

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="spins"
    )

    reward = models.TextField(
        default="empty"
    )

    reward_count = models.IntegerField(
        default=0
    )

    points = models.IntegerField(
        default=0
    )

    play_date = models.DateField(
        default=timezone.localdate
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["customer", "play_date"],
                name="one_spin_per_customer_per_day"
            )
        ]

    def __str__(self):
        return f"{self.customer.username} - {self.reward}"