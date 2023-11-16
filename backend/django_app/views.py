# backend/django_app/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .youtube_api import *
from django.conf import settings

@csrf_exempt
def handle_frontend_data(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        field1 = data.get('field1')
        field2 = data.get('field2')

        # Do something with the data, e.g., save it to the database

        print(field1, field2);

        youtube_service = get_authenticated_service('youtube', 'v3', api_key=settings.YOUTUBE_API_KEY)
        playlist1_items = get_playlist_items(youtube_service, field1)
        playlist2_items = get_playlist_items(youtube_service, field2)

        process_playlist_items(playlist1_items)

        return JsonResponse({'message': 'Data received successfully'})

    return JsonResponse({'error': 'Invalid request method'})
