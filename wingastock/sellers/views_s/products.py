from django.db.models.aggregates import Count
from django.shortcuts import render
from decimal import Decimal, InvalidOperation
from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
import cloudinary
from sellers.models import Product, Seller

# Products management
# Product list
def seller_products(request):
    products = Product.objects.filter(
        owner=request.user
        ).order_by('created_at')
    
    return render(request, 'products_s.html', {
        'products': products
    })





# Add product
@login_required(login_url="login_seller")
def seller_add_product(request):

    # ==========================================
    # CHECK USER
    # ==========================================

    if not request.user.is_authenticated:
        messages.error(
            request,
            "Please login first."
        )
        return redirect("login")



    # ==========================================
    # CHECK PRODUCT LIMIT
    # ==========================================

    check_products = Product.objects.filter(
        owner=request.user
    ).count()

    MAX_PRODUCTS = 5

    if check_products >= MAX_PRODUCTS:

        return redirect(
            "seller_payment_alert"
        )


    # ==========================================
    # POST
    # ==========================================

    if request.method == "POST":

        title = request.POST.get(
            "title",
            ""
        ).strip()

        description = request.POST.get(
            "description",
            ""
        ).strip()

        category = request.POST.get(
            "category",
            ""
        ).strip()

        price_input = request.POST.get(
            "price",
            ""
        ).strip()

        image = request.FILES.get(
            "image"
        )


        # ======================================
        # TITLE VALIDATION
        # ======================================

        if not title:

            messages.error(
                request,
                "Product title is required."
            )

            return redirect(
                "seller_add_product"
            )


        if len(title) < 3:

            messages.error(
                request,
                "Title must be at least 3 characters."
            )

            return redirect(
                "seller_add_product"
            )


        if len(title) > 150:

            messages.error(
                request,
                "Title cannot exceed 150 characters."
            )

            return redirect(
                "seller_add_product"
            )


        # ======================================
        # DESCRIPTION VALIDATION
        # ======================================

        if not description:

            messages.error(
                request,
                "Description is required."
            )

            return redirect(
                "seller_add_product"
            )


        if len(description) < 10:

            messages.error(
                request,
                "Description must be at least 10 characters."
            )

            return redirect(
                "seller_add_product"
            )


        if len(description) > 5000:

            messages.error(
                request,
                "Description is too long."
            )

            return redirect(
                "seller_add_product"
            )


        # ======================================
        # CATEGORY VALIDATION
        # ======================================

        valid_categories = dict(
            Product.CATEGORY_CHOICES
        )

        if category not in valid_categories:

            messages.error(
                request,
                "Invalid category selected."
            )

            return redirect(
                "seller_add_product"
            )


        # ======================================
        # PRICE VALIDATION
        # ======================================

        if not price_input:

            messages.error(
                request,
                "Product price is required."
            )

            return redirect(
                "seller_add_product"
            )


        try:

            price = Decimal(price_input)

        except (InvalidOperation, ValueError):

            messages.error(
                request,
                "Enter a valid price."
            )

            return redirect(
                "seller_add_product"
            )


        if not price.is_finite():

            messages.error(
                request,
                "Invalid price."
            )

            return redirect(
                "seller_add_product"
            )


        if price <= 0:

            messages.error(
                request,
                "Price must be greater than zero."
            )

            return redirect(
                "seller_add_product"
            )


        # Optional maximum price
        if price > Decimal("999999999999"):

            messages.error(
                request,
                "Price is too high."
            )

            return redirect(
                "seller_add_product"
            )


        # ======================================
        # IMAGE VALIDATION
        # ======================================

        if not image:

            messages.error(
                request,
                "Please upload an image."
            )

            return redirect(
                "seller_add_product"
            )


        # Maximum image size = 5MB
        MAX_IMAGE_SIZE = 5 * 1024 * 1024

        if image.size > MAX_IMAGE_SIZE:

            messages.error(
                request,
                "Image must not exceed 5MB."
            )

            return redirect(
                "seller_add_product"
            )


        # ======================================
        # IMAGE TYPE VALIDATION
        # ======================================

        allowed_types = [
            "image/jpeg",
            "image/png",
            "image/webp",
        ]

        if image.content_type not in allowed_types:

            messages.error(
                request,
                "Only JPG, PNG, and WEBP images are allowed."
            )

            return redirect(
                "seller_add_product"
            )


        # ======================================
        # IMAGE EXTENSION VALIDATION
        # ======================================

        allowed_extensions = [
            ".jpg",
            ".jpeg",
            ".png",
            ".webp",
        ]

        image_name = image.name.lower()

        if not any(
            image_name.endswith(ext)
            for ext in allowed_extensions
        ):

            messages.error(
                request,
                "Invalid image file."
            )

            return redirect(
                "seller_add_product"
            )


        # ======================================
        # DUPLICATE PRODUCT CHECK
        # ======================================

        duplicate_product = Product.objects.filter(
            owner=request.user,
            title__iexact=title
        ).exists()

        if duplicate_product:

            messages.error(
                request,
                "You already have a product with this title."
            )

            return redirect(
                "seller_add_product"
            )


        # ======================================
        # CREATE PRODUCT
        # ======================================

        Product.objects.create(
            title=title,
            description=description,
            price=price,
            category=category,

            image=image,

            owner=request.user,
        )


        # ======================================
        # SUCCESS
        # ======================================

        messages.success(
            request,
            "Product added successfully."
        )

        return redirect(
            "seller_add_product"
        )


    # ==========================================
    # GET
    # ==========================================

    return render(
        request,
        "add_product_s.html",
        {
            "product_remain":
                MAX_PRODUCTS - check_products
        }
    )




