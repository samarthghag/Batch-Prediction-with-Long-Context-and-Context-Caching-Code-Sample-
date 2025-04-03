import google.generativeai as genai
from typing import List, Dict, Optional
import time
from config import settings
from utils.context_cache import context_cache
from utils.text_chunker import TextChunker

class BatchProcessor:
    def __init__(self):
        try:
            print(f"Initializing Gemini model with API key: {settings.google_api_key[:5]}...")
            genai.configure(api_key=settings.google_api_key)
            
            # List available models
            for m in genai.list_models():
                print(f"Available model: {m.name}")
            
            print(f"Attempting to use model: {settings.MODEL_NAME}")
            self.model = genai.GenerativeModel(settings.MODEL_NAME)
            print("Model initialized successfully")
        except Exception as e:
            print(f"Error initializing Gemini model: {str(e)}")
            raise
        self.text_chunker = TextChunker()
    
    def _prepare_prompt(self, context: str, question: str, conversation_history: List[Dict]) -> str:
        """Prepare the prompt with context, question, and conversation history."""
        prompt = f"""Context from video transcript:
{context}

Previous conversation:
"""
        
        for msg in conversation_history:
            prompt += f"{msg['role']}: {msg['content']}\n"
        
        prompt += f"\nCurrent question: {question}\n\nPlease provide a detailed answer based on the context and previous conversation."
        return prompt
    
    def _process_single_question(self, 
                               question: str, 
                               context_chunks: List[str], 
                               conversation_id: str) -> str:
        """Process a single question against all context chunks."""
        # Check cache first
        cached_response = context_cache.get_cached_response(question)
        if cached_response:
            return cached_response
        
        # Get conversation history
        history = context_cache.get_conversation_history(conversation_id)
        
        # Process each chunk and combine responses
        responses = []
        for chunk in context_chunks:
            prompt = self._prepare_prompt(chunk, question, history)
            
            try:
                print(f"Processing chunk with model: {settings.MODEL_NAME}")
                response = self.model.generate_content(
                    prompt,
                    generation_config={
                        "temperature": settings.TEMPERATURE,
                        "max_output_tokens": settings.MAX_TOKENS,
                    }
                )
                responses.append(response.text)
            except Exception as e:
                print(f"Error processing chunk: {str(e)}")
                continue
        
        # Combine responses if multiple chunks were processed
        if len(responses) > 1:
            # Use the model to synthesize the responses
            synthesis_prompt = f"""Please synthesize the following responses into a coherent answer:

Responses:
{chr(10).join(responses)}

Provide a comprehensive answer that combines all the information."""
            
            try:
                final_response = self.model.generate_content(
                    synthesis_prompt,
                    generation_config={
                        "temperature": settings.TEMPERATURE,
                        "max_output_tokens": settings.MAX_TOKENS,
                    }
                )
                response_text = final_response.text
            except Exception as e:
                print(f"Error synthesizing responses: {str(e)}")
                response_text = "\n".join(responses)
        else:
            response_text = responses[0] if responses else "No relevant information found."
        
        # Cache the response
        context_cache.cache_response(question, response_text)
        
        # Add to conversation history
        context_cache.add_to_conversation(conversation_id, "user", question)
        context_cache.add_to_conversation(conversation_id, "assistant", response_text)
        
        return response_text
    
    def process_batch(self, 
                     questions: List[str], 
                     context: str, 
                     conversation_id: str) -> List[Dict]:
        """Process a batch of questions."""
        # Clean and chunk the context
        clean_context = self.text_chunker.clean_text(context)
        context_chunks = self.text_chunker.chunk_text(clean_context)
        
        results = []
        for i, question in enumerate(questions):
            try:
                response = self._process_single_question(
                    question, 
                    context_chunks, 
                    conversation_id
                )
                results.append({
                    "question": question,
                    "answer": response,
                    "status": "success"
                })
            except Exception as e:
                results.append({
                    "question": question,
                    "answer": f"Error processing question: {str(e)}",
                    "status": "error"
                })
            
            # Add a small delay between questions to avoid rate limiting
            if i < len(questions) - 1:
                time.sleep(1)
        
        return results 