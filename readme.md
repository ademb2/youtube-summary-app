📖 Project Overview
Why This Project?

YouTube videos are a significant part of my knowledge consumption, offering invaluable insights across various topics. However, the sheer volume of information makes it difficult to retain key points over time. Taking notes manually isn't always feasible due to time constraints and context in which it's consumed, leaving much of the content underutilized or forgotten.

This project aims to bridge that gap by automating the summarization process, providing concise, high-quality drafts of YouTube video content. These summaries can either be used directly or refined further to suit personal needs, making knowledge retention and note organization seamless.
The Problem

Watching videos often serves different purposes—learning a new skill, staying updated, or exploring a topic in-depth. Current tools fail to adapt their summaries to the diverse intent behind watching each video. They also rarely integrate with note-taking apps, leaving users with a disconnected workflow.

Specific challenges include:

- Time Constraints: Taking notes during or after watching videos is often impractical.
- Content Adaptability: Summaries must be tailored to the video's purpose, whether educational, tutorial-based, or news-oriented.
- Note Integration: Summaries should align with personal workflows, including Markdown formatting, relevant tags, and meaningful titles derived from content rather than clickbait YouTube titles.

The Approach

This project combines:

    Transcript Extraction: Retrieving transcripts from YouTube videos, including automatically generated subtitles.
    Advanced Summarization with LLMs: Using Google LLM Gemini to generate summaries tailored to the video's intent and structure.
    Seamless Note Integration: Producing Markdown-formatted outputs with essential properties (tags, content-based titles, and timestamps) for easy integration into note-taking systems.

The result is an adaptable, efficient solution that helps capture the essence of video content, enhancing knowledge retention and making note-taking faster and more effective.


✨ Features

- Transcript Extraction: Automatically retrieves video transcripts, including automatically generated YouTube subtitles.
- Language Model Integration: Summarizes the transcripts using Google LLM Gemini (might add possibility of using other llm later)
- Flexible Output: Generates JSON output containing:
    The original transcript
    A Markdown-formatted summary
    Video metadata: title, language, and YouTube ID
- Support for All YouTube URL Formats: Extracts the video ID seamlessly from various URL structures.
- Adaptable Summaries: Designed for manual refinement to complement personal note-taking workflows.

🚀 Future Plans

This project is in its early stages, but here are planned features:

- API Development: Expose summarization functionality via a REST API.
Web Application: Build an interface for users to upload URLs, view summaries, and download outputs.
- Database Integration: Store summaries, transcripts, and metadata for future reference.
- Mobile App: Create an Android app for on-the-go summarization and note management.

⚙️ Installation
Prerequisites

    Python 3.12 or above
    Google API Key (for Google LLM Gemini)
    Required libraries (listed below)

Steps

 - 
 - 
 - 
 - 
 - 


📝 Usage

    Provide a YouTube video URL when prompted.
    The script will:
        Extract the transcript
        Summarize the content
        Save the output in a JSON file in the same directory
    Example JSON structure:

    {
        "video_id": "abc123",
        "title": "Sample Video Title",
        "language": "en",
        "transcript": "Original transcript text...",
        "summary": "## Summary\n\n- Main idea 1...\n- Main idea 2..."
    }

📦 Dependencies

    LangChain: Used for language model integration.
    youtube-transcript-api: Extracts video transcripts without requiring YouTube's official API.

        ⚠ Disclaimer: This library relies on an undocumented YouTube API and may break if YouTube updates its backend. The project will adapt to any changes as they arise.


A full list of dependencies is provided in pyproject.toml.
🔧 Limitations

    YouTube Transcript Retrieval: Since the YouTube Transcript API is unofficial, its functionality is subject to change.
    Manual Adjustments: Summaries are designed as a starting point and may require manual edits for completeness or personalization.


📜 License

MIT License
🛠️ Acknowledgments

    Google LLM Gemini for powering the summarization.
    youtube-transcript-api for enabling transcript retrieval.
    