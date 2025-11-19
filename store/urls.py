from django.urls import path
from store import views

urlpatterns = [

    path('', views.store, name='store'),
    path('product/', views.products, name='products'),  # html for product.html
    path('cart/', views.cart, name='cart'),  # html for cart.html

    # html for checkout.html
    path('checkout/', views.checkout, name='checkout'),

    path('<slug:category_slug>/', views.store, name='products_by_category'),
    path('<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),



]
