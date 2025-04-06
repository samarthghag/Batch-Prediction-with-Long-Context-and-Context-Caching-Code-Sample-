from cachetools import TTLCache
from typing import Dict, List, Optional, Tuple
import hashlib
from config import settings
import json

class ContextCache:
    def __init__(self):
        self.cache = TTLCache(maxsize=100, ttl=settings.CACHE_TTL)
        self.conversation_history: Dict[str, List[Dict]] = {}
        self.language_cache: Dict[str, Tuple[str, float]] = {}
        self.cultural_cache: Dict[str, List[Dict]] = {}
    
    def _generate_key(self, text: str) -> str:
        """Generate a unique key for the given text."""
        return hashlib.md5(text.encode()).hexdigest()
    
    def get_response(self, question: str, context: str) -> Optional[str]:
        """
        Get cached response for a question and context.
        
        Args:
            question (str): The question being asked
            context (str): The context for the question
            
        Returns:
            Optional[str]: Cached response if available, None otherwise
        """
        key = self._generate_key(f"{question}:{context}")
        return self.cache.get(key)
    
    def cache_response(self, question: str, context: str, response: str) -> None:
        """
        Cache a response for a question and context.
        
        Args:
            question (str): The question being asked
            context (str): The context for the question
            response (str): The response to cache
        """
        key = self._generate_key(f"{question}:{context}")
        self.cache[key] = response
    
    def get_language_info(self, text: str) -> Optional[Tuple[str, float]]:
        """
        Get cached language detection info.
        
        Args:
            text (str): Text to get language info for
            
        Returns:
            Optional[Tuple[str, float]]: (language_code, confidence) if cached
        """
        key = self._generate_key(text)
        return self.language_cache.get(key)
    
    def cache_language_info(self, text: str, lang_code: str, confidence: float) -> None:
        """
        Cache language detection info.
        
        Args:
            text (str): Text to cache language info for
            lang_code (str): Detected language code
            confidence (float): Detection confidence
        """
        key = self._generate_key(text)
        self.language_cache[key] = (lang_code, confidence)
    
    def get_cultural_references(self, text: str) -> Optional[List[Dict]]:
        """
        Get cached cultural references.
        
        Args:
            text (str): Text to get cultural references for
            
        Returns:
            Optional[List[Dict]]: List of cultural references if cached
        """
        key = self._generate_key(text)
        return self.cultural_cache.get(key)
    
    def cache_cultural_references(self, text: str, references: List[Dict]) -> None:
        """
        Cache cultural references.
        
        Args:
            text (str): Text to cache cultural references for
            references (List[Dict]): Cultural references to cache
        """
        key = self._generate_key(text)
        self.cultural_cache[key] = references
    
    def add_to_conversation(self, conversation_id: str, role: str, content: str) -> None:
        """
        Add a message to the conversation history.
        
        Args:
            conversation_id (str): Unique conversation identifier
            role (str): Role of the message sender (user/assistant)
            content (str): Message content
        """
        if conversation_id not in self.conversation_history:
            self.conversation_history[conversation_id] = []
        self.conversation_history[conversation_id].append({
            "role": role,
            "content": content
        })
    
    def get_conversation_history(self, conversation_id: str) -> List[Dict]:
        """
        Retrieve the conversation history for a given ID.
        
        Args:
            conversation_id (str): Unique conversation identifier
            
        Returns:
            List[Dict]: List of conversation messages
        """
        return self.conversation_history.get(conversation_id, [])
    
    def clear_conversation(self, conversation_id: str) -> None:
        """
        Clear the conversation history for a given ID.
        
        Args:
            conversation_id (str): Unique conversation identifier
        """
        if conversation_id in self.conversation_history:
            del self.conversation_history[conversation_id]
    
    def clear_all(self) -> None:
        """Clear all cached data and conversation histories."""
        self.cache.clear()
        self.conversation_history.clear()
        self.language_cache.clear()
        self.cultural_cache.clear()

# Create a global instance
context_cache = ContextCache() 