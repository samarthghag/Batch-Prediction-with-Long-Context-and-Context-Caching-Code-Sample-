import google.generativeai as genai
from typing import List, Dict, Optional
import logging
from .context_cache import ContextCache
import os

logger = logging.getLogger(__name__)

class BatchProcessor:
    def __init__(self):
        # Initialize Google API
        api_key = os.getenv('google_api_key')
        if not api_key:
            raise ValueError("API key not found. Please set the 'google_api_key' environment variable.")
            
        genai.configure(api_key=api_key)
        
        # Print first 5 characters of API key for debugging
        logger.info(f"Using API key starting with: {api_key[:5]}...")
        
        # List available models
        try:
            models = [m.name for m in genai.list_models()]
            logger.info(f"Available models: {models}")
        except Exception as e:
            logger.error(f"Error listing models: {str(e)}")
        
        # Initialize model
        try:
            self.model = genai.GenerativeModel('gemini-1.5-pro')
            logger.info("Successfully initialized Gemini model")
        except Exception as e:
            logger.error(f"Error initializing model: {str(e)}")
            raise
        
        # Initialize cache
        self.context_cache = ContextCache()

    def process_questions(self, questions: List[str], context: str) -> Dict[str, str]:
        """
        Process a batch of questions using the context.
        
        Args:
            questions (List[str]): List of questions to process
            context (str): Context text to use for answering questions
            
        Returns:
            Dict[str, str]: Dictionary mapping questions to answers
        """
        try:
            # Process questions in batches
            results = {}
            for question in questions:
                try:
                    # Check cache first
                    cached_response = self.context_cache.get_response(question, context)
                    if cached_response:
                        results[question] = cached_response
                        continue
                    
                    # Generate response
                    response = self.model.generate_content(
                        f"Context: {context}\n\nQuestion: {question}\n\nAnswer:"
                    )
                    
                    if response and response.text:
                        # Cache the response
                        self.context_cache.cache_response(question, context, response.text)
                        results[question] = response.text
                    else:
                        results[question] = "Failed to generate response."
                        
                except Exception as e:
                    logger.error(f"Error processing question '{question}': {str(e)}")
                    results[question] = f"Error: {str(e)}"
            
            return results
            
        except Exception as e:
            logger.error(f"Error in batch processing: {str(e)}")
            raise

    def generate_questions(self, context: str, limit: int = 5) -> List[str]:
        """
        Generate relevant questions based on the context.
        
        Args:
            context (str): Context text to generate questions from
            limit (int): Maximum number of questions to generate
            
        Returns:
            List[str]: List of generated questions
        """
        try:
            # Generate questions using the model
            prompt = f"""
            Based on the following context, generate {limit} relevant and insightful questions.
            Make sure the questions are diverse and cover different aspects of the content.
            
            Context: {context}
            
            Questions:
            """
            
            response = self.model.generate_content(prompt)
            
            if response and response.text:
                # Extract questions from response
                questions = [
                    line.strip().strip('0123456789.') for line in response.text.split('\n')
                    if line.strip() and any(c.isalpha() for c in line)
                ]
                return questions[:limit]
            
            return []
            
        except Exception as e:
            logger.error(f"Error generating questions: {str(e)}")
            return [] 