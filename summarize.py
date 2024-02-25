import os
from pathlib import Path
import moviepy.editor as mp
from openai import OpenAI
import imageio_ffmpeg as ffmpeg

# Explicitly set the path to the ffmpeg executable
ffmpeg_path = "/opt/homebrew/bin/ffmpeg"  # Adjust this path as necessary
os.environ["IMAGEIO_FFMPEG_EXE"] = ffmpeg_path

# Verify that moviepy can now locate ffmpeg
print("Using ffmpeg at:", ffmpeg.get_ffmpeg_exe())

# Initialize the OpenAI client
client = OpenAI(api_key='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')

def extract_audio_from_video(video_path):
    """Extract the audio from the given video file and save it as an MP3."""
    video = mp.VideoFileClip(video_path)
    audio_path = Path(video_path).with_suffix('.mp3')
    video.audio.write_audiofile(audio_path)
    return audio_path

def transcribe_audio(audio_path):
    """Transcribe the given audio file to text using OpenAI's Whisper model."""
    with open(audio_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return transcript["text"]

def summarize_text_with_gpt4(text):
    """Summarize the given text using OpenAI's GPT-4 model for studying purposes."""
    prompt = f"Summarize the following text for study purposes:\n\n{text}"
    response = client.completions.create(
        model="gpt-4",
        prompt=prompt,
        max_tokens=1000  # Adjust based on your needs
    )
    return response.choices[0].text.strip()

def text_to_speech(text, output_path):
    """Convert the given text to speech using OpenAI's TTS model and save it as an MP3."""
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=text
    )
    response.stream_to_file(output_path)

def process_video_for_study(video_path):
    audio_path = extract_audio_from_video(video_path)
    transcribed_text = transcribe_audio(audio_path)
    summary = summarize_text_with_gpt4(transcribed_text)
    speech_file_path = Path(video_path).parent / "summary_speech.mp3"
    text_to_speech(summary, speech_file_path)
    print(f"Summary speech file saved to: {speech_file_path}")

# Example usage
video_path = "/Users/guylavian/Documents/מתמטיקה בדידה 1, 20067, קבוצת הרצאה מספר 80, יפית נתני, יום .mp4"
process_video_for_study(video_path)
