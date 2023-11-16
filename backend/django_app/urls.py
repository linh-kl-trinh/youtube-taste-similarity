# backend/django_app/urls.py

from django.urls import path
from .views import handle_frontend_data

urlpatterns = [
    path('handle_frontend_data/', handle_frontend_data, name='handle_frontend_data'),
]
