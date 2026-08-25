from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from cloudinary.models import CloudinaryField


class Seller(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='seller'
    )
    
    seller_name = models.CharField(max_length=100)
    seller_phone = models.CharField(max_length=20)
    seller_address = models.CharField(max_length=255)
    seller_description = models.TextField()
    seller_dp = models.ImageField(upload_to='sellers/', blank=True, null=True)
    reg_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.seller_name



# Product model
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('food', 'Food'),
        ('clothes', 'Clothes'),
        ('furniture', 'Furniture'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    status = models.CharField(max_length=100, default="saved")
    image = CloudinaryField("image", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='products'
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("product_details", kwargs={"id": self.id})
