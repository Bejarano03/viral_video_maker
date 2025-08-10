import os
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv

def generate_voiceover(script_text, voice_id="ZT9u07TYPVl83ejeLakq"):
    """
    Generates a high-quality voiceover from script text and saves it as an MP3.

    Args:
        script_text (str): The full text of the video script.
        voice_id (str): The ID of the ElevenLabs voice to use. Default is "Bella".

    Returns:
        str: The local file path to the saved voiceover MP3 file, or None if it fails.
    """
    load_dotenv()
    elevenlabs_api_key = os.getenv('ELEVENLABS_API_KEY')
    if not elevenlabs_api_key:
        print("Error: ELEVENLABS_API_KEY not found.")
        return None

    # Initialize the ElevenLabs client with your API key
    client = ElevenLabs(api_key=elevenlabs_api_key)

    print("Generating voiceover with ElevenLabs...")

    try:
        # CORRECTED: The parameter name is 'voice_id' instead of 'voice'
        audio_stream = client.text_to_speech.convert(
            text=script_text,
            voice_id=voice_id,
            model_id="eleven_multilingual_v2"
        )
        
        audio_file_path = "voiceover.mp3"
        
        # Stream the audio to a file
        with open(audio_file_path, "wb") as f:
            for chunk in audio_stream:
                f.write(chunk)
                
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
    test_script = "Hey there, space enthusiasts! Your brain has more neurons than there are stars in the Milky Way. Keep exploring and never stop learning!"
    generated_audio_path = generate_voiceover(test_script)
    if generated_audio_path:
        print("\nTest voiceover is ready!")
    else:
        print("\nFailed to generate test voiceover.")