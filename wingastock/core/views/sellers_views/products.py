from django.db.models.aggregates import Count
from django.shortcuts import render
from decimal import Decimal, InvalidOperation
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404

from core.models import Product

# Products management
# Product list
@login_required(login_url="login_seller")
def seller_products(request):
    products = Product.objects.all().order_by('created_at')
    return render(request, 'sellers/products.html', {
        'products': products
    })





# Add product
@login_required(login_url="login_seller")
def seller_add_product(request):

    # Check user products total
    check_products = Product.objects.filter(phone=request.user.username).count()
    if check_products > 5:
        return redirect("seller_payment_alert")
    

    if request.method == "POST":

        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        category = request.POST.get("category", "")
        location = request.POST.get("location", "")
        price = request.POST.get("price", "")

        # Get uploaded image
        image = request.FILES.get("image")

        # Validation
        if not title:
            messages.error(request, "Product title is required.")
            return redirect("seller_add_product")

        if len(title) < 3:
            messages.error(request, "Title must be at least 3 characters.")
            return redirect("seller_add_product")

        if not description:
            messages.error(request, "Description is required.")
            return redirect("seller_add_product")

        if category not in dict(Product.CATEGORY_CHOICES):
            messages.error(request, "Invalid category selected.")
            return redirect("seller_add_product")

        try:
            price = Decimal(price)
            if price <= 0:
                raise ValueError
        except (InvalidOperation, ValueError):
            messages.error(request, "Enter a valid price.")
            return redirect("seller_add_product")

        if not image:
            messages.error(request, "Please upload an image.")
            return redirect("seller_add_product")

        # Save product
        Product.objects.create(
            title=title,
            description=description,
            category=category,
            price=price,
            phone=request.user.username,
            location=location,
            image=image,  # Uploaded to Cloudinary automatically
            owner=request.user,
        )

        messages.success(request, "Product added successfully.")
        return redirect("sellers_add_product")

    return render(request, "sellers/add_product.html", {'product_remain': 5 - check_products})



# Payment alert
@login_required(login_url="login_seller")
def seller_payment_alert(request):
    return render(request, 'sellers/payment_alert.html', {})


# Edit products
@login_required(login_url="login_seller")
def seller_edit_product(request, id):
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
            return redirect("seller_edit_product", id=id)

        if len(title) < 3:
            messages.error(request, "Title must be at least 3 characters.")
            return redirect("seller_edit_product", id=id)

        if not description:
            messages.error(request, "Description is required.")
            return redirect("seller_edit_product", id=id)

        if category not in dict(Product.CATEGORY_CHOICES):
            messages.error(request, "Invalid category selected.")
            return redirect("seller_edit_product", id=id)

        try:
            price = Decimal(price)
            if price <= 0:
                raise ValueError
        except (InvalidOperation, ValueError):
            messages.error(request, "Enter a valid price.")
            return redirect("seller_edit_product", id=id)

        # Update product
        product.title = title
        product.description = description
        product.category = category
        product.price = price
        product.location = location

        # Update image only if a new one was uploaded
        if image:
            product.image = image

        product.save()

        messages.success(request, "Product updated successfully.")
        return redirect("seller_edit_product", id=id)

    return render(
        request,
        "sellers/edit_product.html",
        {
            "selected": product,
        },
    )


# Preview product
@login_required(login_url="login_seller")
def seller_preview_p(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'sellers/preview.html', {
            'product': product,
        })


# Delete product
@login_required(login_url="login_seller")
def seller_delete_product(request, id):
    product = get_object_or_404(Product, id=id)

    # Delete product
    product.delete()

    messages.success(request, "Product deleted successfully.")
    return redirect("seller_products")

