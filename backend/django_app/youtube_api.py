# django_app/youtube_api.py
import asyncio
import time
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi, CouldNotRetrieveTranscript
import cohere
from django.conf import settings

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

    # Categorize words into video_info, category_info, and channel_info
    video_info_words = []
    category_info_words = []
    channel_info_words = []
    transcript_words = []

    for result in await asyncio.gather(*tasks):
        video_info_words.append(result["video_info"])
        category_info_words.append(result["category_info"])
        channel_info_words.append(result["channel_info"])
        transcript_words.append(result["transcript"])

    playlist_words = {
        "video_info": " ".join(video_info_words),
        "category_info": " ".join(category_info_words),
        "channel_info": " ".join(channel_info_words),
        "transcript" : " ".join(transcript_words)
    }

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

async def get_transcript_summary(video_id):
    try:
        transcript = await asyncio.to_thread(YouTubeTranscriptApi.get_transcript, video_id)
        text = " ".join([chunk.get("text") for chunk in transcript]).replace("\n", " ")

        if len(text) < 250:
            return text
    except CouldNotRetrieveTranscript:
        print("No transcript available.")
        return ""

    keys = [settings.COHERE_API_KEY,
            settings.COHERE_API_KEY_1,
            settings.COHERE_API_KEY_2,
            settings.COHERE_API_KEY_3]
    
    for key in keys:
        try:
            # print(video_id, key)
            co = cohere.Client(key)
        
            # summarize transcript using Cohere
            response = co.summarize(
                text=text,
                length='short',
                extractiveness='medium'
            )

            # print(response.summary)

            return response.summary.replace("Here is your short summary", "")
        except Exception as e:
            pass

    print("No summary available.")
    return ""

async def process_playlist_items(youtube_service, item):
    video_id = item.get("contentDetails").get("videoId")
    snippet = item.get("snippet", {})

    title = snippet.get("title")
    channel_name = snippet.get("videoOwnerChannelTitle")
    channel_id = snippet.get("videoOwnerChannelId")
    description = snippet.get("description")

    category_info = await get_category_info(youtube_service, video_id)
    channel_info = await get_channel_info(youtube_service, channel_id)

    title = title if title is not None else ""
    channel_name = channel_name if channel_name is not None else ""
    description = description if description is not None else ""

    video_info = " ".join([title, description])

    category_name = catch(lambda: category_info.get("name"))
    channel_description = catch(lambda: channel_info.get("description"))

    category_info_words = f"Category: {category_name}"
    channel_info_words = f"Channel: {channel_name}, {channel_description}"

    transcript_words = await get_transcript_summary(video_id)

    words = {
        "video_info": video_info,
        "category_info": category_info_words,
        "channel_info": channel_info_words,
        "transcript": transcript_words
    }

    return words

def catch(func, handle=lambda e : e, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except AttributeError:
        return ""

async def get_channel_info(youtube_service, channel_id):
    if channel_id:
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
    else:
        return None

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