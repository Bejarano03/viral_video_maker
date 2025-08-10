import os
import json
import re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def clean_script_text(text):
    """
    Removes emojis, bracketed text, parentheses, and other non-dialogue elements from the script.
    """
    # Regex to remove bracketed text (e.g., "[Cut to close-ups...]")
    bracket_pattern = re.compile(r'\[.*?\]', re.DOTALL)
    clean_text = bracket_pattern.sub(r'', text)

    # Regex to remove text in parentheses (e.g., "(Upbeat music plays...)")
    parentheses_pattern = re.compile(r'\(.*?\)', re.DOTALL)
    clean_text = parentheses_pattern.sub(r'', clean_text)
    
    # Regex to remove NARRATOR (V.O.), Narrator:, and similar tags
    narrator_pattern = re.compile(r'\b(NARRATOR|Narrator)\s*(:|\(V\.O\.\))?\s*', re.IGNORECASE)
    clean_text = narrator_pattern.sub(r'', clean_text)

    # Regex to remove most common emojis
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # Emoticons
        "\U0001F300-\U0001F5FF"  # Symbols & Pictographs
        "\U0001F680-\U0001F6FF"  # Transport & Map Symbols
        "\U0001F1E0-\U0001F1FF"  # Flags (iOS)
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    
    clean_text = emoji_pattern.sub(r'', clean_text)

    # Remove short, standalone lines that are likely titles or labels
    lines = clean_text.split('\n')
    # Filter out empty lines and lines that are too short to be dialogue
    cleaned_lines = [line.strip() for line in lines if len(line.strip()) > 5]
    
    return " ".join(cleaned_lines).strip()

def generate_video_script(topic):
    """
    Generates a video script and visual keywords using the OpenAI API.
    """
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    prompt = f"""
    You are a viral video producer. Your task is to create a compelling, 30-second video script about the topic: "{topic}". 
    The video should have a strong hook, a clear narrative, and a call to action. 
    
    Structure the response in a JSON object with the following keys:
    - `script`: A full script for a 30-second video.
    - `keywords`: A comma-separated list of 5 descriptive phrases for video generation. Each phrase should be highly specific and visually detailed, not a single word.
    
    Example of good keywords:
    "a futuristic cityscape with flying cars and neon lights"
    "a diverse group of people celebrating in slow motion"
    "a close-up shot of a cat's paws playing with a ball of yarn"
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are a professional video script writer."},
                {"role": "user", "content": prompt}
            ]
        )
        
        script_json = response.choices[0].message.content
        script_data = json.loads(script_json)
        
        script_text = script_data.get("script", "")
        keywords_string = script_data.get("keywords", "")
        
        # New line to split the keyword string into a list of strings
        keywords = [kw.strip() for kw in keywords_string.split(',')]
        
        # Call the improved cleaning function before saving the script
        cleaned_script_text = clean_script_text(script_text)
        
        script_file_path = "script.txt"
        with open(script_file_path, 'w') as f:
            f.write(cleaned_script_text)
        print(f"Script saved to {script_file_path}")

        return cleaned_script_text, keywords

    except Exception as e:
        print(f"An error occurred with the OpenAI API or during JSON parsing: {e}")
        return None, None

if __name__ == '__main__':
    trending_topic = "Why is everyone talking about the new tech gadget?" 
    
    script_text, keywords = generate_video_script(trending_topic)
    
    if script_text and keywords:
        print("\nGenerated Script:")
        print(script_text)
        print("\nGenerated Keywords:")
        print(keywords)
    else:
        print("Failed to generate script.")