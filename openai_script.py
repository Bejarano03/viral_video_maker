import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def generate_video_script(topic):
    """Generates a video script and visual keywords using the OpenAI API."""
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    prompt = f"""
    You are a viral video producer. Your task is to create a compelling, 30-second video script about the topic: "{topic}". 
    The video should have a strong hook, a clear narrative, and a call to action. 
    
    Structure the response in a JSON object with the following keys:
    - `script`: A full script for a 30-second video.
    - `visual_keywords`: A comma-separated list of 5 keywords for video generation (e.g., "fast cars, epic race, city skyline, futuristic neon lights").
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"}, # This ensures a structured output
            messages=[
                {"role": "system", "content": "You are a professional video script writer."},
                {"role": "user", "content": prompt}
            ]
        )
        # Parse the JSON response
        return response.choices[0].message.content
    except Exception as e:
        print(f"An error occurred with the OpenAI API: {e}")
        return None

if __name__ == '__main__':
    # We will get a topic from our youtube_scraper.py script
    trending_topic = "Why is everyone talking about the new tech gadget?" 
    
    script_data = generate_video_script(trending_topic)
    
    if script_data:
        print("Generated Script and Keywords:")
        print(script_data)
    else:
        print("Failed to generate script.")