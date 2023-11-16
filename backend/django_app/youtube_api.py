# django_app/youtube_api.py
import os
from googleapiclient.discovery import build
import re

def get_authenticated_service(api_name, api_version, api_key):
    youtube_service = build(api_name, api_version, developerKey=api_key)
    return youtube_service

def get_playlist_items(youtube_service, playlist_url):
    # playlist_id = get_playlist_id(youtube_service=youtube_service, playlist_url=playlist_url)
    playlist_id = "PLrgUJTSd4L4t0PRkYgQnV4MfMe0mmXIXz"
    print("playlist id:", playlist_id)

    playlist_items = []
    request = youtube_service.playlistItems().list(
        part='snippet,contentDetails',
        playlistId=playlist_id,
        maxResults=50
    )

    while request:
        response = request.execute()
        playlist_items.extend(response['items'])
        request = youtube_service.playlistItems().list_next(request, response)

    # print(playlist_items)

    return playlist_items

def get_playlist_id(youtube_service, playlist_url):
    # Extract playlist ID from URL
    playlist_id = extract_playlist_id(playlist_url)
    if not playlist_id:
        print('Invalid or unsupported playlist URL format.')
        return None 

    # Call the playlists.list method to get playlist details
    request = youtube_service.playlists().list(
        part='id',
        maxResults=1,
        fields='items/id',
        id=playlist_id
    )

    try:
        response = request.execute()
        if 'items' in response and response['items']:
            return response['items'][0]['id']
        else:
            print('Playlist not found.')
    except Exception as e:
        print(f'Error retrieving playlist ID: {e}')

    return None

def extract_playlist_id(url):
    # Your regular expression pattern to extract the playlist ID
    pattern = (
        r'(?:https?://)?(?:www\.)?'
        '(?:youtube\.com/(?:[^/]+/.+/|(?:v|e(?:mbed)))/|youtu\.be/)'
        '(?P<playlist_id>[^"&?/]+)'
    )

    match = re.search(pattern, url)
    if match:
        return match.group('playlist_id')

    return None


def process_playlist_items(playlist_items):
    for item in playlist_items:
        video_id = item.get("id")
        snippet = item.get("snippet", {})
        title = snippet.get("title")
        description = snippet.get("description")

        print(title);