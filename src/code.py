from youtube_transcript_api import YouTubeTranscriptApi
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from langchain.schema import Document
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv, find_dotenv
import os
import getpass
from urllib.parse import urlparse, parse_qs
import json


def get_video_id(input_value):
    """
    Get the video ID from a YouTube URL or return the input directly if it's already a video ID.

    Supported formats:
    - Standard URL: https://www.youtube.com/watch?v=<video_id>
    - Shortened URL: https://youtu.be/<video_id>
    - Embed URL: https://www.youtube.com/embed/<video_id>

    Args:
        input_value (str): The YouTube URL or the video ID.

    Returns:
        str: The video ID, or None if invalid input.
    """
    try:
        # Parse the input value as a URL
        parsed_url = urlparse(input_value)

        # Handle URLs
        if parsed_url.scheme in ['http', 'https']:
            if 'youtube.com' in parsed_url.netloc:
                if parsed_url.path.startswith('/watch'):
                    # Extract 'v' parameter from standard watch URLs
                    return parse_qs(parsed_url.query).get('v', [None])[0]
                elif parsed_url.path.startswith('/embed/'):
                    # Extract video ID from embed URLs
                    return parsed_url.path.split('/embed/')[1].split('?')[0]
            elif 'youtu.be' in parsed_url.netloc:
                # Extract video ID from shortened URLs
                return parsed_url.path.lstrip('/')

        # Assume input is a video ID if it's not a valid URL
        return input_value
    except (IndexError, ValueError) as e:
        # Return None for invalid inputs or malformed URLs
        print(f"Error processing input: {e}")
        return None

# Step 2: Load environment variables
load_dotenv(find_dotenv(), override=True)

if 'GOOGLE_API_KEY' not in os.environ:
    os.environ['GOOGLE_API_KEY'] = getpass.getpass('Provide your Google API Key: ')



# Step 3: Provide YouTube URL and extract video ID
youtube_url = input("Enter the YouTube video URL: ")
video_id = get_video_id(youtube_url)

if not video_id:
    print("Invalid YouTube URL. Please provide a valid URL.")
    exit()



# Step 4: Transcript extraction
try:
    # Retrieve the transcript
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    # Extract the text from the transcript
    transcript_text = ' '.join([entry['text'] for entry in transcript])

    # Prepare the data to be saved as JSON
    transcript_data = {
        "video_id": video_id,
        "transcript": transcript_text
    }

    # Define the target directory and file path
    output_dir = os.path.join("..", "data", "transcripts")
    os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists

    output_file = os.path.join(output_dir, f"{video_id}.json")

    # Save the transcript data to a JSON file
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(transcript_data, json_file, ensure_ascii=False, indent=4)

    print(f'Transcript saved to {output_file}')

except Exception as e:
    print(f'An error occurred while fetching transcript: {e}')
    transcript_text = None

# Step 5: Use LangChain to summarize
if transcript_text:
    try:
        # Initialize the LLM
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")

        # Create Document object
        docs = [Document(page_content=transcript_text)]

        # Define the prompt
        prompt = ChatPromptTemplate.from_template(
            "Give a detailed summary with the main ideas in bullet points, and ensure proper markdown formatting. Include all examples cited to illustrate each idea: {context}"
        )

        # Create and run the LLM chain
        chain = prompt | llm
        result = chain.invoke({"context": docs})
        print("Summary:")
        print(result)

# Now, update the JSON file with the summary

        content = result.content
        llm_usage = result.usage_metadata
        
        # Prepare the data to update with the summary
        summary_data = {
            "summary": content,
            "llm_usage": llm_usage,
            "summary_status": "success"
        }

        # Read the existing JSON file
        with open(output_file, 'r+', encoding='utf-8') as json_file:
            existing_data = json.load(json_file)
            
            # Update the existing data with the summary
            existing_data.update(summary_data)
            
            # Move the file pointer to the beginning and overwrite the file with updated content
            json_file.seek(0)
            json.dump(existing_data, json_file, ensure_ascii=False, indent=4)

        print(f'Summary added to {output_file}')

    except Exception as e:
        print(f'An error occurred during summarization: {e}')
