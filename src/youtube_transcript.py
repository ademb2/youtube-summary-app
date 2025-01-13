import os
import re
import json
import logging
from datetime import datetime
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

def get_video_id(input_value):
    """Extract the YouTube video ID from various URL formats or validate direct video ID."""
    try:
        id_pattern = r'^[0-9A-Za-z_-]{11}$'
        url_pattern = r'(youtube\.com\/(watch\?v=|embed\/)|youtu\.be\/)([0-9A-Za-z_-]{11})(?:[&?][^ ]*)?'

        if re.match(id_pattern, input_value):
            return input_value
        
        match = re.search(url_pattern, input_value)
        if match:
            return match.group(3)
    except Exception as e:
        logging.error(f"Failed to extract video ID: {e}")
    return None

def get_video_info(video_id):
    """Fetch video details using YouTube API."""
    try:
        youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
        request = youtube.videos().list(part="snippet", id=video_id)
        response = request.execute()
        snippet = response["items"][0]["snippet"]
        
        published_at = snippet["publishedAt"]
        formatted_date = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d")

        return {"title": snippet["title"], "publishedAt": formatted_date}
    except Exception as e:
        logging.error(f"Error fetching video info: {e}")
        return None

def extract_transcript(video_id):
    """Retrieve the YouTube transcript as a single text block."""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'en-GB', 'en-US', 'en-CA', 'en-AU', 'fr', 'fr-CA'])
        return ' '.join(entry['text'] for entry in transcript)
    except Exception as e:
        logging.error(f"Error fetching transcript: {e}")
        return None

def save_transcript_to_file(video_id, transcript_text, video_info, output_dir="../data/transcripts"):
    """Save transcript and video metadata to a JSON file with today's date as the save date."""
    try:
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, f"{video_id}.json")
        save_date = datetime.now().strftime("%Y-%m-%d")
        data = {
            "video_id": video_id,
            "title": video_info["title"],
            "publishedAt": video_info["publishedAt"],
            "transcript": transcript_text,
            "save_date": save_date
        }
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        return file_path
    except Exception as e:
        logging.error(f"Error saving transcript to file: {e}")
        return None

def update_transcript_with_summary(file_path, summary):
    """Add the summary to the transcript JSON."""
    try:
        with open(file_path, 'r+', encoding='utf-8') as file:
            data = json.load(file)
            data.update({"summary": summary})
            file.seek(0)
            json.dump(data, file, ensure_ascii=False, indent=4)
    except Exception as e:
        logging.error(f"Error updating transcript file: {e}")