from django.db import models
from django.contrib.auth.models import User

from sellers.models import Product


class Customer(models.Model):

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='product_views'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='customer_views'
    )

    view_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.username} viewed {self.product}"
