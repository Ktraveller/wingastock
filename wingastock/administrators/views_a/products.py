import cloudinary
from django.shortcuts import render
from decimal import Decimal, InvalidOperation
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404

from sellers.models import Product

# Products management
# Product list
@login_required(login_url="login_admin")
def admin_products(request):
    products = Product.objects.all().order_by('created_at')
    return render(request, 'products_a.html', {
        'products': products
    })




# Preview product
@login_required(login_url="login_admin")
def preview_p(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'preview_a.html', {
            'product': product,
        })


# Delete product
@login_required(login_url="login_admin")
def delete_product(request, id):
    product = get_object_or_404(Product, id=id)

    # Delete image from Cloudinary
    if product.image:
        cloudinary.uploader.destroy(product.image.public_id)

    # Delete product from database
    product.delete()

    messages.success(request, "Product deleted successfully.")
    return redirect("admin_products")

