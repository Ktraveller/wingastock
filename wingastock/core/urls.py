from django.urls import path
from core.views.admin_views.login_admin import admin_login, admin_logout
from core.views.admin_views.sellers import sellers
from core.views.admin_views.products import add_product, delete_product, edit_product, preview_p, admin_products
from core.views.index import about, health_check, home, search, categories, favorities, terms_policy, communication
from core.views.products import preview_products, products, filter_products
from core.views.admin_views.index import admin_home

from core.views.lucky import lucky

from django.views.generic import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage

from core.views.sellers_views.index import seller_home
from core.views.sellers_views.login_seller import seller_signup, seller_login, seller_logout
from core.views.sellers_views.products import seller_add_product, seller_delete_product, seller_edit_product, seller_preview_p, seller_products, seller_payment_alert


urlpatterns = [
    # Customers
    path('', home, name='home'),
    path('tafuta/', search, name='search'),
    path('makundi/', categories, name='categories'),
    path('pendwa/', favorities, name='favorities'),
    
    path('bidhaa/', products, name="products"),
    path('p/<int:id>', preview_products, name="product_details"),
    path('f/<str:category>', filter_products, name="filter_products"),
    path('about/', about, name='about'),
    path('terms_and_policy/', terms_policy, name='terms'),
    path('mawasiliano/', communication, name='communication'),

    # Lucky
    path('zawadi/', lucky, name='zawadi'),

    # Admin
    path('privilege/', admin_home, name='admin_home'),
    path('privilege/products/', admin_products, name='admin_products'),
    path('privilege/preview/<int:id>', preview_p, name='preview_p'),
    path('privilege/add-product/', add_product, name='add_product'),
    path('privilege/edit-product/<int:id>', edit_product, name='edit_product'),
    path('privilege/delete-product/<int:id>', delete_product, name='delete_product'),


    path('privilege/sellers/', sellers, name='admin_sellers'),

    # Sellers
    path('sellers/', seller_home, name='seller_home'),
    path('sellers/products/', seller_products, name='seller_products'),
    path('sellers/preview/<int:id>', seller_preview_p, name='seller_preview_p'),
    path('sellers/add-product/', seller_add_product, name='seller_add_product'),
    path('sellers/payment_alert/', seller_payment_alert, name='seller_payment_alert'),
    path('sellers/edit-product/<int:id>', seller_edit_product, name='seller_edit_product'),
    path('sellers/delete-product/<int:id>', seller_delete_product, name='seller_delete_product'),

    # Admin Authentication
    path('privilege/login/', admin_login, name='login_admin'),
    path('privilege/logout/', admin_logout, name='logout_admin'),
    # Sellers Authentication
    path('sellers/signup/', seller_signup, name='signup_seller'),
    path('sellers/login/', seller_login, name='login_seller'),
    path('sellers/logout/', seller_logout, name='logout_seller'),


    # web check
    path('ping/', health_check, name='health_check'),
]
