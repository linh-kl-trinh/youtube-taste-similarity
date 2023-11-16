# backend/your_django_app/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def handle_frontend_data(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        field1 = data.get('field1')
        field2 = data.get('field2')

        # Do something with the data, e.g., save it to the database

        return JsonResponse({'message': 'Data received successfully'})

    return JsonResponse({'error': 'Invalid request method'})
