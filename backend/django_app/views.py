# backend/django_app/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .youtube_api import *
from django.conf import settings
from .similarity import *

@csrf_exempt
def handle_frontend_data(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        field1 = data.get('field1')
        field2 = data.get('field2')

        print(field1, field2)

        for input in [field1, field2]:
            if not is_youtube_url(input):
                print("Not a valid YouTube URL.")
                # TODO: ask for input again

        youtube_service = get_authenticated_service('youtube', 'v3', api_key=settings.YOUTUBE_API_KEY)
        
        playlist1_words = asyncio.run(get_playlist_words(youtube_service, field1))
        playlist2_words = asyncio.run(get_playlist_words(youtube_service, field2))

        similarity_score = calculate_similarity(playlist1_words, playlist2_words)

        print(similarity_score)

        return JsonResponse({'message': 'Data received successfully', 'score': float(similarity_score)})

    return JsonResponse({'error': 'Invalid request method'})
