from django.shortcuts import render

# Create your views here.
import os
import tempfile
from django.http import FileResponse, JsonResponse, StreamingHttpResponse
from pytubefix import YouTube
from pytubefix import Search

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

def youtube_audio(request):
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



        # direct_url = audio_stream.url
        # import requests
        # r = requests.get(direct_url,stream=True)

        # response = StreamingHttpResponse(
        #     streaming_content=r.iter_content(chunk_size=4096),
        #     content_type=r.headers.get('Content-Type',"audio/webm")
        # )
        # response["Content-Disposition"] = 'inline; filename="audio.webm"'
        
        # return response

        # if not audio_stream:
        #     return JsonResponse({"error": "No audio stream available"}, status=500)

        # # Temporary file to store audio
        # temp_dir = tempfile.gettempdir()
        # temp_path = os.path.join(temp_dir, f"{yt.title}.mp3")

        # # pytubefix downloads audio as .webm or .mp4 normally, but we rename to mp3
        # downloaded_path = audio_stream.download(output_path=temp_dir)
        # os.rename(downloaded_path, temp_path)

        # # return as file response
        # response = FileResponse(open(temp_path, "rb"), as_attachment=True, filename=f"{yt.title}.mp3")

        # # optional: delete after sending (only works if FileResponse finishes)
        # # os.remove(temp_path)

        # return response

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
