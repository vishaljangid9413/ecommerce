from django.urls import path
from django.views.generic import TemplateView
from cart.views import add_to_cart, cart_page, remove_from_cart, thank_you_page, update_cart_quantity

urlpatterns = [
    path('cart/', cart_page, name='cart_page'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:product_id>/', update_cart_quantity, name='update_cart_quantity'),
    path('thank-you/', thank_you_page, name='thank_you'),
]
