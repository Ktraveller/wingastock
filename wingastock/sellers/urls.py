from django.urls import path
from sellers.views_s.products import seller_payment_alert, seller_preview_p
from sellers.views_s.index import seller_home
from sellers.views_s.login_seller import seller_login, seller_logout, seller_signup, seller_terms, seller_declaration
from sellers.views_s.products import seller_add_product, seller_delete_product, seller_edit_product, seller_products, make_product_visible, make_product_hide


urlpatterns = [
    # Sellers
    path('', seller_home, name='seller_home'),
    path('products/', seller_products, name='seller_products'),
    path('preview_p/<int:id>/', seller_preview_p, name='seller_preview_p'),
    path('make_product_visible/<int:id>/', make_product_visible, name='make_product_visible'),
    path('make_product_hide/<int:id>/', make_product_hide, name='make_product_hide'),
    path('add-product/', seller_add_product, name='seller_add_product'),
    path('payment_alert/', seller_payment_alert, name='seller_payment_alert'),
    path('edit-product/<int:id>', seller_edit_product, name='seller_edit_product'),
    path('delete-product/<int:id>', seller_delete_product, name='seller_delete_product'),


    # Authentications
    path('seller_terms/', seller_terms, name='seller_terms'),
    path('seller_declaration/', seller_declaration, name='seller_declaration'),
    path('seller_signup/', seller_signup, name='signup_seller'),
    path('seller_login/', seller_login, name='login_seller'),
    path('seller_logout/', seller_logout, name='logout_seller'),
]
