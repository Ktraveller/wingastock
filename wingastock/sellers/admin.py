from django.contrib import admin
from django.utils import timezone
from .models import SellerPaymentRequest


@admin.register(SellerPaymentRequest)
class SellerPaymentRequestAdmin(admin.ModelAdmin):
    list_display = ("seller", "requested_products", "amount", "status", "created_at", "reviewed_at")
    list_filter = ("status", "created_at")
    search_fields = ("seller__email", "payment_reference")
    readonly_fields = ("created_at",)

    def save_model(self, request, obj, form, change):
        if obj.status in {"approved", "rejected"} and not obj.reviewed_at:
            obj.reviewed_at = timezone.now()
        super().save_model(request, obj, form, change)
