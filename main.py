# main.py
import os
import json
import ffmpeg

# Import all our custom modules
from youtube_scraper import get_trending_topic
from openai_script import generate_video_script # Corrected import name
from elevenlabs_api import generate_voiceover
from runway_api import generate_runway_clips
from video_editor import assemble_video

if __name__ == '__main__':
    print("--- Starting Viral Video Maker Workflow ---")

    # 1. Get a trending topic from YouTube
    trending_topic = get_trending_topic()
    if not trending_topic:
        print("❌ Failed to find a trending topic.")
        exit()
    print(f"✅ Found trending topic: '{trending_topic}'")

    # 2. Generate a script and visual keywords from OpenAI
    print("Generating video script and keywords...")
    script_text, keywords = generate_video_script(trending_topic)
    if not script_text or not keywords:
        print("❌ Failed to generate script.")
        exit()
    print(f"✅ Script generated successfully. Keywords: {keywords}")

    # 3. Generate voiceover from the script using ElevenLabs
    print("Generating voiceover...")
    audio_path = generate_voiceover(script_text)
    if not audio_path:
        print("❌ Failed to generate voiceover.")
        exit()
    print(f"✅ Voiceover saved to '{audio_path}'")
    
    # 4. Generate multiple video clips from the keywords using Runway ML
    # Pass the entire list of keywords to the function
    print("Generating video clips from keywords...")
    video_paths = generate_runway_clips(keywords)
    
    if not video_paths:
        print("❌ No video clips were generated. Exiting.")
        exit()

    print(f"✅ Generated {len(video_paths)} clips: {video_paths}")

    # 5. Assemble the final video with audio and captions
    print("Assembling final video...")
    final_video_path = assemble_video(video_paths, audio_path, "script.txt")
    
    if final_video_path:
        print("\n--- ✅ Project Completed! ✅ ---")
        print(f"Your final video is ready at: {final_video_path}")
    else:
        print("\n--- ❌ Project Failed at the Final Assembly Stage. ---")