from django.urls import path
from . import views

urlpatterns = [
    path('product-detail/<int:pk>', views.product_detail, name='product-detail'),
    path('checkout', views.checkout, name='checkout'),
    path('contact', views.contact, name='contact'),
    path('', views.index, name='home'),
    path('shop-grid', views.shop_grid, name='shop-grid'),
    path('shopping-cart', views.shopping_cart, name='shopping-cart'),

    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.user_logout, name='logout'),

    path('remove-from-cart/<int:pk>/', views.remove_from_cart, name='remove-from-cart'),
]
