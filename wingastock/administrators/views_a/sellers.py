from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from sellers.models import Seller, Product
from cloudinary import uploader
from django.contrib.auth.models import User


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

    # --------------------------------
    # DELETE SELLER PROFILE PICTURE
    # --------------------------------
    if seller.seller_dp:

        try:
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
    # RETURN TO SELLERS PAGE
    # --------------------------------
    return redirect("admin_sellers")