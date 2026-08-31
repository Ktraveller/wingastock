from django.urls import path
from administrators.views_a.login_admin import admin_login, admin_logout
from administrators.views_a.index import admin_home
from administrators.views_a.products import admin_products, delete_product, preview_p
from administrators.views_a.sellers import sellers, delete_seller

urlpatterns = [
    path('', admin_home, name='admin_home'),
    path('products_a/', admin_products, name='admin_products'),
    path('sellers_a/', sellers, name='admin_sellers'),
    path('seller_delete_a/<int:id>/', delete_seller, name='delete_seller'),
    path('privilege_a/preview/<int:id>', preview_p, name='admin_preview_p'),
    path('privilege_a/delete-product/<int:id>', delete_product, name='delete_product'),

    # Authentications
    path('login_a/', admin_login, name='login_admin'),
    path('logout_a/', admin_logout, name='logout_admin'),
]
