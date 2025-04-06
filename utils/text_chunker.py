from typing import List
import re
from config import settings

class TextChunker:
    def __init__(self):
        self.max_length = settings.MAX_CONTEXT_LENGTH
        self.chunk_overlap = settings.CHUNK_OVERLAP
    
    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into overlapping chunks while trying to maintain sentence boundaries.
        """
        if len(text) <= self.max_length:
            return [text]
        
        chunks = []
        current_pos = 0
        
        while current_pos < len(text):
            # Find the end position for this chunk
            end_pos = current_pos + self.max_length
            
            if end_pos >= len(text):
                # Last chunk
                chunks.append(text[current_pos:])
                break
            
            # Try to find a sentence boundary
            next_period = text.find('.', end_pos - 100, end_pos + 100)
            next_newline = text.find('\n', end_pos - 100, end_pos + 100)
            
            if next_period != -1 and next_period < end_pos + 100:
                end_pos = next_period + 1
            elif next_newline != -1 and next_newline < end_pos + 100:
                end_pos = next_newline + 1
            
            # Add the chunk
            chunk = text[current_pos:end_pos]
            chunks.append(chunk)
            
            # Move to the next position, accounting for overlap
            current_pos = end_pos - self.chunk_overlap
        
        return chunks
    
    def clean_text(self, text: str) -> str:
        """
        Clean the input text by removing extra whitespace and normalizing line endings.
        """
        # Replace multiple spaces with a single space
        text = re.sub(r'\s+', ' ', text)
        # Normalize line endings
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        # Remove multiple consecutive newlines
        text = re.sub(r'\n\s*\n', '\n\n', text)
        return text.strip()
    
    def extract_timestamps(self, text: str) -> List[dict]:
        """
        Extract timestamps from the text if they exist in a common format.
        Returns a list of dictionaries with timestamp and text.
        """
        # Common timestamp patterns
        patterns = [
            r'(\d{1,2}:\d{2}(?::\d{2})?(?:\.\d{3})?)',  # HH:MM:SS or HH:MM
            r'(\d{1,2}:\d{2}:\d{2})',  # HH:MM:SS
            r'(\d{1,2}:\d{2})',  # HH:MM
        ]
        
        timestamps = []
        for pattern in patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                timestamp = match.group(1)
                # Get the text after the timestamp until the next timestamp or end
                start_pos = match.end()
                next_match = re.search(pattern, text[start_pos:])
                end_pos = start_pos + next_match.start() if next_match else len(text)
                text_content = text[start_pos:end_pos].strip()
                
                timestamps.append({
                    'timestamp': timestamp,
                    'text': text_content
                })
        
        return timestamps 