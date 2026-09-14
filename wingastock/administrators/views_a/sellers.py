from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from sellers.models import Seller, Product
from cloudinary import uploader
from django.contrib.auth.models import User
from django.contrib import messages

import cloudinary 
from sellers.models import Seller 
from deliver.models import DeliveryRequest 
from mails.models import Mails


# Get sellers
@login_required(login_url="login_admin")
def sellers(request):

    # Only staff/admin users can access this page
    if not request.user.is_staff:
        return redirect("login_admin")

    sellers_list = Seller.objects.all().order_by('id').distinct()

    return render(request, 'sellers_a.html', {
        'sellers_list': sellers_list
    })




# Delete seller view
@login_required(login_url="login_admin")
def delete_seller(request, id):

    # Only staff/admin users can access this page
    if not request.user.is_staff:
        return redirect("login_admin")

    seller = get_object_or_404(Seller, id=id)
    user = seller.user

    # Save seller name before deleting
    seller_name = seller.seller_name

    # --------------------------------
    # DELETE SELLER PROFILE PICTURE
    # --------------------------------
    if seller.seller_dp:

        try:
            if seller.seller_dp.public_id:
                uploader.destroy(
                    seller.seller_dp.public_id,
                    resource_type="image"
                )

        except Exception as e:
            print(f"Seller DP Cloudinary delete error: {e}")

    # --------------------------------
    # GET ALL SELLER PRODUCTS
    # --------------------------------
    products = Product.objects.filter(owner=user)

    # --------------------------------
    # DELETE PRODUCT IMAGES
    # FROM CLOUDINARY
    # --------------------------------
    for product in products:

        if product.image:

            try:
                public_id = product.image.public_id

                if public_id:
                    uploader.destroy(
                        public_id,
                        resource_type="image"
                    )

            except Exception as e:
                print(
                    f"Product image delete error "
                    f"for product {product.id}: {e}"
                )

    # --------------------------------
    # DELETE PRODUCTS FROM DATABASE
    # --------------------------------
    products.delete()

    # --------------------------------
    # DELETE SELLER FROM DATABASE
    # --------------------------------
    seller.delete()

    # --------------------------------
    # DELETE USER ACCOUNT
    # --------------------------------
    user.delete()

    # --------------------------------
    # SUCCESS MESSAGE
    # --------------------------------
    messages.success(
        request,
        f'Seller "{seller_name}" and all related products were deleted successfully.'
    )

    # --------------------------------
    # RETURN TO SELLERS PAGE
    # --------------------------------
    return redirect("admin_sellers")



# Customers
@login_required(login_url="login_admin")
def customers(request):

    # Only staff/admin users can access this page
    if not request.user.is_staff:
        return redirect("login_admin")

    # Get normal customer users:
    # - Active users
    # - Not staff
    # - Not superusers
    # - Not registered as sellers
    customers_list = (
        User.objects
        .filter(
            is_staff=False,
            is_superuser=False
        )
        .exclude(
            id__in=Seller.objects.values_list(
                'user_id',
                flat=True
            )
        )
        .order_by('id')
        .distinct()
    )

    return render(request, 'customers_a.html', {
        'customers_list': customers_list
    })




# Delete customer
@login_required(login_url="login_admin")
def delete_customer(request, id):

    # Only staff/admin users can delete customers
    if not request.user.is_staff:
        return redirect("login_admin")

    # Get the user
    customer = get_object_or_404(User, id=id)

    # Do not allow admin/staff accounts to be deleted
    if customer.is_staff or customer.is_superuser:
        messages.error(
            request,
            "You cannot delete an admin or staff account."
        )
        return redirect("admin_customers")

    # Do not allow sellers to be deleted from the customer page
    if Seller.objects.filter(user=customer).exists():
        messages.error(
            request,
            "This user is a seller and cannot be deleted from the customer page."
        )
        return redirect("admin_customers")

    customer_name = customer.username or customer.email

    # ---------------------------------------------------------
    # DELETE CUSTOMER DELIVERY REQUESTS + CLOUDINARY IMAGES
    # ---------------------------------------------------------

    delivery_requests = DeliveryRequest.objects.filter(
        customer=customer
    )

    for delivery_request in delivery_requests:

        # Delete delivery image from Cloudinary
        if delivery_request.image:
            try:
                public_id = delivery_request.image.public_id

                if public_id:
                    cloudinary.uploader.destroy(
                        public_id,
                        resource_type="image"
                    )

            except Exception:
                # Continue deleting the customer even if
                # Cloudinary deletion fails
                pass

    # Delete delivery request records from database
    delivery_requests.delete()

    # ---------------------------------------------------------
    # DELETE SAVED MAILS BELONGING TO THIS CUSTOMER
    # ---------------------------------------------------------

    Mails.objects.filter(
        owner=customer
    ).delete()

    # ---------------------------------------------------------
    # DELETE CUSTOMER ACCOUNT
    # ---------------------------------------------------------

    customer.delete()

    messages.success(
        request,
        f'Customer "{customer_name}" and all related delivery requests, '
        f'images, and saved mails were deleted successfully.'
    )

    return redirect("admin_customers")