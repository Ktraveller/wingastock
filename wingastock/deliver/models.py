from django.db import models
from django.conf import settings
from cloudinary.models import CloudinaryField


class DeliveryRequest(models.Model):
	STATUS_CHOICES = [
		("pending", "Pending"),
		("processing", "Processing"),
		("processed", "Processed"),
		("rejected", "Rejected"),
	]

	customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="delivery_requests")
	image = CloudinaryField("delivery image", folder="deliver")
	title = models.CharField(max_length=200)
	category = models.CharField(max_length=100, blank=True)
	price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
	customer_note = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["-created_at"]

	def __str__(self):
		return f"{self.title} - {self.customer.email} ({self.status})"
