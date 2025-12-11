from django.shortcuts import render

# Create your views here.
import os
import tempfile
from django.http import FileResponse, JsonResponse, StreamingHttpResponse
from pytubefix import YouTube,Playlist,Search

def search(request):
    text = request.GET.get("search")
    results = Search(text)
    data = []
    try:
        for video in results.videos:
            obj = {
                'title': video.title,
                'thumbnail': video.thumbnail_url,
                'author': video.author,
                'length': video.length,
                'video_id': video.video_id,
                'url': video.watch_url,
                'streams': []
            }
            for st in video.streams.filter(type="audio").asc():
                stream = {
                    'type': st.mime_type,
                    'bitRate': st.abr,
                }
                obj['streams'].append(stream)
            data.append(obj)
        return JsonResponse({"status":True,"result":data})
    except Exception as e:
        return JsonResponse({"error":False,"message":"error"},status=400)
    
def search_playlist(request):
    text = request.GET.get("search")
    results = Playlist(text)
    playlist = {}
    try:
        playlist['title'] = results.title
        playlist['thumbnail'] = results.thumbnail_url
        playlist['length'] = len(results.videos)
        data = []
        for video in results.videos:
            obj = {
                'title': video.title,
                'thumbnail': video.thumbnail_url,
                'author': video.author,
                'length': video.length,
                'video_id': video.video_id,
                'url': video.watch_url,
                'streams': []
            }
            for st in video.streams.filter(type="audio").asc():
                stream = {
                    'type': st.mime_type,
                    'bitRate': st.abr,
                }
                obj['streams'].append(stream)
            data.append(obj)
        playlist['videos'] = data
        return JsonResponse({"status":True,"result":playlist})
    except Exception as e:
        return JsonResponse({"error":False,"message":"error"},status=400)


def get_audio_details(request):
    url = request.GET.get("url")
    if not url:
        return JsonResponse({"status":False,"error":"Url not entered"})
    
    try:
        yt = YouTube(url)
        data = {}
        data['age_restricted'] = yt.age_restricted
        data["details"] = {
            'title': yt.title,
            'thumbnail': yt.thumbnail_url,
            'author': yt.author,
            'length': yt.length,
            'video_id': yt.video_id,
        }
        return JsonResponse({"status":True,"result":data})
    
    except Exception as e:
        return JsonResponse({"status":False,"error":"error"})

def play_media(request):
    url = request.GET.get("url")
    rate = request.GET.get("rate")

    if not url:
        return JsonResponse({"error": "URL is required"}, status=400)

    try:
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True,abr=rate).first()

        return JsonResponse({
            "title": yt.title,
            "audio_url": audio_stream.url,  # direct Googlevideo stream
            "mime_type": audio_stream.mime_type
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
