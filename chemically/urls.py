from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index,name="get chemical info"),
    path('api/get-chemical/<int:id>',views.get_chemicals,name="get chemical info"),
    path('api/find-chemicals/',views.find_chemicals,name="find chemical"),
    path('api/add-chemical/',views.add_chemicals,name="add new chemical")
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)