from django.shortcuts import render
from decimal import Decimal, InvalidOperation
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404

from core.models import Product

# Products management
# Product list
@login_required(login_url="login_admin")
def admin_products(request):
    products = Product.objects.all().order_by('created_at')
    return render(request, 'privilege/products.html', {
        'products': products
    })





# Add product
@login_required(login_url="login_admin")
def add_product(request):
    if request.method == "POST":

        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        category = request.POST.get("category", "")
        phone = request.POST.get("phone", "").strip()
        location = request.POST.get("location", "")
        price = request.POST.get("price", "")

        # Get uploaded image
        image = request.FILES.get("image")

        # Validation
        if not title:
            messages.error(request, "Product title is required.")
            return redirect("add_product")

        if len(title) < 3:
            messages.error(request, "Title must be at least 3 characters.")
            return redirect("add_product")

        if not description:
            messages.error(request, "Description is required.")
            return redirect("add_product")

        if category not in dict(Product.CATEGORY_CHOICES):
            messages.error(request, "Invalid category selected.")
            return redirect("add_product")

        try:
            price = Decimal(price)
            if price <= 0:
                raise ValueError
        except (InvalidOperation, ValueError):
            messages.error(request, "Enter a valid price.")
            return redirect("add_product")

        if not phone:
            messages.error(request, "Phone number is required.")
            return redirect("add_product")

        if not image:
            messages.error(request, "Please upload an image.")
            return redirect("add_product")

        # Save product
        Product.objects.create(
            title=title,
            description=description,
            category=category,
            price=price,
            phone=phone,
            location=location,
            image=image,  # Uploaded to Cloudinary automatically
            owner=request.user,
        )

        messages.success(request, "Product added successfully.")
        return redirect("add_product")

    return render(request, "privilege/add_product.html")





# Edit products
@login_required(login_url="login_admin")
def edit_product(request, id):
    product = get_object_or_404(Product, id=id)

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        category = request.POST.get("category", "")
        phone = request.POST.get("phone", "").strip()
        location = request.POST.get("location", "")
        price = request.POST.get("price", "")

        # Get uploaded image
        image = request.FILES.get("image")

        # Validation
        if not title:
            messages.error(request, "Product title is required.")
            return redirect("edit_product", id=id)

        if len(title) < 3:
            messages.error(request, "Title must be at least 3 characters.")
            return redirect("edit_product", id=id)

        if not description:
            messages.error(request, "Description is required.")
            return redirect("edit_product", id=id)

        if category not in dict(Product.CATEGORY_CHOICES):
            messages.error(request, "Invalid category selected.")
            return redirect("edit_product", id=id)

        try:
            price = Decimal(price)
            if price <= 0:
                raise ValueError
        except (InvalidOperation, ValueError):
            messages.error(request, "Enter a valid price.")
            return redirect("edit_product", id=id)

        if not phone:
            messages.error(request, "Phone number is required.")
            return redirect("edit_product", id=id)

        # Update product
        product.title = title
        product.description = description
        product.category = category
        product.price = price
        product.phone = phone
        product.location = location

        # Update image only if a new one was uploaded
        if image:
            product.image = image

        product.save()

        messages.success(request, "Product updated successfully.")
        return redirect("edit_product", id=id)

    return render(
        request,
        "privilege/edit_product.html",
        {
            "selected": product,
        },
    )


# Preview product
@login_required(login_url="login_admin")
def preview_p(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'privilege/preview.html', {
            'product': product,
        })


# Delete product
@login_required(login_url="login_admin")
def delete_product(request, id):
    product = get_object_or_404(Product, id=id)

    # Delete product
    product.delete()

    messages.success(request, "Product deleted successfully.")
    return redirect("admin_products")

