from django.urls import path
from core.views.index import about, health_check, home, search, categories, favorities, terms_policy, communication
from core.views.products import preview_products, products, filter_products
from core.views.lucky import lucky
from core.views.register import customer_register, customer_login, customer_logout

from django.views.generic import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage


urlpatterns = [
    # Customers
    path('', home, name='home'),
    path('search/', search, name='search'),
    path('categories/', categories, name='categories'),
    path('favorites/', favorities, name='favorities'),
    
    path('products/', products, name="products"),
    path('p/<int:id>', preview_products, name="product_details"),
    path('f/<str:category>', filter_products, name="filter_products"),
    path('about/', about, name='about'),
    path('terms_and_policy/', terms_policy, name='terms'),
    path('communications/', communication, name='communication'),


    # Register customers
    path('register/', customer_register, name='customer_register'),
    path('customer_login/', customer_login, name='customer_login'),
    path('customer_logout/', customer_logout, name='customer_logout'),

    # Lucky
    path('zawadi/', lucky, name='zawadi'),

    # web check
    path('ping/', health_check, name='health_check'),
]
