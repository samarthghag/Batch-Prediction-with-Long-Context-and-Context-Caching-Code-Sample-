from cachetools import TTLCache
from typing import Dict, List, Optional
import hashlib
from config import settings

class ContextCache:
    def __init__(self):
        self.cache = TTLCache(maxsize=100, ttl=settings.CACHE_TTL)
        self.conversation_history: Dict[str, List[Dict]] = {}
    
    def _generate_key(self, text: str) -> str:
        """Generate a unique key for the given text."""
        return hashlib.md5(text.encode()).hexdigest()
    
    def get_cached_response(self, text: str) -> Optional[str]:
        """Retrieve a cached response for the given text."""
        key = self._generate_key(text)
        return self.cache.get(key)
    
    def cache_response(self, text: str, response: str) -> None:
        """Cache a response for the given text."""
        key = self._generate_key(text)
        self.cache[key] = response
    
    def add_to_conversation(self, conversation_id: str, role: str, content: str) -> None:
        """Add a message to the conversation history."""
        if conversation_id not in self.conversation_history:
            self.conversation_history[conversation_id] = []
        self.conversation_history[conversation_id].append({
            "role": role,
            "content": content
        })
    
    def get_conversation_history(self, conversation_id: str) -> List[Dict]:
        """Retrieve the conversation history for a given ID."""
        return self.conversation_history.get(conversation_id, [])
    
    def clear_conversation(self, conversation_id: str) -> None:
        """Clear the conversation history for a given ID."""
        if conversation_id in self.conversation_history:
            del self.conversation_history[conversation_id]
    
    def clear_all(self) -> None:
        """Clear all cached data and conversation histories."""
        self.cache.clear()
        self.conversation_history.clear()

# Create a global instance
context_cache = ContextCache() 