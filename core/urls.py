from django.urls import path
from .views import (
            HomeView, 
            ItemDetailView , 
            add_to_cart , 
            remove_from_cart,
            order_summary,
            remove_single_item_from_cart,
            CheckoutView,
            Payment,
)
app_name = "core"

urlpatterns = [
    path('', HomeView.as_view(), name='item_list'),
    path('product/<slug>', ItemDetailView.as_view(), name='item_detail'),
    path('add_to_cart/<slug>',add_to_cart,name='add_to_cart'),
    path('remove_from_cart/<slug>',remove_from_cart,name='remove_from_cart'),
    path('order-summary/',order_summary.as_view(),name='order_summary'),
    path('remove_from_cart/<slug>/',remove_from_cart,name='remove_from_cart'),
    path('remove_single_item_from_cart/<slug>',remove_single_item_from_cart,name='remove_single_item_cart'),
    path('checkout/',CheckoutView.as_view(),name='checkout'),
    path('payment/<payment_option>/',Payment.as_view(),name='payment'),
]
