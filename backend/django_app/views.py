# backend/django_app/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .youtube_api import *
from django.conf import settings
from .similarity import *
from .models import PlaylistSimilarity

@csrf_exempt
def handle_frontend_data(request):
    if request.method == 'GET':
        all_ps = PlaylistSimilarity.objects.all()
        ps_data = [{'playlist1': ps.playlist1, 'field2': ps.playlist2, 'similarity': ps.similarity} for ps in all_ps]
        return JsonResponse({'playlists': ps_data})

    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        field1 = data.get('field1')
        field2 = data.get('field2')

        ps = PlaylistSimilarity(playlist1=field1, playlist2=field2)

        print(field1, field2)

        for input in [field1, field2]:
            if not is_youtube_url(input):
                print("Not a valid YouTube URL.")
                # TODO: ask for input again

        youtube_service = get_authenticated_service('youtube', 'v3', api_key=settings.YOUTUBE_API_KEY)
        playlist1_items = get_playlist_items(youtube_service, field1)
        playlist2_items = get_playlist_items(youtube_service, field2)

        playlist1_words = process_playlist_items(youtube_service, playlist1_items)
        playlist2_words = process_playlist_items(youtube_service, playlist2_items)

        similarity_score = calculate_similarity(playlist1_words, playlist2_words)

        ps.similarity = similarity_score
        ps.save()

        return JsonResponse({'message': 'Data received successfully', 'score': float(similarity_score)})

    return JsonResponse({'error': 'Invalid request method'})
