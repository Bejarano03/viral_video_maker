import os
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()


def get_trending_videos(api_key, country_code='US', category_id=None):
    """Fetches trending videos from YouTube Data API v3."""
    try:
        # Build the service object for the YouTube Data API
        youtube = build('youtube', 'v3', developerKey=api_key)

        # Make the API call to get the most popular videos
        request = youtube.videos().list(
            part='snippet,statistics',
            chart='mostPopular',
            regionCode=country_code,
            videoCategoryId=category_id,
            maxResults=50
        )
        response = request.execute()

        # Extract video titles and other useful data
        trending_videos = []
        for item in response.get('items', []):
            title = item['snippet']['title']
            video_id = item['id']
            trending_videos.append({'title': title, 'video_id': video_id})
        
        return trending_videos

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == '__main__':
    api_key = os.getenv('YOUTUBE_API_KEY')
    
    if api_key == 'YOUR_API_KEY':
        print("Please set your YOUTUBE_API_KEY environment variable or replace the placeholder.")
    else:
        videos = get_trending_videos(api_key, country_code='US', category_id='23')
        if videos:
            print("Successfully fetched trending videos:")
            for video in videos:
                print(f"- Title: {video['title']} (ID: {video['video_id']})")