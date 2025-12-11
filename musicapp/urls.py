from django.urls import path
from . import views

urlpatterns = [
    path('stream-audio/',views.play_media,name="download music audio"),
    path('get_audio_details/',views.get_audio_details,name="get music audio options"),
    path('search/',views.search,name="search music and videos"),
    path('search_playlist/',views.search_playlist,name="search playlist from youtube"),
]