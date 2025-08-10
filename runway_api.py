import os
import requests
import base64
from runwayml import RunwayML, TaskFailedError
from dotenv import load_dotenv

load_dotenv()

def generate_runway_clips(visual_keywords_list, duration=5):
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

    # Create a 1x1 pixel transparent PNG as a placeholder prompt image
    placeholder_image_url = "https://placehold.co/1x1.png"

    clip_urls = []
    print("Starting video generation with Runway ML...")

    for keywords in visual_keywords_list:
        print(f"  - Generating clip for: '{keywords}'...")
        try:
            # We'll use the 'gen3a_turbo' model as it's a powerful and cost-effective option
            task = client.image_to_video.create(
                model='gen3a_turbo',
                prompt_image=placeholder_image_url,
                prompt_text=keywords,
                duration=duration,
                ratio='768:1280'
            ).wait_for_task_output()
            
            # The task object now contains the final output directly
            video_url = task.output[0]
            clip_urls.append(video_url)
            print(f"  - Clip generated successfully. URL: {video_url}")

        except TaskFailedError as e:
            print(f"  - Video generation failed for this prompt.")
            print(f"  - Error details: {e.task_details}")
        except Exception as e:
            print(f"An unexpected error occurred with the Runway API: {e}")

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
    keywords_from_openai = ["futuristic cyberpunk city"]
    downloaded_clips = generate_runway_clips(keywords_from_openai)
    if downloaded_clips:
        print("\nAll Runway clips are ready for assembly:", downloaded_clips)
    else:
        print("\nNo Runway clips were generated or downloaded.")