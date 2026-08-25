from django.urls import path
from administrators.views_a.login_admin import admin_login, admin_logout
from administrators.views_a.index import admin_home
from administrators.views_a.products import admin_products
from administrators.views_a.sellers import sellers

urlpatterns = [
    path('', admin_home, name='admin_home'),
    path('products/', admin_products, name='admin_products'),
    path('sellers/', sellers, name='admin_sellers'),

    # Authentications
    path('login/', admin_login, name='login_admin'),
    path('logout/', admin_logout, name='logout_admin'),
]
