from youtube_transcript_api import YouTubeTranscriptApi
import re

def extract_video_id(url: str) -> str:
    """Extract the video ID from a YouTube URL."""
    # Handle different YouTube URL formats
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?]+)',
        r'youtube\.com\/embed\/([^&\n?]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    raise ValueError("Invalid YouTube URL")

def get_transcript(video_id: str) -> str:
    """Get the transcript for a YouTube video."""
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        # Combine all transcript pieces into a single text
        full_transcript = " ".join([entry['text'] for entry in transcript_list])
        return full_transcript
    except Exception as e:
        raise Exception(f"Failed to get transcript: {str(e)}")

def suggest_questions(transcript: str) -> list:
    """Generate suggested questions based on the transcript content."""
    # This is a simple example - you might want to use the Gemini API to generate more sophisticated questions
    questions = [
        "What are the main topics discussed in this video?",
        "What are the key points or takeaways from this video?",
        "What are the main arguments or conclusions presented?",
        "What are the technical terms or concepts mentioned?",
        "What are the examples or case studies discussed?",
        "What are the challenges or problems addressed?",
        "What are the solutions or recommendations provided?",
        "What are the future implications or next steps mentioned?"
    ]
    return questions 