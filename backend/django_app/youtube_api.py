# django_app/youtube_api.py
import asyncio
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled

def get_authenticated_service(api_name, api_version, api_key):
    youtube_service = build(api_name, api_version, developerKey=api_key)
    return youtube_service

async def get_playlist_items(youtube_service, playlist_id, page_token=None):
    request = youtube_service.playlistItems().list(
        part='snippet,contentDetails',
        playlistId=playlist_id,
        maxResults=50,
        pageToken=page_token
    )

    response = request.execute()

    return response.get('items', []), response.get('nextPageToken')

async def get_playlist_words(youtube_service, playlist_url):
    playlist_id = get_playlist_id(youtube_service=youtube_service, playlist_url=playlist_url)
    print("playlist id:", playlist_id)

    if playlist_id is None:
        return None

    playlist_items, next_page_token = await get_playlist_items(youtube_service, playlist_id)

    tasks = [process_playlist_items(youtube_service, item) for item in playlist_items]

    while next_page_token:
        playlist_items, next_page_token = await get_playlist_items(youtube_service, playlist_id, next_page_token)
        tasks.extend([process_playlist_items(youtube_service, item) for item in playlist_items])

    playlist_words = await asyncio.gather(*tasks)

    return playlist_words

def get_playlist_id(youtube_service, playlist_url):
    # Extract playlist ID from URL
    playlist_id = extract_playlist_id(playlist_url)
    if not playlist_id:
        print('Invalid or unsupported playlist URL format.')
        # TODO: frontend
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

from urllib.parse import urlparse, parse_qs

def is_youtube_url(url):
    # Parse the URL
    parsed_url = urlparse(url)

    # Check if the domain is 'youtube.com'
    return parsed_url.netloc == 'www.youtube.com' or parsed_url.netloc == 'youtube.com'

def extract_playlist_id(url):
    parsed_url = urlparse(url)

    # Extract the query parameters
    query_params = parse_qs(parsed_url.query)

    # Try to retrieve the 'list' parameter from the query parameters
    playlist_id = query_params.get('list', [None])[0]

    return playlist_id

async def get_transcript(video_id):
    try:
        transcript = await asyncio.to_thread(YouTubeTranscriptApi.get_transcript, video_id)
        return " ".join([chunk.get("text") for chunk in transcript]).replace("\n", " ")
    except TranscriptsDisabled:
        # print("No transcript available.")
        return ""

async def process_playlist_items(youtube_service, item):
    video_id = item.get("contentDetails").get("videoId")
    snippet = item.get("snippet", {})

    title = snippet.get("title")
    channel_name = snippet.get("videoOwnerChannelTitle")
    channel_id = snippet.get("videoOwnerChannelId")
    description = snippet.get("description")

    # https://pypi.org/project/youtube-transcript-api/#api
    # transcript language defaults to english
    transcript = await get_transcript(video_id)

    category_info = await get_category_info(youtube_service, video_id)
    channel_info = await get_channel_info(youtube_service, channel_id)

    title = title if title is not None else ""
    channel_name = channel_name if channel_name is not None else ""
    transcript = transcript if transcript is not None else ""

    words = " ".join([title,
                    channel_name,
                    description,
                    transcript,
                    catch(lambda: category_info.get("name")),
                    catch(lambda: channel_info.get("description"))])

    # print()
    # print(title, channel_name)
    # print(transcript)
    # print(playlist_words)

    return words

def catch(func, handle=lambda e : e, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except AttributeError:
        return ""

async def get_channel_info(youtube_service, channel_id):
    channel_request = youtube_service.channels().list(
        part='snippet',
        id=channel_id
    )

    try:
        response = channel_request.execute()
        channel_description = response.get("items")[0].get("snippet").get("description")
    except Exception as e:
        print(f"Error: {e}")
        return None

    # print(channel_description)

    return {"description": channel_description}

async def get_category_info(youtube_service, video_id):
    # Make the API request to get video details
    video_request = youtube_service.videos().list(
        part='snippet',
        id=video_id
    )

    try:
        response = video_request.execute()
        category_id = response.get("items")[0].get("snippet").get("categoryId")

        category_request = youtube_service.videoCategories().list(
            part='snippet',
            id=category_id
        )
        response = category_request.execute()
        category_name = response.get("items")[0].get("snippet").get("title")

        # print(category_name)

        return {"id": category_id, "name": category_name}

    except Exception as e:
        print(f"Error: {e}")
        return None
    
if __name__ == '__main__':
    url = "https://www.youtube.com/playlist?list=PLZRgWTUIhSaK7xSuWH9f7ydLJ4zcQCMUJ"
    print(extract_playlist_id(url))