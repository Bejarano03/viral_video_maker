import os
from elevenlabs import generate, save
from dotenv import load_dotenv

def generate_voiceover(script_text, voice_name="Bella"):
    """
    Generates a high-quality voiceover from script text and saves it as an MP3.

    Args:
        script_text (str): The full text of the video script.
        voice_name (str): The name of the ElevenLabs voice to use.

    Returns:
        str: The local file path to the saved voiceover MP3 file, or None if it fails.
    """
    load_dotenv()
    elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')
    if not elevenlabs_api_key:
        print("Error: ELEVENLABS_API_KEY not found.")
        return None

    os.environ['ELEVENLABS_API_KEY'] = elevenlabs_api_key

    print("Generating voiceover with ElevenLabs...")

    try:
        audio = generate(
            text=script_text,
            voice=voice_name,
            model="eleven_multilingual_v2" # A versatile model
        )
        
        audio_file_path = "voiceover.mp3"
        save(audio, audio_file_path)
        print(f"Voiceover saved to {audio_file_path}")
        
        # We also save the script to a text file for the FFmpeg captions step
        script_file_path = "script.txt"
        with open(script_file_path, 'w') as f:
            f.write(script_text)
        print(f"Script saved to {script_file_path} for captions.")

        return audio_file_path
        
    except Exception as e:
        print(f"An error occurred with the ElevenLabs API: {e}")
        return None

if __name__ == '__main__':
    # This block shows how to test the function independently
    test_script = "Hey there, space enthusiasts! Your brain has more neurons than there are stars in the Milky Way. Keep exploring and never stop learning!"
    
    generated_audio_path = generate_voiceover(test_script)
    if generated_audio_path:
        print("\nTest voiceover is ready!")
    else:
        print("\nFailed to generate test voiceover.")