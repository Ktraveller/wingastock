from django.urls import path
from deliver.views_d.deliver_home import deliver_home
from deliver.views_d.deliver_product import deliver_product
from deliver.views_d.how_deliver import how_deliver

urlpatterns = [
    path('', deliver_home, name='delivery_home'),
    path('deliver-product/', deliver_product, name='deliver_product'),
    path('how-to-deliver/', how_deliver, name='how_to_deliver')
]