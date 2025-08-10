# streamlit_app.py
import streamlit as st
import os
import json
import ffmpeg

# Import all our custom modules
from youtube_scraper import get_trending_topic
from openai_script import generate_video_script
from elevenlabs_api import generate_voiceover
from runway_api import generate_runway_clips
from video_editor import assemble_video
from category_selector import get_category_id_from_prompt

# Main Streamlit UI
st.set_page_config(page_title="AI Viral Video Maker", layout="wide")
st.title("📹 AI Viral Video Maker")
st.subheader("Turn your ideas into videos using AI")
st.markdown("---")

# User input prompt
user_prompt = st.text_input(
    "What kind of video do you want to make?",
    placeholder="e.g., 'A funny video about dogs playing with toys'",
    key="user_prompt_input"
)

# Start button
if st.button("Generate Video!", key="generate_button"):
    if not user_prompt:
        st.error("Please enter a video idea to get started.")
        st.stop()
    
    # Use a Streamlit placeholder to display status updates
    status_placeholder = st.empty()

    try:
        status_placeholder.info("1. Identifying the best YouTube category for your idea...")
        
        # New function call to get the dynamic category ID
        category_id = get_category_id_from_prompt(user_prompt)
        if not category_id:
            st.error("❌ Failed to identify a suitable YouTube category. Please try a different prompt.")
            st.stop()
        
        status_placeholder.info(f"2. Found a relevant category ID: {category_id}. Scraping trending videos...")
        trending_topic = get_trending_topic(category_id=category_id)
        if not trending_topic:
            st.error("❌ Failed to find a trending topic.")
            st.stop()
        status_placeholder.success(f"✅ Found trending topic: '{trending_topic}'")

        status_placeholder.info("3. Generating video script and visual keywords with OpenAI...")
        script_text, keywords = generate_video_script(trending_topic)
        if not script_text or not keywords:
            st.error("❌ Failed to generate script.")
            st.stop()
        status_placeholder.success(f"✅ Script and keywords generated.")

        status_placeholder.info("4. Generating voiceover with ElevenLabs...")
        audio_path = generate_voiceover(script_text)
        if not audio_path:
            st.error("❌ Failed to generate voiceover.")
            st.stop()
        status_placeholder.success(f"✅ Voiceover saved to '{audio_path}'")
        
        status_placeholder.info("5. Generating video clips from keywords with Runway ML...")
        video_paths = generate_runway_clips(keywords)
        if not video_paths:
            st.error("❌ No video clips were generated.")
            st.stop()
        status_placeholder.success(f"✅ Generated {len(video_paths)} clips.")

        status_placeholder.info("6. Assembling final video with FFmpeg...")
        final_video_path = assemble_video(video_paths, audio_path, "script.txt")
        
        if final_video_path:
            status_placeholder.success("✅ Final video assembly complete!")
            st.video(final_video_path)
            st.balloons()
            st.markdown(f"### 🎉 Your video is ready!")
        else:
            st.error("❌ An error occurred during video assembly.")

    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")