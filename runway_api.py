import os
import requests
import base64
from runwayml import RunwayML
from dotenv import load_dotenv
import time

load_dotenv()

def generate_runway_clips(visual_keywords_list, duration=1):
    """
    Generates multiple short video clips using Runway ML based on a list of keywords.

    Args:
        visual_keywords_list (list): A list of strings with keywords for each clip.
        duration (int): The duration of each video clip in seconds.

    Returns:
        list: A list of local file paths for the downloaded video clips.
    """
    runway_key = os.getenv('RUNWAYML_API_SECRET')
    if not runway_key:
        print("Error: Runway API key not found.")
        return []
    
    client = RunwayML(api_key=runway_key)

    blank_image_data_uri = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="

    
    clip_urls = []
    print("Starting video generation with Runway ML...")
    
    for keywords in visual_keywords_list:
        print(f"  - Generating clip for: '{keywords}'...")
        try:
            # We'll use the 'gen-3-motion' model as it's a powerful and cost-effective option
            task = client.image_to_video.create(
                model='gen-3-motion',
                prompt_image=blank_image_data_uri,
                prompt_text=keywords,
                duration=duration,
                ratio='9:16'  # Vertical video format
            )
            
            # Poll the API until the task is complete
            status = task.get('status')
            while status not in ['succeeded', 'failed']:
                print(f"    - Status: {status}...")
                time.sleep(10)  # Wait for 10 seconds before checking again
                task = client.tasks.retrieve(task['id'])
                status = task.get('status')
                
            if status == 'succeeded':
                video_url = task['result']['video']['url']
                clip_urls.append(video_url)
                print(f"  - Clip generated successfully. URL: {video_url}")
            else:
                print("  - Video generation failed for this prompt.")
        except Exception as e:
            print(f"An error occurred with the Runway API: {e}")
            
    # Now, download the generated clips to the local machine
    local_clip_paths = []
    if clip_urls:
        print("\nDownloading generated clips...")
        for i, url in enumerate(clip_urls):
            file_path = f"runway_clip_{i+1}.mp4"
            try:
                response = requests.get(url, stream=True)
                if response.status_code == 200:
                    with open(file_path, "wb") as f:
                        f.write(response.content)
                    local_clip_paths.append(file_path)
                    print(f"  - Downloaded to {file_path}")
                else:
                    print(f"  - Failed to download clip from {url}. Status code: {response.status_code}")
            except Exception as e:
                print(f"  - Error downloading clip: {e}")

    return local_clip_paths

if __name__ == '__main__':
    # This block shows how to use the function. It's for testing purposes.
    keywords_from_openai = ["futuristic cyberpunk city"]
    downloaded_clips = generate_runway_clips(keywords_from_openai)
    if downloaded_clips:
        print("\nAll Runway clips are ready for assembly:", downloaded_clips)
    else:
        print("\nNo Runway clips were generated or downloaded.")