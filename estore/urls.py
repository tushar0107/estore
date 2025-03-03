
from . import views,api_views
from django.urls import path
from django.conf import global_settings
from django.conf.urls.static import static

urlpatterns = [
	path('',views.index),
	path('product/', views.product_list, name='product_list'),
    path('product/<slug:slug>', views.product_detail, name='product_detail'),
	path('profile/',views.profile, name='user profile'),
    path('logout/',views.user_logout, name="user logout"),
    path('update-cart/',views.update_cart,name="cart page for user"),
    path('cart/',views.cart,name="cart page for user"),
    path('checkout/',views.checkout, name="checkout page"),
    path('checkout/<int:id>/',views.checkout, name="checkout page"),
    path('login/',views.user_login,name="user login"),
    path('register/',views.signup, name='user registration'),
    path('create-order-item/',views.create_order_item,name="add item to order item"),
    path('confirm-order/', views.confirm_order, name="create order for user"),
    path('get-csrf-token/', views.get_csrf_token, name='token'),
    path('api/product/<int:pk>/', api_views.ProductView.as_view(), name='to get product by id'),
    path('api/products/', api_views.ProductListView.as_view({'get':'list'}),name='to get product list'),
    path('api/login/<int:id>',api_views.LoginView.as_view(), name='to login for a user'),
    path('api/login/',api_views.LoginView.as_view(), name='to login for a user'),
    path('api/register/',api_views.RegisterUser.as_view(), name='to register new user'),
    path('api/create-customer/',api_views.CustomerCreate.as_view(), name='to create customer for a user'),
]