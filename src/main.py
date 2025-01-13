import logging
import time
import argparse
from dotenv import load_dotenv
from youtube_transcript import get_video_id, get_video_info, extract_transcript, save_transcript_to_file, update_transcript_with_summary
from summarizer import generate_summary

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load environment variables
load_dotenv()

def main(youtube_url):
    start_time = time.time()
    video_id = get_video_id(youtube_url)
    if not video_id:
        logging.error("Invalid YouTube URL or video ID.")
        exit(1)
    logging.info(f"Time to get video ID: {time.time() - start_time:.2f} seconds")

    start_time = time.time()
    video_info = get_video_info(video_id)
    if not video_info:
        logging.error("Failed to retrieve video info.")
        exit(1)
    logging.info(f"Time to get video info: {time.time() - start_time:.2f} seconds")

    start_time = time.time()
    transcript_text = extract_transcript(video_id)
    if not transcript_text:
        logging.error("Failed to retrieve transcript.")
        exit(1)
    logging.info(f"Time to extract transcript: {time.time() - start_time:.2f} seconds")

    start_time = time.time()
    file_path = save_transcript_to_file(video_id, transcript_text, video_info)
    if not file_path:
        logging.error("Failed to save transcript.")
        exit(1)
    logging.info(f"Time to save transcript to file: {time.time() - start_time:.2f} seconds")

    start_time = time.time()
    summary = generate_summary(transcript_text)
    if not summary:
        logging.error("Failed to generate summary.")
        exit(1)
    logging.info(f"Time to generate summary: {time.time() - start_time:.2f} seconds")

    start_time = time.time()
    update_transcript_with_summary(file_path, summary)
    logging.info(f"Summary added to {file_path}")
    logging.info(f"Time to update transcript with summary: {time.time() - start_time:.2f} seconds")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YouTube Video Summarizer")
    parser.add_argument("youtube_url", type=str, help="The URL of the YouTube video to summarize")
    args = parser.parse_args()
    main(args.youtube_url)