# Payment alert
@login_required(login_url="login_seller")
def seller_payment_alert(request):
    return render(request, 'payment_alert_s.html', {})


# Edit products
@login_required(login_url="login_seller")
def seller_edit_product(request, id):

    # ==========================================
    # GET PRODUCT
    # ==========================================

    product = get_object_or_404(
        Product,
        id=id,
        owner=request.user
    )


    # ==========================================
    # POST
    # ==========================================

    if request.method == "POST":

        title = request.POST.get(
            "title",
            ""
        ).strip()

        description = request.POST.get(
            "description",
            ""
        ).strip()

        category = request.POST.get(
            "category",
            ""
        ).strip()

        price_input = request.POST.get(
            "price",
            ""
        ).strip()

        image = request.FILES.get(
            "image"
        )


        # ======================================
        # TITLE VALIDATION
        # ======================================

        if not title:

            messages.error(
                request,
                "Product title is required."
            )

            return redirect(
                "seller_edit_product",
                id=id
            )


        if len(title) < 3:

            messages.error(
                request,
                "Title must be at least 3 characters."
            )

            return redirect(
                "seller_edit_product",
                id=id
            )


        if len(title) > 150:

            messages.error(
                request,
                "Title cannot exceed 150 characters."
            )

            return redirect(
                "seller_edit_product",
                id=id
            )


        # ======================================
        # DESCRIPTION VALIDATION
        # ======================================

        if not description:

            messages.error(
                request,
                "Description is required."
            )

            return redirect(
                "seller_edit_product",
                id=id
            )


        if len(description) < 10:

            messages.error(
                request,
                "Description must be at least 10 characters."
            )

            return redirect(
                "seller_edit_product",
                id=id
            )


        if len(description) > 5000:

            messages.error(
                request,
                "Description is too long."
            )

            return redirect(
                "seller_edit_product",
                id=id
            )


        # ======================================
        # CATEGORY VALIDATION
        # ======================================

        valid_categories = dict(
            Product.CATEGORY_CHOICES
        )

        if category not in valid_categories:

            messages.error(
                request,
                "Invalid category selected."
            )

            return redirect(
                "seller_edit_product",
                id=id
            )


        # ======================================
        # PRICE VALIDATION
        # ======================================

        if not price_input:

            messages.error(
                request,
                "Product price is required."
            )

            return redirect(
                "seller_edit_product",
                id=id
            )


        try:

            price = Decimal(
                price_input
            )

        except (InvalidOperation, ValueError):

            messages.error(
                request,
                "Enter a valid price."
            )

            return redirect(
                "seller_edit_product",
                id=id
            )


        # Check NaN / Infinity

        if not price.is_finite():

            messages.error(
                request,
                "Invalid price."
            )

            return redirect(
                "seller_edit_product",
                id=id
            )


        if price <= 0:

            messages.error(
                request,
                "Price must be greater than zero."
            )

            return redirect(
                "seller_edit_product",
                id=id
            )


        # Maximum price

        if price > Decimal("999999999999"):

            messages.error(
                request,
                "Price is too high."
            )

            return redirect(
                "seller_edit_product",
                id=id
            )


        # ======================================
        # IMAGE VALIDATION
        # ======================================
        #
        # Unlike ADD:
        # image is NOT required during edit.
        #
        # If user doesn't upload a new image,
        # the old image remains.
        # ======================================

        if image:

            # Maximum 5MB

            MAX_IMAGE_SIZE = 5 * 1024 * 1024

            if image.size > MAX_IMAGE_SIZE:

                messages.error(
                    request,
                    "Image must not exceed 5MB."
                )

                return redirect(
                    "seller_edit_product",
                    id=id
                )


            # ==================================
            # IMAGE TYPE
            # ==================================

            allowed_types = [
                "image/jpeg",
                "image/png",
                "image/webp",
            ]

            if image.content_type not in allowed_types:

                messages.error(
                    request,
                    "Only JPG, PNG, and WEBP images are allowed."
                )

                return redirect(
                    "seller_edit_product",
                    id=id
                )


            # ==================================
            # IMAGE EXTENSION
            # ==================================

            allowed_extensions = [
                ".jpg",
                ".jpeg",
                ".png",
                ".webp",
            ]

            image_name = image.name.lower()

            if not any(
                image_name.endswith(ext)
                for ext in allowed_extensions
            ):

                messages.error(
                    request,
                    "Invalid image file."
                )

                return redirect(
                    "seller_edit_product",
                    id=id
                )


        # ======================================
        # DUPLICATE PRODUCT CHECK
        # ======================================

        duplicate_product = Product.objects.filter(
            owner=request.user,
            title__iexact=title
        ).exclude(
            id=product.id
        ).exists()


        if duplicate_product:

            messages.error(
                request,
                "You already have another product with this title."
            )

            return redirect(
                "seller_edit_product",
                id=id
            )


        # ======================================
        # UPDATE PRODUCT
        # ======================================

        product.title = title

        product.description = description

        product.category = category

        product.price = price


        # ======================================
        # UPDATE IMAGE ONLY IF NEW IMAGE EXISTS
        # ======================================

        if image:
            # Delete old image from Cloudinary
            if product.image:
                cloudinary.uploader.destroy(product.image.public_id)

            # Save new image
            product.image = image

        product.save()



        # ======================================
        # SUCCESS
        # ======================================

        messages.success(
            request,
            "Product updated successfully."
        )

        return redirect(
            "seller_edit_product",
            id=id
        )


    # ==========================================
    # GET
    # ==========================================

    return render(
        request,
        "edit_product_s.html",
        {
            "selected": product,
        }
    )


