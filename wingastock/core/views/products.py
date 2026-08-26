from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from mails.models import Mails
from sellers.models import Product, Product_informations, Product_comments, ProductReaction

def products(request):
    products = Product.objects.filter(status='visible').order_by('?')

    if request.user.is_authenticated:
        mails = Mails.objects.filter(
            receiver_id=request.user.email,
            status='unread'
        ).order_by('-id')


        return render(request, 'products.html', {
        'products': products,
        'mails': mails
    })
    
    return render(request, 'products.html', {
        'products': products,
    })


def preview_products(request, id):


    if request.user.is_authenticated:

        product = get_object_or_404(
            Product,
            id=id,
            status='visible'
        )

        # Make sure session exists
        if not request.session.session_key:
            request.session.create()

        # -------------------------
        # PRODUCT INFORMATION
        # -------------------------

        product_informations, _ = Product_informations.objects.get_or_create(
            product=product,
            defaults={
                'views': 0,
                'likes': 0,
                'dislikes': 0,
            }
        )

        # -------------------------
        # VIEW COUNT
        # -------------------------

        viewed_products = request.session.get('viewed_products', {})

        # Fix old session data if it was a list
        if not isinstance(viewed_products, dict):
            viewed_products = {}

        now = timezone.now().timestamp()

        last_view = viewed_products.get(str(product.id))

        # Count once every 24 hours
        if not last_view or now - last_view >= 86400:

            product_informations.views += 1

            product_informations.save(
                update_fields=['views']
            )

            viewed_products[str(product.id)] = now

            request.session['viewed_products'] = viewed_products

        # -------------------------
        # CURRENT REACTION
        # -------------------------

        session_key = request.session.session_key

        reaction = ProductReaction.objects.filter(
            product=product,
            session_key=session_key
        ).first()


        mails = Mails.objects.filter(
            receiver_id=request.user.email,
            status='unread'
        ).order_by('-id')


        return render(request, 'product_details.html', {
        'product': product,
        'mails': mails,
        'product_informations': product_informations,
        'reaction': reaction,
    })

    product = get_object_or_404(
        Product,
        id=id,
        status='visible'
    )

    # Make sure session exists
    if not request.session.session_key:
        request.session.create()

    # -------------------------
    # PRODUCT INFORMATION
    # -------------------------

    product_informations, _ = Product_informations.objects.get_or_create(
        product=product,
        defaults={
            'views': 0,
            'likes': 0,
            'dislikes': 0,
        }
    )

    # -------------------------
    # VIEW COUNT
    # -------------------------

    viewed_products = request.session.get('viewed_products', {})

    # Fix old session data if it was a list
    if not isinstance(viewed_products, dict):
        viewed_products = {}

    now = timezone.now().timestamp()

    last_view = viewed_products.get(str(product.id))

    # Count once every 24 hours
    if not last_view or now - last_view >= 86400:

        product_informations.views += 1

        product_informations.save(
            update_fields=['views']
        )

        viewed_products[str(product.id)] = now

        request.session['viewed_products'] = viewed_products

    # -------------------------
    # CURRENT REACTION
    # -------------------------

    session_key = request.session.session_key

    reaction = ProductReaction.objects.filter(
        product=product,
        session_key=session_key
    ).first()

    return render(request, 'product_details.html', {
        'product': product,
        'product_informations': product_informations,
        'reaction': reaction,
    })



# Like ans dislike
def react_product(request, id):
    if request.method != 'POST':
        return JsonResponse(
            {'error': 'POST request required'},
            status=405
        )

    product = get_object_or_404(
        Product,
        id=id,
        status='visible'
    )

    if not request.session.session_key:
        request.session.create()

    session_key = request.session.session_key

    reaction_type = request.POST.get('reaction')

    if reaction_type not in ['like', 'dislike']:
        return JsonResponse(
            {'error': 'Invalid reaction'},
            status=400
        )

    product_informations, _ = Product_informations.objects.get_or_create(
        product=product
    )

    reaction = ProductReaction.objects.filter(
        product=product,
        session_key=session_key
    ).first()

    # -------------------------
    # NO PREVIOUS REACTION
    # -------------------------

    if reaction is None:

        ProductReaction.objects.create(
            product=product,
            session_key=session_key,
            reaction=reaction_type
        )

        if reaction_type == 'like':
            product_informations.likes += 1
        else:
            product_informations.dislikes += 1

    # -------------------------
    # SAME REACTION AGAIN
    # -------------------------

    elif reaction.reaction == reaction_type:

        return JsonResponse({
            'success': False,
            'message': 'You already reacted to this product.',
            'likes': product_informations.likes,
            'dislikes': product_informations.dislikes,
        })

    # -------------------------
    # CHANGE REACTION
    # -------------------------

    else:

        old_reaction = reaction.reaction

        reaction.reaction = reaction_type
        reaction.save(update_fields=['reaction'])

        if old_reaction == 'like':
            product_informations.likes -= 1
            product_informations.dislikes += 1
        else:
            product_informations.dislikes -= 1
            product_informations.likes += 1

    product_informations.save(
        update_fields=['likes', 'dislikes']
    )

    return JsonResponse({
        'success': True,
        'reaction': reaction_type,
        'likes': product_informations.likes,
        'dislikes': product_informations.dislikes,
    })


# customer comments
@login_required(login_url="customer_login")
def submit_comments(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        comments = request.POST.get('comments')
        Product_comments.objects.create(
            product=product,
            customer=request.user,
            comment=comments
        )
        return redirect('product_details', id=id)

# Comment delete
@login_required(login_url="customer_login")
def delete_comment(request, id):
    comment = get_object_or_404(Product_comments, id=id, customer=request.user)
    product = comment.product.id
    comment.delete()

    return redirect('product_details', id=product)
    

def filter_products(request, category):
    products = Product.objects.order_by('?').filter(category=category, status='visible')

    if request.user.is_authenticated:
        mails = Mails.objects.filter(
            receiver_id=request.user.email,
            status='unread'
        ).order_by('-id')


        return render(request, 'products.html', {
        'products': products,
        'mails': mails
    })

    return render(request, 'products.html', {
        'products': products,
        'mails': mails,
    })

