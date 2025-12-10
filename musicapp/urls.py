from django.urls import path
from . import views

urlpatterns = [
    path('stream-audio/',views.youtube_audio,name="download music audio"),
    path('get_audio_details/',views.get_audio_details,name="get music audio options"),
    path('search/',views.search,name="search music and videos"),
]