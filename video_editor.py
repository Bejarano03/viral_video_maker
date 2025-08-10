import ffmpeg
import os
import json

def create_srt_from_script(script_text, audio_duration_seconds, srt_output_path="captions.srt"):
    """
    Creates a basic .srt subtitle file by estimating timings from audio duration.
    This is a simplified approach for demonstration purposes.
    """
    try:
        words = script_text.split()
        total_words = len(words)
        words_per_second = total_words / audio_duration_seconds

        with open(srt_output_path, 'w') as f:
            current_word_index = 0
            for i in range(0, total_words, 5):  # Create a new caption block every 5 words
                caption_block_start_sec = current_word_index / words_per_second
                caption_block_end_sec = (current_word_index + 5) / words_per_second

                start_time_ms = int(caption_block_start_sec * 1000)
                end_time_ms = int(caption_block_end_sec * 1000)

                start_time_str = f"{start_time_ms // 3600000:02d}:{start_time_ms % 3600000 // 60000:02d}:{start_time_ms % 60000 // 1000:02d},{start_time_ms % 1000:03d}"
                end_time_str = f"{end_time_ms // 3600000:02d}:{end_time_ms % 3600000 // 60000:02d}:{end_time_ms % 60000 // 1000:02d},{end_time_ms % 1000:03d}"

                caption_text = " ".join(words[i:i+5])
                
                f.write(f"{i // 5 + 1}\n")
                f.write(f"{start_time_str} --> {end_time_str}\n")
                f.write(f"{caption_text}\n\n")

                current_word_index += 5

        print(f"SRT file created at {srt_output_path}")
        return srt_output_path
    
    except Exception as e:
        print(f"Error creating SRT file: {e}")
        return None

def assemble_video(video_clip_paths, audio_file_path, script_file_path, output_path="final_video.mp4"):
    """
    Concatenates video clips, adds an audio track, and overlays captions.
    """
    print("Starting video assembly with FFmpeg...")

    try:
        # Get audio duration using ffmpeg.probe()
        probe = ffmpeg.probe(audio_file_path)
        audio_duration = float(probe['format']['duration'])
        
        # Create the .srt file for captions
        srt_file_path = create_srt_from_script(
            open(script_file_path).read(),
            audio_duration
        )
        if not srt_file_path:
            return None

        # Step 1: Create input streams for all video clips
        video_streams = [ffmpeg.input(clip) for clip in video_clip_paths]

        # Step 2: Concatenate the video clips
        concatenated_video_stream = ffmpeg.concat(*video_streams, v=1, a=0).node
        
        # Step 3: Apply the subtitles filter to the concatenated video stream
        subtitled_video_stream = ffmpeg.filter(concatenated_video_stream[0], 'subtitles', filename=srt_file_path).node

        # Step 4: Add the audio input and combine with the subtitled video
        audio_stream = ffmpeg.input(audio_file_path)
        
        # We need to set the duration of the final video to match the audio
        final_video = (
            ffmpeg
            .output(subtitled_video_stream[0], audio_stream, output_path, vcodec='libx264', acodec='aac', t=audio_duration)
            .overwrite_output()
        )
        
        ffmpeg.run(final_video)
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
    # You would use this script with your generated files
    test_videos = ["runway_clip_1.mp4", "runway_clip_2.mp4", "runway_clip_3.mp4", "runway_clip_4.mp4", "runway_clip_5.mp4"]
    test_audio = "voiceover.mp3"
    test_script = "script.txt"
    final_video_path = assemble_video(test_videos, test_audio, test_script)
    if final_video_path:
        print("\nVideo is ready!")
    else:
        print("\nVideo assembly failed.")