from django.urls import path
from . import views


urlpatterns = [
    path('', views.cart, name="cart"),
    path('remove_cart/<int:product_id>/<int:cart_item_id>/',
         views.remove_cart, name="remove_cart"),
    path('delete_cart_item/<int:product_id>/<int:cart_item_id>/',
         views.delete_cart_item, name="delete_cart_item"),

    path('add_cart/<int:product_id>/', views.add_cart, name="add_cart"),
]
