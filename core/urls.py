from django.urls import path
from core.views.admin_views.login_admin import admin_login, admin_logout
from core.views.admin_views.messages import messages
from core.views.admin_views.products import add_product, delete_product, edit_product, admin_products
from core.views.admin_views.statistics import statistics
from core.views.admin_views.users import users
from core.views.index import home
from core.views.products import preview_products, products, filter_products
from core.views.admin_views.index import admin_home
from core.views.admin_views.settings import settings


urlpatterns = [
    # Customers
    path('', home, name='home'),
    path('products/', products, name="products"),
    path('product-preview/<int:id>', preview_products, name="product_details"),
    path('product-preview/<str:category>', filter_products, name="filter_products"),



    # Admin
    path('privilege/', admin_home, name='admin_home'),
    path('privilege/users/', users, name='admin_users'),
    path('privilege/products/', admin_products, name='admin_products'),
    path('privilege/add-product/', add_product, name='add_product'),
    path('privilege/edit-product/<int:id>', edit_product, name='edit_product'),
    path('privilege/delete-product/<int:id>', delete_product, name='delete_product'),


    path('privilege/messages/', messages, name='admin_messages'),
    path('privilege/statistics/', statistics, name='admin_statistics'),
    path('privilege/settings/', settings, name='admin_settings'),


    # Admin Authentication
    path('privilege/login/', admin_login, name='login_admin'),
    path('privilege/logout/', admin_logout, name='logout_admin')
]