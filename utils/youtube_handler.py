import re
from youtube_transcript_api import YouTubeTranscriptApi
import logging

logger = logging.getLogger(__name__)

class YouTubeHandler:
    def __init__(self):
        self.transcript_cache = {}

    def extract_video_id(self, url: str) -> str:
        """
        Extract video ID from various YouTube URL formats.
        
        Args:
            url (str): YouTube video URL
            
        Returns:
            str: Video ID
        """
        patterns = [
            r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?]+)',
            r'youtube\.com\/shorts\/([^&\n?]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
                
        raise ValueError("Invalid YouTube URL format")

    def get_transcript(self, url: str) -> str:
        """
        Get transcript for a YouTube video.
        
        Args:
            url (str): YouTube video URL
            
        Returns:
            str: Video transcript
        """
        try:
            video_id = self.extract_video_id(url)
            
            # Check cache first
            if video_id in self.transcript_cache:
                logger.info(f"Retrieved transcript from cache for video: {video_id}")
                return self.transcript_cache[video_id]
            
            # Get transcript from API
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            
            # Combine transcript pieces
            full_transcript = ' '.join([piece['text'] for piece in transcript_list])
            
            # Cache the transcript
            self.transcript_cache[video_id] = full_transcript
            logger.info(f"Cached transcript for video: {video_id}")
            
            return full_transcript
            
        except Exception as e:
            logger.error(f"Error getting transcript: {str(e)}")
            raise

    def suggest_questions(self, transcript: str, limit: int = 5) -> list:
        """
        Generate relevant questions based on the transcript.
        
        Args:
            transcript (str): Video transcript
            limit (int): Maximum number of questions to generate
            
        Returns:
            list: List of suggested questions
        """
        try:
            # Split transcript into chunks for better processing
            chunks = [transcript[i:i+1000] for i in range(0, len(transcript), 1000)]
            
            # Generate questions for each chunk
            questions = []
            for chunk in chunks:
                # Use Gemini API to generate questions
                # This is a placeholder - implement actual question generation
                questions.extend([
                    "What are the main topics discussed in this video?",
                    "Can you summarize the key points?",
                    "What are the important conclusions?",
                    "Are there any specific examples or case studies mentioned?",
                    "What are the practical implications discussed?"
                ])
            
            # Remove duplicates and limit the number of questions
            return list(set(questions))[:limit]
            
        except Exception as e:
            logger.error(f"Error generating questions: {str(e)}")
            return [] 