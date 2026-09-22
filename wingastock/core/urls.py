from django.urls import path
from core.views.index import about, health_check, home, search, categories, favorities, terms_policy, communication
from core.views.products import preview_products, products, filter_products, react_product, submit_comments, delete_comment
from core.views.lucky import spin_page, spin, congratulations
from core.views.register import customer_register, customer_login, customer_logout
from core.views.shops import shop_lists, shop_preview
from core.views.account import user_account, user_profile, user_history, user_notification, user_support, about_us

from django.views.generic import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage


urlpatterns = [
    # Customers
    path('', home, name='home'),
    path('search/', search, name='search'),
    path('categories/', categories, name='categories'),
    path('favorites/', favorities, name='favorities'),
    
    path('products/', products, name="products"),
    path('p/<int:id>/<str:title>/', preview_products, name="product_details"),
    path('f/<str:category>', filter_products, name="filter_products"),
    path('about/', about, name='about'),
    path('terms-and-policy/', terms_policy, name='terms'),
    path('communications/', communication, name='communication'),

    #Like and dislike
    path('product-react/<int:id>/react/', react_product, name='react_product'),
    path('product-comment/<int:id>/', submit_comments, name='submit_comments'),
    path('comment-delete/<int:id>/', delete_comment, name='delete_comment'),

    # Register customers
    path('user-account/', user_account, name='customer_account'),
    path('user-profile/', user_profile, name='customer_profile'),
    path('user-history/', user_history, name='customer_history'),
    path('user-notification/', user_notification, name='customer_notification'),
    path('user-support/', user_support, name='user_support'),

    path('register/', customer_register, name='customer_register'),
    path('customer-login/', customer_login, name='customer_login'),
    path('customer-logout/', customer_logout, name='customer_logout'),

    # Lucky
    path('spin/', spin_page, name='spin'),
    path('spin/play/', spin, name='spin_play'),
    path('spin/congratulations/', congratulations, name='congratulations'),

    # Seller shops
    path('shops', shop_lists, name='shop_list'),
    path('shop/<int:id>/', shop_preview, name='shop_preview'),

    # web check
    path('ping/', health_check, name='health_check'),


    # About us
    path('about-us/', about_us, name='about_us'),
]
