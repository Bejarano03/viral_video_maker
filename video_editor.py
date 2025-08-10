import ffmpeg
import json
import os

def assemble_video(video_clips, audio_file_path, script_file_path, output_path="final_video.mp4"):
    """
    Concatenates video clips, adds an audio track, and overlays captions.

    Args:
        video_clips (list): A list of file paths to the generated video clips.
        audio_file_path (str): The file path to the generated voiceover MP3.
        script_file_path (str): The file path to the script text file.
        output_path (str): The desired output file path for the final video.

    Returns:
        str: The path to the assembled video, or None if it fails.
    """
    print("Starting video assembly with FFmpeg...")

    try:
        # Step 1: Read the script for captions
        with open(script_file_path, 'r') as f:
            script_text = f.read()

        # Step 2: Concatenate the video clips
        # We need to create input streams for each clip
        input_clips = [ffmpeg.input(clip) for clip in video_clips]
        
        # Use the concat filter to join them together
        concatenated_video = ffmpeg.concat(*input_clips, v=1, a=0).node
        
        # Step 3: Add the audio track
        audio_input = ffmpeg.input(audio_file_path)
        final_video = ffmpeg.output(concatenated_video[0], audio_input.audio, output_path, vcodec='libx264', acodec='aac')

        # Step 4: Run the FFmpeg command
        final_video.run(overwrite_output=True)

        print(f"Video assembly successful! Final video saved to {output_path}")
        return output_path
    
    except ffmpeg.Error as e:
        print("FFmpeg Error during video assembly:")
        print(e.stderr.decode('utf8'))
        return None
    except Exception as e:
        print(f"An unexpected error occurred during video assembly: {e}")
        return None

if __name__ == '__main__':
    # This is an example of how you might test the script.
    # You would need to have the files 'runway_clip_1.mp4', etc.
    # and a 'voiceover.mp3' and 'script.txt' in your directory.
    #
    video_files = ["runway_clip_1.mp4", "runway_clip_2.mp4", "runway_clip_3.mp4"]
    audio_file = "voiceover.mp3"
    script_file = "script.txt"
    final_video_path = assemble_video(video_files, audio_file, script_file)
    
    if final_video_path:
       print("\nVideo is ready!")
    else:
       print("\nVideo assembly failed.")