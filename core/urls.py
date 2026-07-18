from django.urls import path
from core.views.admin_views.login_admin import admin_login, admin_logout
from core.views.admin_views.sellers import sellers
from core.views.admin_views.products import add_product, delete_product, edit_product, preview_p, admin_products
from core.views.index import about, health_check, home
from core.views.products import preview_products, products, filter_products
from core.views.admin_views.index import admin_home

from django.views.generic import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage


urlpatterns = [
    # Customers
    path('', home, name='home'),
    path('bidhaa/', products, name="products"),
    path('p/<int:id>', preview_products, name="product_details"),
    path('f/<str:category>', filter_products, name="filter_products"),
    path('about/', about, name='about'),



    # Admin
    path('privilege/', admin_home, name='admin_home'),
    path('privilege/products/', admin_products, name='admin_products'),
    path('privilege/preview/<int:id>', preview_p, name='preview_p'),
    path('privilege/add-product/', add_product, name='add_product'),
    path('privilege/edit-product/<int:id>', edit_product, name='edit_product'),
    path('privilege/delete-product/<int:id>', delete_product, name='delete_product'),


    path('privilege/sellers/', sellers, name='admin_sellers'),


    # Admin Authentication
    path('privilege/login/', admin_login, name='login_admin'),
    path('privilege/logout/', admin_logout, name='logout_admin'),


    path(
        "robots.txt",
        RedirectView.as_view(
            url=staticfiles_storage.url("robots.txt"),
            permanent=True
        ),
    ),

    # web check
    path('ping/', health_check, name='health_check'),
]