YouTube Video Summarizer with LLM Assistance
📖 Project Overview

This project automates the process of summarizing YouTube videos using a combination of transcript extraction and an advanced language model (Google LLM Gemini). It generates concise, Markdown-formatted summaries tailored for note-taking purposes. The goal is to assist users in capturing the most important information from videos, saving time, and making it easier to organize personal notes.

Although there are existing tools for summarization, this project focuses on creating summaries that are adaptable to different video types and personal use cases.
✨ Features

    Transcript Extraction: Automatically retrieves video transcripts, including automatically generated YouTube subtitles.
    Language Model Integration: Summarizes the transcripts using Google LLM Gemini (might add possibility of using other llm later)
    Flexible Output: Generates JSON output containing:
        The original transcript
        A Markdown-formatted summary
        Video metadata: title, language, and YouTube ID
    Support for All YouTube URL Formats: Extracts the video ID seamlessly from various URL structures.
    Adaptable Summaries: Designed for manual refinement to complement personal note-taking workflows.

🚀 Future Plans

This project is in its early stages, but here are planned features:

    API Development: Expose summarization functionality via a REST API.
    Web Application: Build an interface for users to upload URLs, view summaries, and download outputs.
    Database Integration: Store summaries, transcripts, and metadata for future reference.
    Mobile App: Create an Android app for on-the-go summarization and note management.

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
    