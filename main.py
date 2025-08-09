from youtube_scraper import get_trending_videos
from openai_script import generate_video_script
import os

if __name__ == '__main__':
    api_key = os.getenv('YOUTUBE_API_KEY')

    if api_key:
        videos = get_trending_videos(api_key, country_code='US', category_id='23')

        if videos:
            first_trending_title = videos[0]['title']
            print(f"Using trending title as inspiration: {first_trending_title}")

            script_output = generate_video_script(first_trending_title)

            if script_output:
                print("Successfully generated video script and visual keywords!")
                print(script_output)