# Preview product
@login_required(login_url="login_seller")
def seller_preview_p(request, id):
    product = get_object_or_404(
            Product,
            id=id,
            owner=request.user
        )
    return render(request, 'preview_s.html', {
            'product': product,
        })


# Delete product
@login_required(login_url="login_seller")
def seller_delete_product(request, id):
    product = get_object_or_404(
            Product,
            id=id,
            owner=request.user
        )

    # Delete image from Cloudinary
    if product.image:
        cloudinary.uploader.destroy(product.image.public_id)

    # Delete product from database
    product.delete()

    messages.success(request, "Product deleted successfully.")
    return redirect("seller_products")


# Make product visible
@login_required(login_url="login_seller")
def make_product_visible(request, id):
    product = get_object_or_404(
            Product,
            id=id,
            owner=request.user
        )

    product.status = 'visible'
    product.save()

    messages.success(
        request,
            "Product now visible to customers"
    )

    return redirect(
        "seller_preview_p",
        id=id
    )


# Hide product
@login_required(login_url="login_seller")
def make_product_hide(request, id):
    product = get_object_or_404(
            Product,
            id=id,
            owner=request.user
        )

    product.status = 'saved'
    product.save()

    messages.success(
        request,
            "Product now hidded to customers"
    )

    return redirect(
        "seller_preview_p",
        id=id
    )