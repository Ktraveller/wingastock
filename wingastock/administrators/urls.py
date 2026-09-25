from django.urls import path
from administrators.views_a.login_admin import admin_login, admin_logout
from administrators.views_a.index import admin_home
from administrators.views_a.products import admin_products, delete_product, preview_p
from administrators.views_a.sellers import sellers, delete_seller, customers, delete_customer
from administrators.views_a.payments import payment_requests, review_payment_request
from administrators.views_a.delivery import delivery_requests, review_delivery_request
from administrators.views_a.mail import admin_mail
from administrators.views_a.field_report_a import field_report_a, report_preview_a

urlpatterns = [
    path('', admin_home, name='admin_home'),
    path('products_a/', admin_products, name='admin_products'),
    path('sellers_a/', sellers, name='admin_sellers'),
    path('seller_delete_a/<int:id>/', delete_seller, name='delete_seller'),
    path('payment-requests/', payment_requests, name='admin_payment_requests'),
    path('payment-requests/<int:id>/review/', review_payment_request, name='admin_review_payment'),
    path('delivery-requests/', delivery_requests, name='admin_delivery_requests'),
    path('delivery-requests/<int:id>/review/', review_delivery_request, name='admin_review_delivery'),
    path('mail/', admin_mail, name='admin_mail'),
    path('privilege_a/preview/<int:id>', preview_p, name='admin_preview_p'),
    path('privilege_a/delete-product/<int:id>', delete_product, name='delete_product'),

    path('customers-a/', customers, name="admin_customers"),
    path('delete-customer/<int:id>/', delete_customer, name="delete_customer"),

    # Report
    path('field-report-list/', field_report_a, name='field_report_list'),
    path(
        "report-preview/<int:id>/",
        report_preview_a,
        name="report_preview_a",
    ),

    # Authentications
    path('login_a/', admin_login, name='login_admin'),
    path('logout_a/', admin_logout, name='logout_admin'),
]
