from django.urls import path
from core.views.index import about, health_check, home, search, categories, favorities, terms_policy, communication
from core.views.products import preview_products, products, filter_products, react_product, submit_comments, delete_comment
from core.views.lucky import spin_page, spin, congratulations
from core.views.register import customer_register, customer_login, customer_logout
from core.views.how_to import how1, how2, how3
from core.views.shops import shop_lists, shop_preview

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

    #Like and dislike
    path('product_react/<int:id>/react/', react_product, name='react_product'),
    path('product_comment/<int:id>/', submit_comments, name='submit_comments'),
    path('comment_delete/<int:id>/', delete_comment, name='delete_comment'),

    # Register customers
    path('register/', customer_register, name='customer_register'),
    path('customer_login/', customer_login, name='customer_login'),
    path('customer_logout/', customer_logout, name='customer_logout'),

    # Lucky
    path('spin/', spin_page, name='spin'),
    path('spin/play/', spin, name='spin_play'),
    path('spin/congratulations/', congratulations, name='congratulations'),

    # How to use wingastock
    path('how1/', how1, name='how1'),
    path('how2/', how2, name='how2'),
    path('how3/', how3, name='how3'),


    # Seller shops
    path('shops', shop_lists, name='shop_list'),
    path('shop-preview/<int:id>/', shop_preview, name='shop_preview'),

    # web check
    path('ping/', health_check, name='health_check'),
]
