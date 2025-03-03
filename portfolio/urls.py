from django.urls import path
from . import views

urlpatterns = [
	path('sendmail/',views.getMail,name='send email')
]