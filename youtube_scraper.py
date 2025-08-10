# youtube_scraper.py
import os
import random
from googleapiclient.discovery import build
from dotenv import load_dotenv

def get_trending_videos(api_key, country_code='US', category_id=None):
    """
    Fetches trending videos from YouTube Data API v3.
    """
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)

        request = youtube.videos().list(
            part='snippet,statistics',
            chart='mostPopular',
            regionCode=country_code,
            videoCategoryId=category_id,
            maxResults=50
        )
        response = request.execute()

        trending_videos = []
        for item in response.get('items', []):
            title = item['snippet']['title']
            video_id = item['id']
            trending_videos.append({'title': title, 'video_id': video_id})
        
        return trending_videos

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_trending_topic(category_id=None):
    """
    Fetches trending videos and returns a random video title.
    Now accepts an optional category_id to filter results.
    """
    load_dotenv()
    api_key = os.getenv('YOUTUBE_API_KEY')
    
    if not api_key:
        print("Error: YOUTUBE_API_KEY not found in .env file.")
        return None

    trending_videos = get_trending_videos(api_key, category_id=category_id)
    
    if trending_videos:
        # Select a random title from the list of trending videos
        random_video = random.choice(trending_videos)
        return random_video['title']
    else:
        print("Failed to fetch trending videos.")
        return None

if __name__ == '__main__':
    # You can now test the function with a specific category ID, e.g., '20' for Gaming
    trending_topic = get_trending_topic(category_id='20')
    if trending_topic:
        print(f"Successfully fetched a trending topic: {trending_topic}")
    else:
        print("Failed to fetch a trending topic.")