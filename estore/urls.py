
from . import views
from django.urls import path
from django.conf import global_settings
from django.conf.urls.static import static

urlpatterns = [
	path('',views.index),
	path('page',views.page),
	path('product/', views.product_list, name='product_list'),
    path('product/<slug:slug>', views.product_detail, name='product_detail'),
]

if global_settings.DEBUG:
	urlpatterns += static(global_settings.STATIC_URL, document_root=global_settings.STATIC_ROOT)
	urlpatterns += static(global_settings.MEDIA_URL, document_root=global_settings.MEDIA_ROOT)