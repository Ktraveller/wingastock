from django.conf import settings
from django.db import migrations, models
import cloudinary.models


class Migration(migrations.Migration):
    dependencies = [
        ("sellers", "0009_alter_product_category"),
    ]

    operations = [
        migrations.CreateModel(
            name="SellerPaymentRequest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("requested_products", models.PositiveIntegerField()),
                ("amount", models.PositiveIntegerField()),
                ("payment_reference", models.CharField(blank=True, max_length=120)),
                ("screenshot", cloudinary.models.CloudinaryField(max_length=255, verbose_name="payment screenshot")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending review"),
                            ("approved", "Approved"),
                            ("rejected", "Rejected"),
                        ],
                        default="pending",
                        max_length=20,
                    ),
                ),
                ("admin_note", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("reviewed_at", models.DateTimeField(blank=True, null=True)),
                (
                    "seller",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE,
                        related_name="seller_payment_requests",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
